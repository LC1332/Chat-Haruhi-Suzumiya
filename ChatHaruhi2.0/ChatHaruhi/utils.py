from argparse import Namespace

from openai import OpenAI

# client = OpenAI(api_key=<YOUR OPENAI API KEY>)

from transformers import AutoModel, AutoTokenizer
import torch
import random

import tiktoken
import re

import numpy as np

import base64
import struct

import os

import tqdm

import requests



def get_access_token():
    API_KEY = os.getenv("StoryAudit_API_AK")
    SECRET_KEY = os.getenv("StoryAudit_API_SK")

    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

'''
文本审核接口
'''
def text_censor(text):
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"

    params = {"text":text}
    access_token = get_access_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    return response.json()["conclusion"] == "合规"

def package_role( system_prompt, texts_path , embedding ):
    datas = []

    # 暂时只有一种embedding 'luotuo_openai'
    embed_name = 'luotuo_openai'

    datas.append({ 'text':system_prompt , embed_name:'system_prompt'})
    datas.append({ 'text':'Reserve Config Setting Here' , embed_name:'config'})
    

    # debug_count = 3

    # for file in os.listdir(texts_path):

    files = os.listdir(texts_path)

    for i in tqdm.tqdm(range(len(files))):
        file = files[i]
        # if file name end with txt
        if file.endswith(".txt"):
            file_path = os.path.join(texts_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                current_str = f.read()
                current_vec = embedding(current_str)
                encode_vec = float_array_to_base64(current_vec)
                datas.append({ 'text':current_str , embed_name:encode_vec})

                # debug_count -= 1
                # if debug_count == 0:
                #     break
    return datas


import struct

def string_to_base64(text):
    byte_array = b''
    for char in text:
        num_bytes = char.encode('utf-8')
        byte_array += num_bytes

    base64_data = base64.b64encode(byte_array)
    return base64_data.decode('utf-8')

def base64_to_string(base64_data):
    byte_array = base64.b64decode(base64_data)
    text = byte_array.decode('utf-8')
    return text


def float_array_to_base64(float_arr):
    
    byte_array = b''
    
    for f in float_arr:
        # 将每个浮点数打包为4字节
        num_bytes = struct.pack('!f', f)  
        byte_array += num_bytes
    
    # 将字节数组进行base64编码    
    base64_data = base64.b64encode(byte_array)
    
    return base64_data.decode('utf-8')

def base64_to_float_array(base64_data):

    byte_array = base64.b64decode(base64_data)
    
    float_array = []
    
    # 每 4 个字节解析为一个浮点数
    for i in range(0, len(byte_array), 4):
        num = struct.unpack('!f', byte_array[i:i+4])[0] 
        float_array.append(num)

    return float_array


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

_luotuo_model = None

_luotuo_model_en = None
_luotuo_en_tokenizer = None

_enc_model = None

# ======== add bge_zh mmodel
# by Cheng Li
# 这一次我们试图一次性去适配更多的模型

_model_pool = {}
_tokenizer_pool = {}

# BAAI/bge-small-zh-v1.5

def get_general_embeddings( sentences , model_name = "BAAI/bge-small-zh-v1.5" ):

    global _model_pool
    global _tokenizer_pool

    if model_name not in _model_pool:
        from transformers import AutoTokenizer, AutoModel
        _tokenizer_pool[model_name] = AutoTokenizer.from_pretrained(model_name)
        _model_pool[model_name] = AutoModel.from_pretrained(model_name)

    _model_pool[model_name].eval()

    # Tokenize sentences
    encoded_input = _tokenizer_pool[model_name](sentences, padding=True, truncation=True, return_tensors='pt', max_length = 512)

    # Compute token embeddings
    with torch.no_grad():
        model_output = _model_pool[model_name](**encoded_input)
        # Perform pooling. In this case, cls pooling.
        sentence_embeddings = model_output[0][:, 0]

    # normalize embeddings
    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
    return sentence_embeddings.cpu().tolist()

def get_general_embedding( text_or_texts , model_name = "BAAI/bge-small-zh-v1.5" ):
    if isinstance(text_or_texts, str):
        return get_general_embeddings([text_or_texts], model_name)[0]
    else:
        return get_general_embeddings_safe(text_or_texts, model_name)
    
general_batch_size = 16

import math

def get_general_embeddings_safe(sentences, model_name = "BAAI/bge-small-zh-v1.5"):
    
    embeddings = []
    
    num_batches = math.ceil(len(sentences) / general_batch_size)
    
    for i in tqdm.tqdm( range(num_batches) ):
        # print("run bge with batch ", i)
        start_index = i * general_batch_size
        end_index = min(len(sentences), start_index + general_batch_size)
        batch = sentences[start_index:end_index]
        embs = get_general_embeddings(batch, model_name)
        embeddings.extend(embs)
        
    return embeddings

def get_bge_zh_embedding( text_or_texts ):
    return get_general_embedding(text_or_texts, "BAAI/bge-small-zh-v1.5")

## TODO: 重构bge_en部分的代码，复用general的函数

# ======== add bge model
# by Cheng Li
# for English only right now

_bge_model = None
_bge_tokenizer = None

def get_bge_embeddings( sentences ):
    # unsafe ensure batch size by yourself

    global _bge_model
    global _bge_tokenizer

    if _bge_model is None:
        from transformers import AutoTokenizer, AutoModel
        _bge_tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
        _bge_model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

    _bge_model.eval()

    # Tokenize sentences
    encoded_input = _bge_tokenizer(sentences, padding=True, truncation=True, return_tensors='pt', max_length = 512)

    # Compute token embeddings
    with torch.no_grad():
        model_output = _bge_model(**encoded_input)
        # Perform pooling. In this case, cls pooling.
        sentence_embeddings = model_output[0][:, 0]
    # normalize embeddings
    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
    return sentence_embeddings.cpu().tolist()

def get_bge_embedding( text_or_texts ):
    if isinstance(text_or_texts, str):
        return get_bge_embeddings([text_or_texts])[0]
    else:
        return get_bge_embeddings_safe(text_or_texts)

bge_batch_size = 32

import math
# from tqdm import tqdm

def get_bge_embeddings_safe(sentences):
    
    embeddings = []
    
    num_batches = math.ceil(len(sentences) / bge_batch_size)
    
    for i in tqdm.tqdm( range(num_batches) ):
        # print("run bge with batch ", i)
        start_index = i * bge_batch_size
        end_index = min(len(sentences), start_index + bge_batch_size)
        batch = sentences[start_index:end_index]
        embs = get_bge_embeddings(batch)
        embeddings.extend(embs)
        
    return embeddings

# === add bge model

def tiktokenizer( text ):
    global _enc_model

    if _enc_model is None:
        _enc_model = tiktoken.get_encoding("cl100k_base")

    return len(_enc_model.encode(text))
    
def response_postprocess(text,dialogue_bra_token = '「',dialogue_ket_token = '」'):
    lines = text.split('\n')
    new_lines = ""

    first_name = None

    for line in lines:
        line = line.strip(" ")
        match = re.match(r'^(.*?)[:：]' + dialogue_bra_token + r"(.*?)" + dialogue_ket_token + r"$", line)

        
        if match:
            curr_name = match.group(1)
            # print(curr_name)
            if first_name is None:
                first_name = curr_name
                new_lines += (match.group(2))
            else:
                if curr_name != first_name:
                    return first_name + ":" + dialogue_bra_token +  new_lines + dialogue_ket_token
                else:
                    new_lines += (match.group(2))
            
        else:
            if first_name == None:
                return text
            else:
                return first_name + ":" + dialogue_bra_token +  new_lines + dialogue_ket_token
    return first_name + ":" + dialogue_bra_token + new_lines + dialogue_ket_token

def download_models():
    print("正在下载Luotuo-Bert")
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                           init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert-medium", trust_remote_code=True, model_args=model_args).to(
        device)
    print("Luotuo-Bert下载完毕")
    return model

