# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个程序用来将一句话的对话转化为连续的一段对话
# 用法：python chat2dialogue.py -input_chat <input_chat> -output_dialogue <output_dialogue> -config <config_file> -role_name <role_name> -other_names <other_names>
# 其中，input_chat是聊天记录文件，output_dialogue是输出文件，如果不指定，则默认为input_chat_to_dialogue.jsonl
# config_file是配置文件，如果不指定，则默认为config.ini
# role_name是主角的名字，如果不指定，则默认为春日
# other_names是主角的其他名字（对于凉宫春日来说，有凉宫春日，凉宫），如果不指定，则默认为空

# 现在ChatGPT类中间的divide_story函数还没有实现，应该实现之后就基本能跑了
# 关于config.ini的配置，请咨询冷子昂和闫晨曦


# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 18:58
# @Author  : scixing, chenxi
# @FileName: chat2dialogue.py
# @Software: PyCharm
# @github  ：https://github.com/LC1332/Chat-Haruhi-Suzumiya

import json
import argparse
import configparser

from ChatGPT_for_generation import ChatGPT


def load_chat(filename):
    with open(filename, 'r') as f:
        chats = [json.loads(line) for line in f]
    return chats


def save_dialogue(filename, dialogue):
    with open(filename, 'w+', encoding='utf-8') as f:
        for message in dialogue:
            f.write(json.dumps(message, ensure_ascii=False) + '\n')


def parse_args():
    parser = argparse.ArgumentParser(description='Chat to Dialogue Conversion')
    parser.add_argument('-input_chat', nargs="+", type=str, required=True, help='input chat file (jsonl)')
    parser.add_argument('-config_role_name', nargs="+", type=str, required=True, help='role name in config.ini')
    parser.add_argument('-text_role_name', nargs="+", type=str, required=True, help='role name in texts folder')
    return parser.parse_args()


def main(input_chat, role_name, other_names):
    # Load chat data
    chat_data = load_chat(input_chat)

    # Load config
    configuration = {}
    config = configparser.ConfigParser()
    config.read("../src_reform/config.ini", encoding='utf-8')
    sections = config.sections()
    print(config.items)
    items = config.items(role_name)
    for key, value in items:
        configuration[key] = value

    # Initialize ChatGPT
    chatgpt = ChatGPT(configuration)
    chatgpt.preload()
    # Set role training
    chatgpt.set_training(role_name, other_names.split())

    # Generate dialogue
    dialogue = []
    for chat in chat_data:
        role = chat['role']
        text = chat['text']

        # Format user message
        user_message = f'{role}:「{text}」'

        # Get response from ChatGPT
        response = chatgpt.get_response(user_message, [])

        # Append message to dialogue
        dialogue.append({"dialogue": [{"role": role, "text": text}, {"role": role_name, "text": response}], "source": "synthesized"})

    # Save dialogue to output file
    output_dialogue = f'{input_chat[:-4]}_to_dialogue.jsonl'
    save_dialogue(output_dialogue, dialogue)


if __name__ == '__main__':
    args = parse_args()
    input_chat_lis = args.input_chat
    config_role_name_lis = args.config_role_name
    text_role_name_lis = args.text_role_name
    if len(input_chat_lis) == len(config_role_name_lis) == len(text_role_name_lis):
        for input_chat, config_role_name, text_role_name in zip(input_chat_lis, config_role_name_lis, text_role_name_lis):
            main(input_chat, config_role_name, text_role_name)
