import collections
import os
import pickle
from argparse import Namespace
import torch
from PIL import Image
from torch import cosine_similarity
from transformers import AutoTokenizer, AutoModel


def download_models():
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                           init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)
    return model


class Text:
    def __init__(self, text_dir, model, num_steps, pkl_path=None, dict_path=None, image_path=None):
        self.text_dir = text_dir
        self.model = model
        self.num_steps = num_steps
        self.pkl_path = pkl_path
        self.dict_path = dict_path
        self.image_path = image_path

    def get_embedding(self, text):
        tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
        model = download_models()
        if len(text) > self.num_steps:
            text = text[:self.num_steps]
        texts = [text]
        # Tokenize the text
        inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
        # Extract the embeddings
        # Get the embeddings
        with torch.no_grad():
            embeddings = model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
        return embeddings[0]

    def read_text(self, is_save=False):
        """抽取、预存"""
        text_embeddings = collections.defaultdict()
        dirs = os.listdir(self.text_dir)
        for dir in dirs:
            with open(self.text_dir + '/' + dir, 'r') as fr:
                for line in fr.readlines():
                    ch = '：' if '：' in line else ':'
                    if '旁白' in line:
                        text = line.strip().split(ch)[1].strip()
                    else:
                        text = ''.join(list(line.strip().split(ch)[1])[1:-1])  # 提取「」内的文本
                    text_embeddings[text] = self.get_embedding(text)
        if is_save and self.pkl_path:
            with open(self.pkl_path, 'wb+') as fw:
                pickle.dump(text_embeddings, fw)

        return text_embeddings

    def load(self):
        if self.pkl_path:
            with open(self.pkl_path, 'rb') as f:
                return pickle.load(f)
        else:
            print("No pkl_path")

    def get_cosine_similarity(self, texts):
        """
            计算文本列表的相似度避免重复计算query_similarity
            texts[0] = query
        """
        pkl = self.load()
        texts_similarity = []
        texts_embeddings = []
        query_embedding = pkl[texts[0]] if texts[0] in pkl.keys() else self.get_embedding(texts[0])
        texts_embeddings.append(query_embedding)
        for text in texts[1:]:
            text_embedding = pkl[text] if text in pkl.keys() else self.get_embedding(text)
            texts_embeddings.append(text_embedding)
        for embed in texts_embeddings[1:]:
            texts_similarity.append(cosine_similarity(query_embedding, embed, dim=0))
        return texts_similarity

    def text_to_image(self, text):
        """
            给定文本出图片
            计算query 和 texts 的相似度，取最高的作为new_query 查询image
            到text_image_dict 读取图片名
            然后到images里面加载该图片然后返回
        """
        if self.dict_path and self.image_path:
            text_image = collections.defaultdict()
            with open(self.dict_path, 'r') as f:
                data = f.readlines()
                for sub_text, image in zip(data[::2], data[1::2]):
                    text_image[sub_text.strip()] = image.strip()
            keys = list(text_image.keys())
            keys.insert(0, text)
            query_similarity = self.get_cosine_similarity(keys)
            key_index = query_similarity.index(max(query_similarity))
            text = list(text_image.keys())[key_index]

            image = text_image[text] + '.jpg'
            if image in os.listdir(self.image_path):
                res = Image.open(self.image_path + '/' + image)
                # res.show()
                return res
            else:
                print("Image doesn't exist")
        else:
            print("No path")

    def text_to_text(self, text):
        pkl = self.load()
        texts = list(pkl.keys())
        texts.insert(0, text)
        texts_similarity = self.get_cosine_similarity(texts)
        key_index = texts_similarity.index(max(texts_similarity))
        value = list(pkl.keys())[key_index]
        return value


if __name__ == '__main__':
    pkl_path = './pkl/texts.pkl'
    dict_path = "../characters/haruhi/text_image_dict.txt"
    image_path = "../characters/haruhi/images"
    model = download_models()
    text = Text("../characters/haruhi/texts", model=model, num_steps=50, pkl_path=pkl_path, dict_path=dict_path, image_path=image_path)
    # text.read_text(is_save=True)
    # data = text.load()
    sub_text = "什么？你在说什么啊？我可不会让你这么轻易地逃脱我的视线。SOS团可是需要你这样的人才的。"
    # image = text.text_to_image(sub_text, dict_path=dict_path, image_path=image_path)
    # print(image)
    # print(data)
    value = text.text_to_text(sub_text)
    print(value)
