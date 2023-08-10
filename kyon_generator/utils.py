from argparse import Namespace

import openai
from transformers import AutoModel, AutoTokenizer
import torch
import random

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def download_models():
    print("正在下载Luotuo-Bert")
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                           init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert-medium", trust_remote_code=True, model_args=model_args).to(
        device)
    print("Luotuo-Bert下载完毕")
    return model


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
    text = list(text)
    is_chinese, is_english = 0, 0
    for char in text:
        # 判断字符的Unicode值是否在中文字符的Unicode范围内
        if '\u4e00' <= char <= '\u9fa5':
            is_chinese += 1
        # 判断字符是否为英文字符（包括大小写字母和常见标点符号）
        elif ('\u0041' <= char <= '\u005a') or ('\u0061' <= char <= '\u007a') or ('\u0021' <= char <= '\u007e'):
            is_english += 1
    if is_chinese >= is_english:
        return "chinese"
    else:
        return "english"


def get_embedding_for_english(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def get_embedding(model, texts):
    """
        return type: list
    """
    if isinstance(texts, list):
        index = random.randint(0, len(texts) - 1)
        if is_chinese_or_english(texts[index]) == "chinese":
            return [embed.cpu().tolist() for embed in get_embedding_for_chinese(model, texts)]
        else:
            return [get_embedding_for_english(text) for text in texts]
    else:
        if is_chinese_or_english(texts) == "chinese":
            return get_embedding_for_chinese(model, texts)[0].cpu().tolist()
        else:
            return get_embedding_for_english(texts)






