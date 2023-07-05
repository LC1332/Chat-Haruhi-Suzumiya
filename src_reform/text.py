import collections
import os
import pickle
from argparse import Namespace

import numpy as np
import torch
from PIL import Image
from torch import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from utils import download_models

class Text:
    def __init__(self, text_dir, model, num_steps, text_image_pkl_path=None, dict_text_pkl_path=None, pkl_path=None, dict_path=None, image_path=None, maps_path=None):
        self.dict_text_pkl_path = dict_text_pkl_path
        self.text_image_pkl_path = text_image_pkl_path
        self.text_dir = text_dir
        self.model = model
        self.num_steps = num_steps
        self.pkl_path = pkl_path
        self.dict_path = dict_path
        self.image_path = image_path
        self.maps_path = maps_path
        self.embed_model = download_models()

    def get_embedding(self, texts):
        tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
        
        # 截断
        # str or strList
        texts = texts if isinstance(texts, list) else [texts]
        for i in range(len(texts)):
            if len(texts[i]) > self.num_steps:
                texts[i] = texts[i][:self.num_steps]
        # Tokenize the texts
        inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
        # Extract the embeddings
        # Get the embeddings
        with torch.no_grad():
            embeddings = self.embed_model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
        return embeddings[0] if len(texts) == 1 else embeddings

    def read_text(self, save_embeddings=False, save_maps=False):
        """抽取、预存"""
        text_embeddings = collections.defaultdict()
        text_keys = []
        dirs = os.listdir(self.text_dir)
        data = []
        texts = []
        id = 0
        for dir in dirs:
            with open(self.text_dir + '/' + dir, 'r') as fr:
                for line in fr.readlines():
                    category = collections.defaultdict(str)
                    ch = '：' if '：' in line else ':'
                    if '旁白' in line:
                        text = line.strip().split(ch)[1].strip()
                    else:
                        text = ''.join(list(line.strip().split(ch)[1])[1:-1])  # 提取「」内的文本
                    if text in text_keys:  # 避免重复的text，导致embeds 和 maps形状不一致
                        continue
                    text_keys.append(text)
                    if save_maps:
                        category["titles"] = dir.split('.')[0]
                        category["id"] = str(id)
                        category["text"] = text
                        id = id + 1
                        data.append(dict(category))
                    texts.append(text)
        embeddings = self.get_embedding(texts)
        if save_embeddings:
            for text, embed in zip(texts, embeddings):
                text_embeddings[text] = self.get_embedding(text)
        if save_embeddings:
            self.store(self.pkl_path, text_embeddings)
        if save_maps:
            self.store(self.maps_path, data)

        return text_embeddings, data

    def load(self, load_pkl=False, load_maps=False, load_dict_text=False, load_text_image=False):
        if self.pkl_path and load_pkl:
            with open(self.pkl_path, 'rb') as f:
                return pickle.load(f)
        elif self.maps_path and load_maps:
            with open(self.maps_path, 'rb') as f:
                return pickle.load(f)
        elif self.dict_text_pkl_path and load_dict_text:
            with open(self.dict_text_pkl_path, 'rb') as f:
                return pickle.load(f)
        elif self.text_image_pkl_path and load_text_image:
            with open(self.text_image_pkl_path, 'rb') as f:
                return pickle.load(f)
        else:
            print("No pkl_path")

    def get_cosine_similarity(self, texts, get_image=False, get_texts=False):
        """
            计算文本列表的相似度避免重复计算query_similarity
            texts[0] = query
        """
        if get_image:
            pkl = self.load(load_dict_text=True)
        elif get_texts:
            pkl = self.load(load_pkl=True)
        else:
            pkl = {}
            embeddings = self.get_embedding(texts[1:]).reshape(-1, 1536)
            for text, embed in zip(texts, embeddings):
                pkl[text] = embed

        query_embedding = self.get_embedding(texts[0]).reshape(1, -1)
        texts_embeddings = np.array([value.numpy().reshape(-1, 1536) for value in pkl.values()]).squeeze(1)
        return cosine_similarity(query_embedding, torch.from_numpy(texts_embeddings))

    def store(self, path, data):
        with open(path, 'wb+') as f:
            pickle.dump(data, f)

    def text_to_image(self, text, save_dict_text=False):
        """
            给定文本出图片
            计算query 和 texts 的相似度，取最高的作为new_query 查询image
            到text_image_dict 读取图片名
            然后到images里面加载该图片然后返回
        """
        if save_dict_text:
            text_image = {}
            with open(self.dict_path, 'r') as f:
                data = f.readlines()
                for sub_text, image in zip(data[::2], data[1::2]):
                    text_image[sub_text.strip()] = image.strip()
            self.store(self.text_image_pkl_path, text_image)

            keys_embeddings = {}
            embeddings = self.get_embedding(list(text_image.keys()))
            for key, embed in zip(text_image.keys(), embeddings):
                keys_embeddings[key] = embed
            self.store(self.dict_text_pkl_path, keys_embeddings)

        if self.dict_path and self.image_path:
            # 加载 text-imageName
            text_image = self.load(load_text_image=True)
            keys = list(text_image.keys())
            keys.insert(0, text)
            query_similarity = self.get_cosine_similarity(keys, get_image=True)
            key_index = query_similarity.argmax(dim=0)
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
        pkl = self.load(load_pkl=True)
        texts = list(pkl.keys())
        texts.insert(0, text)
        texts_similarity = self.get_cosine_similarity(texts, get_texts=True)
        key_index = texts_similarity.argmax(dim=0).item()
        value = list(pkl.keys())[key_index]
        return value


# if __name__ == '__main__':
    # pkl_path = './pkl/texts.pkl'
    # maps_path = './pkl/maps.pkl'
    # text_image_pkl_path='./pkl/text_image.pkl'
    # dict_path = "../characters/haruhi/text_image_dict.txt"
    # dict_text_pkl_path = './pkl/dict_text.pkl'
    # image_path = "../characters/haruhi/images"
    # text_dir = "../characters/haruhi/texts"
    # model = download_models()
    # text = Text(text_dir, text_image_pkl_path=text_image_pkl_path, maps_path=maps_path,
    #             dict_text_pkl_path=dict_text_pkl_path, model=model, num_steps=50, pkl_path=pkl_path,
    #             dict_path=dict_path, image_path=image_path)
    # text.read_text(save_maps=True, save_embeddings=True)
    # data = text.load(load_pkl=True)
    # sub_text = "你好！"
    # image = text.text_to_image(sub_text)
    # print(image)
    # sub_texts = ["hello", "你好"]
    # print(text.get_cosine_similarity(sub_texts))
    # value = text.text_to_text(sub_text)
    # print(value)
