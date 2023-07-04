import configparser
import json
import pickle

import utils
import os


class StoreData:
    def __init__(self, configuration):
        self.title_to_text_pkl_path = configuration['title_to_text_pkl_path']
        self.text_image_pkl_path = configuration['text_image_pkl_path']
        self.dict_text_pkl_path = configuration['dict_text_pkl_path']
        self.text_embed_jsonl_path = configuration['text_embed_jsonl_path']
        self.dict_path = configuration['dict_path']
        self.image_path = configuration['image_path']
        self.folder = configuration['folder']
        self.model = utils.download_models()

    def store_data(self):
        text_embed = []
        title_to_text = {}
        titles = []
        for file in os.listdir(self.folder):
            if file.endswith('.txt'):
                title_name = file[:-4]
                with open(os.path.join(self.folder, file), 'r', encoding='utf-8') as fr:
                    title_to_text[title_name] = fr.read()
                    titles.append(title_name)
        for text, embed in zip(titles, utils.get_embedding(self.model, list(title_to_text.values()))):
            text_embed.append({text: embed.numpy().tolist()})
        self.store(self.title_to_text_pkl_path, title_to_text)
        self.store(self.text_embed_jsonl_path, text_embed)

        # text_image = {}
        # with open(self.dict_path, 'r', encoding='utf-8') as f:
        #     data = f.readlines()
        #     for sub_text, image in zip(data[::2], data[1::2]):
        #         text_image[sub_text.strip()] = image.strip()
        # self.store(self.text_image_pkl_path, text_image)
        #
        #
        # keys_embeddings = {}
        # for key in text_image.keys():
        #     keys_embeddings[key] = utils.get_embedding(self.model, key)
        # self.store(self.dict_text_pkl_path, keys_embeddings)

    def store(self, path, data):
        if path == self.text_embed_jsonl_path:
            with open(self.text_embed_jsonl_path, 'w+', encoding='utf-8') as f:
                for item in data:
                    json.dump(item, f, ensure_ascii=False)
                    f.write('\n')
        else:
            with open(path, 'wb+') as f:
                pickle.dump(data, f)

configuration = {}
config = configparser.ConfigParser()
character = "liyunlong"
config.read('config.ini')
sections = config.sections()
items = config.items(character)
print(f"正在加载: {character} 角色")
for key, value in items:
    configuration[key]=value

run = StoreData(configuration)
run.store_data()
