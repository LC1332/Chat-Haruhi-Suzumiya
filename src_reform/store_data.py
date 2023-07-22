import configparser
import json
import utils
import os


class StoreData:
    def __init__(self, configuration, input_folder=None, output_folder=None):
        self.image_embed_jsonl_path = configuration['image_embed_jsonl_path']
        self.title_text_embed_jsonl_path = configuration['title_text_embed_jsonl_path']
        self.images_folder = configuration['images_folder']
        self.texts_folder = configuration['texts_folder']
        self.model = utils.download_models()
        self.input_folder = input_folder
        self.output_folder = output_folder

    def split_text(self):
        for file in os.listdir(self.input_folder):
            with open(os.path.join(self.input_folder, file), encoding='utf-8') as f:
                data = f.read()
                for i, dialogue in enumerate(data.split('\n\n')):
                    with open(os.path.join(self.output_folder, f"{file[:-4]}_{i}.txt"), 'w+', encoding='utf-8') as fw:
                        fw.write(dialogue.strip())

    def preload(self, store_image=False):
        title_text_embed = []
        title_text = []
        for file in os.listdir(self.texts_folder):
            if file.endswith('.txt'):
                title_name = file[:-4]
                with open(os.path.join(self.texts_folder, file), 'r', encoding='utf-8') as fr:
                    title_text.append(f"{title_name}link{fr.read()}")
        for title_text, embed in zip(title_text, utils.get_embedding(self.model, title_text)):
            title_text_embed.append({title_text: embed.cpu().numpy().tolist()})
        self.store(self.title_text_embed_jsonl_path, title_text_embed)

        if store_image:
            image_embed = []
            images = []
            for file in os.listdir(self.images_folder):
                images.append(file[:-4])
            for image, embed in zip(images, utils.get_embedding(self.model, images)):
                image_embed.append({image: embed.cpu().numpy().tolist()})
            self.store(self.image_embed_jsonl_path, image_embed)

    def store(self, path, data):
        with open(path, 'w+', encoding='utf-8') as f:
            for item in data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')


configuration = {}
config = configparser.ConfigParser()
character = "于谦"  # 指定1
config.read('config.ini', encoding='utf-8')
sections = config.sections()
items = config.items(character)
print(f"正在加载: {character} 角色")
for key, value in items:
    configuration[key] = value
input_folder = "../src/ycx/yuqian"  # 指定2
output_folder = "../characters/yuqian/texts"  # 指定3
run = StoreData(configuration, input_folder=input_folder, output_folder=output_folder)
# run.split_text()
run.preload()
