import argparse
import configparser
import json
import random
import sys

sys.path.append('..')
from src_reform import utils, checkCharacter
import os
import openai


# TODO

# 在这个文件中 重新实现embedding，替换 utils.get_embedding

# 把原来的embedding函数 在这里做一个 镜像

# 这里可以有一个比如叫chinese_embedding 的函数 return utils.get_embedding(model, text)
# 这个可以

# 你要实现一个if_chinese的函数，判断一个sentence是不是英文为主

# 建立一个combine_embedding函数， 先调用if_chinese然后再调用chinese_embedding或者english_embedding

# 一定要用 openai text-embedding-ada-002

# 写完之后，在test_kyon_generator.ipynb中跑通
# on the fly 增加 Hermione和Malfoy这两个人物

# 然后测试通他们对应的jsonl



def parse_args():
    parser = argparse.ArgumentParser(description='generate character 将台本文件保存成jsonl文件，动态创建新的角色')
    parser.add_argument('--cn_role_name', type=str, required=True, help='Chinese role name')
    parser.add_argument('--en_role_name', type=str, required=True, help='English role name')
    parser.add_argument('--prompt', default=None, type=str, help='prompt file path')
    parser.add_argument('--text_folder', type=str, help='character texts folder')
    return parser.parse_args()


def generate_character(cn_role_name, en_role_name, prompt=None):
    # 在config.ini中加添角色信息
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('../src_reform/config.ini', encoding='utf-8')
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
        with open('../src_reform/config.ini', 'w+', encoding='utf-8') as config_file:
            config.write(config_file)
        config.read('config.ini', encoding='utf-8')
    # 检查角色文件夹
    items = config.items(cn_role_name)
    print(f"正在加载: {cn_role_name} 角色")
    for key, value in items:
        configuration[key] = value
    checkCharacter.checkCharacter(configuration)
    if prompt is not None:
        fr = open(prompt, 'r')
        with open(os.path.join(f"../characters/{en_role_name}", 'system_prompt.txt'), 'w+', encoding='utf-8') as f:
            f.write(fr.read())
            print("system_prompt.txt已创建")
        fr.close()
    return configuration


class StoreData:
    def __init__(self, configuration, text_folder):
        self.image_embed_jsonl_path = configuration['image_embed_jsonl_path']
        self.title_text_embed_jsonl_path = configuration['title_text_embed_jsonl_path']
        self.images_folder = configuration['images_folder']
        self.texts_folder = text_folder
        self.model = utils.download_models()

    def preload(self):
        title_text_embed = []
        title_text = []
        for file in os.listdir(self.texts_folder):
            if file.endswith('.txt'):
                title_name = file[:-4]
                with open(os.path.join(self.texts_folder, file), 'r', encoding='utf-8') as fr:
                    title_text.append(f"{title_name}｜｜｜{fr.read()}")
        embeddings = utils.get_embedding(self.model, title_text)
        for title_text, embed in zip(title_text, embeddings):
            title_text_embed.append({title_text: embed})
        self.store(self.title_text_embed_jsonl_path, title_text_embed)

        if len(os.listdir(configuration['images_folder'])) != 0:
            image_embed = []
            images = []
            for file in os.listdir(self.images_folder):
                images.append(file[:-4])
            embeddings = utils.get_embedding(self.model, images)
            for image, embed in zip(images, embeddings):
                image_embed.append({image: embed})
            self.store(self.image_embed_jsonl_path, image_embed)
        print("角色创建成功!")

    def store(self, path, data):
        with open(path, 'w+', encoding='utf-8') as f:
            for item in data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')


if __name__ == '__main__':
    args = parse_args()

    cn_role_name = args.cn_role_name
    en_role_name = args.en_role_name
    prompt = args.prompt if args.prompt else None
    text_folder = args.text_folder if args.text_folder else f"../characters/{en_role_name}/texts"

    # ini 生成角色配置文件
    configuration = generate_character(cn_role_name, en_role_name, prompt=prompt)

    # 存储数据
    run = StoreData(configuration, text_folder)
    run.preload()

