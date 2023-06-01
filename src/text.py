import collections
import os
import pickle
from argparse import Namespace
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoModel


def download_models():
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                           init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)
    return model


class Text:
    def __init__(self, text_dir, model, num_steps):
        self.text_dir = text_dir
        self.model = model
        self.num_steps = num_steps

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

    def read_text(self, is_save=False, save_path=None):
        """抽取、预存"""
        text_embeddings = collections.defaultdict()
        dirs = os.listdir(self.text_dir)
        for dir in dirs:
            with open(self.text_dir + '/' + dir, 'r') as fr:
                for line in fr.readlines():
                    text = line.strip()
                    text_embeddings[text] = self.get_embedding(text)
        if is_save and save_path:
            with open(save_path, 'wb+') as fw:
                pickle.dump(text_embeddings, fw)

        return text_embeddings

    def load(self, load_path=None):
        if load_path:
            with open(load_path, 'rb') as f:
                return pickle.load(f)
        else:
            print("No path")

    def get_cosine_similarity(self, text1, text2):
        embed1 = self.get_embedding(text1)
        embed2 = self.get_embedding(text2)
        return torch.nn.functional.cosine_similarity(embed1, embed2, dim=0)

    def text_to_image(self, text, dict_path=None, image_path=None):
        """
            给定文本出图片
            到text_image_dict 读取图片名
            然后到images里面加载该图片然后返回
        """
        if dict_path and image_path:
            text_image = collections.defaultdict()
            with open(dict_path, 'r') as f:
                data = f.readlines()
                for sub_text, image in zip(data[::2], data[1::2]):
                    text_image[sub_text.strip()] = image.strip()
            image = text_image[text] + '.jpg'
            if image in os.listdir(image_path):
                res = Image.open(image_path+'/'+image)
                res.show()
                return res
            else:
                print("Image doesn't exist")
        else:
            print("No path")


if __name__ == '__main__':
    path = './pkl/texts.pkl'
    model = download_models()
    text = Text("../characters/haruhi/texts", model=model, num_steps=50)
    text.read_text(is_save=True, save_path=path)
    data = text.load(path)
    sub_text = "你们之中要是有外星人  未来人  异世界人或者超能力者的话 就尽管来找我吧！"
    dict_path = "../characters/haruhi/text_image_dict.txt"
    image_path = "../characters/haruhi/images"
    image = text.text_to_image(sub_text, dict_path=dict_path, image_path=image_path)
    print(data)
