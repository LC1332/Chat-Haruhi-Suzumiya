import configparser
import json
import utils
import os
from checkCharacter import checkCharacter


def split_text(input_file, output_folder):
    if input_file:
        with open(os.path.join(input_file), encoding='utf-8') as f:
            data = f.read()
            for i, dialogue in enumerate(data.split('\n\n')):
                with open(os.path.join(output_folder, f"{os.path.basename(input_file)[:-4]}_{i}.txt"),
                          'w+', encoding='utf-8') as fw:
                    fw.write(dialogue.strip())


def generate_character(cn_role_name, en_role_name, prompt=None):
    # 在config.ini中加添角色信息
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config.ini', encoding='utf-8')
    configuration = {}
    if cn_role_name in config.sections():
        print(f"已存在{cn_role_name}角色的配置文件")
    else:
        # 添加新的配置项
        config.add_section(cn_role_name)
        config[cn_role_name]['character_folder'] = f"../characters/{en_role_name}"
        config[cn_role_name][
            'image_embed_jsonl_path'] = f"../characters/{en_role_name}/jsonl/image_embed.jsonl"
        config[cn_role_name][
            'title_text_embed_jsonl_path'] = f"../characters/{en_role_name}/jsonl/title_text_embed.jsonl"
        config[cn_role_name]['images_folder'] = f"../characters/{en_role_name}/images"
        config[cn_role_name]["jsonl_folder"] = f"../characters/{en_role_name}/jsonl"
        config[cn_role_name]['texts_folder'] = f"../characters/{en_role_name}/texts"
        config[cn_role_name]['system_prompt'] = f"../characters/{en_role_name}/system_prompt.txt"
        config[cn_role_name]['dialogue_path'] = f"../characters/{en_role_name}/dialogues/"
        config[cn_role_name]['max_len_story'] = "1500"
        config[cn_role_name]['max_len_history'] = "1200"
        config[cn_role_name]['gpt'] = "True"
        config[cn_role_name]['local_tokenizer'] = "THUDM/chatglm2-6b"
        config[cn_role_name]['local_model'] = "THUDM/chatglm2-6b"
        config[cn_role_name]['local_lora'] = "Jyshen/Chat_Suzumiya_GLM2LoRA"
        # 保存修改后的配置文件
        with open('config.ini', 'w', encoding='utf-8') as config_file:
            config.write(config_file)
        config.read('config.ini', encoding='utf-8')
    # 检查角色文件夹
    items = config.items(cn_role_name)
    print(f"正在加载: {cn_role_name} 角色")
    for key, value in items:
        configuration[key] = value
    print(configuration)
    checkCharacter(configuration)
    if prompt is not None:
        with open(os.path.join(f"../characters/{en_role_name}", 'system_prompt.txt'), 'w+', encoding='utf-8') as f:
            f.write(prompt)
    return configuration


class StoreData:
    def __init__(self, configuration):
        self.image_embed_jsonl_path = configuration['image_embed_jsonl_path']
        self.title_text_embed_jsonl_path = configuration['title_text_embed_jsonl_path']
        self.images_folder = configuration['images_folder']
        self.texts_folder = configuration['texts_folder']
        self.model = utils.download_models()

    def preload(self):
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

        if len(os.listdir(configuration['images_folder'])) != 0:
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


if __name__ == '__main__':
    # prompt = "N"
    cn_role_name = "韦小宝"
    en_role_name = "weixiaobao"

    # ini 生成角色配置文件
    configuration = generate_character(cn_role_name, en_role_name)
    # 分割文件
    # input_file = './kunkun_all.txt'
    # output_folder = f"../characters/{en_role_name}/texts"
    # split_text(input_file, output_folder)

    # 存储数据
    run = StoreData(configuration)
    run.preload()


"""
请优化下列代码，整体思路是我需要读取selt.texts_folder 文件夹下的 若干文件并进行一定的操作后将结果写入到
```
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
```
"""