def get_luotuo_model():
    global _luotuo_model
    if _luotuo_model is None:
        _luotuo_model = download_models()
    return _luotuo_model


def luotuo_embedding(model, texts):
    # Tokenize the texts_source
    tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert-medium")
    inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
    inputs = inputs.to(device)
    # Extract the embeddings
    # Get the embeddings
    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
    return embeddings

def luotuo_en_embedding( texts ):
    # this function implemented by Cheng
    global _luotuo_model_en
    global _luotuo_en_tokenizer

    if _luotuo_model_en is None:
        _luotuo_en_tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert-en")
        _luotuo_model_en = AutoModel.from_pretrained("silk-road/luotuo-bert-en").to(device)

    if _luotuo_en_tokenizer is None:
        _luotuo_en_tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert-en")

    inputs = _luotuo_en_tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
    inputs = inputs.to(device)

    with torch.no_grad():
        embeddings = _luotuo_model_en(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
        
    return embeddings


def get_embedding_for_chinese(model, texts):
    model = model.to(device)
    # str or strList
    texts = texts if isinstance(texts, list) else [texts]
    # 截断
    for i in range(len(texts)):
        if len(texts[i]) > 510:
            texts[i] = texts[i][:510]
    if len(texts) >= 64:
        embeddings = []
        chunk_size = 64
        for i in range(0, len(texts), chunk_size):
            embeddings.append(luotuo_embedding(model, texts[i: i + chunk_size]))
        return torch.cat(embeddings, dim=0)
    else:
        return luotuo_embedding(model, texts)


def is_chinese_or_english(text):
    # no longer use online openai api
    return "chinese"

    text = list(text)
    is_chinese, is_english = 0, 0

    for char in text:
        # 判断字符的Unicode值是否在中文字符的Unicode范围内
        if '\u4e00' <= char <= '\u9fa5':
            is_chinese += 4
        # 判断字符是否为英文字符（包括大小写字母和常见标点符号）
        elif ('\u0041' <= char <= '\u005a') or ('\u0061' <= char <= '\u007a'):
            is_english += 1
    if is_chinese >= is_english:
        return "chinese"
    else:
        return "english"


def get_embedding_openai(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_embedding_for_english(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

import os

def luotuo_openai_embedding(texts, is_chinese= None ):
    """
        when input is chinese, use luotuo_embedding
        when input is english, use openai_embedding
        texts can be a list or a string
        when texts is a list, return a list of embeddings, using batch inference
        when texts is a string, return a single embedding
    """

    openai_key = os.environ.get("OPENAI_API_KEY")

    if isinstance(texts, list):
        index = random.randint(0, len(texts) - 1)
        if openai_key is None or is_chinese_or_english(texts[index]) == "chinese":
            return [embed.cpu().tolist() for embed in get_embedding_for_chinese(get_luotuo_model(), texts)]
        else:
            return [get_embedding_for_english(text) for text in texts]
    else:
        if openai_key is None or is_chinese_or_english(texts) == "chinese":
            return get_embedding_for_chinese(get_luotuo_model(), texts)[0].cpu().tolist()
        else:
            return get_embedding_for_english(texts)


# compute cosine similarity between two vector
def get_cosine_similarity( v1, v2):
    v1 = torch.tensor(v1).to(device)
    v2 = torch.tensor(v2).to(device)
    return torch.cosine_similarity(v1, v2, dim=0).item()

    

