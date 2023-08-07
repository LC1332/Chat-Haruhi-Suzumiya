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
import os

from ChatGPT_for_generation import ChatGPT

from tqdm import tqdm


def load_chat(filename):
    with open(filename, 'r') as f:
        chats = [json.loads(line) for line in f]
    return chats


def save_dialogue(filename, dialogue):
    with open(filename, 'w+', encoding='utf-8') as f:
        for message in dialogue:
            f.write(json.dumps(message, ensure_ascii=False) + '\n')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Chat to Dialogue Conversion, output_dialogue 和 input_chat 在同一路径')
    parser.add_argument('-input_chat', type=str, required=True, help='input chat file (jsonl)')
    parser.add_argument('-output_dialogue', type=str, default=None, help='output dialogue file (jsonl)')
    parser.add_argument('-role_name', type=str, required=True, help='role name')
    parser.add_argument('-other_names', nargs="+", default="", type=str, help='other names')

    # arugments that figure out temporary saving folder
    parser.add_argument('-temp_save_folder', default=None, type=str, help='temproray saving file path')

    return parser.parse_args()


def merge_dialogue(user_message, dialogue_text):
    dialogue_list = dialogue_text.split('\n')  # Split dialogue into lines
    dialogue = [user_message]
    current_role = ""
    current_text = ""

    for line in dialogue_list:
        if line:
            ch = ":" if ":" in line else "："
            if ch in line:
                parts = line.split(ch)
                role = parts[0].strip().replace("凉宫春日", "春日")
                text = parts[1].strip()
            else:
                role = ""
                text = line

            if role == current_role:
                current_text = current_text[:-1]
                current_text += text[1:]
            else:
                if current_role != "":
                    dialogue.append({"role": current_role, "text": current_text})
                current_role = role
                current_text = text

    dialogue.append({"role": current_role, "text": current_text})  # Append the last dialogue

    return {"dialogue": dialogue, "source": "synthesized"}


def main(input_chat, output_dialogue, role_name, other_names, temp_save_folder):
    config = configparser.ConfigParser()
    config.read("../src_reform/config.ini", encoding='utf-8')
    if role_name not in config.sections():
        print(f"{role_name} 角色未创建，请创建角色后再使用，或是与config.ini 中角色一致")
    else:
        # Load chat data
        chat_data = load_chat(input_chat)

        # Load config
        configuration = {}

        print(config.items)
        items = config.items(role_name)
        for key, value in items:
            configuration[key] = value

        # Initialize ChatGPT
        chatgpt = ChatGPT(configuration)
        chatgpt.preload()
        # Set role training
        chatgpt.set_training(role_name, other_names)
        dialogue = []
        # Generate dialogue
        print("Generating dialogue...")

        # if temp_save_folder not exist, create it
        if not os.path.exists(temp_save_folder):
            os.mkdir(temp_save_folder)
            print(f"创建临时文件夹{temp_save_folder}")

        for i, chat in enumerate(tqdm(chat_data)):
            role = chat['role']
            text = chat['text']

            file_name = f"{i}_{text[:min(4,len(text))]}.jsonl" # 生成文件名
            # replace invalid characters
            file_name = file_name.replace("/", "_")

            # if os.path.join(temp_save_folder, file_name) exists, skip
            if os.path.exists(os.path.join(temp_save_folder, file_name)):
                continue


            user_message = f'{role}:「{text}」'

            response = chatgpt.get_response(user_message, [])
            temp_dialogue = [merge_dialogue(user_message, response)] 
            save_dialogue(os.path.join(temp_save_folder, file_name), temp_dialogue)

            # dialogue.append(merge_dialogue(user_message, response))

        # Save dialogue to output file

        # output_dialogue = f'{input_chat[:-4]}_to_dialogue.jsonl' if output_dialogue is None else output_dialogue
        # save_dialogue(output_dialogue, dialogue)

        # 合并临时文件
        output_dialogue = f'{input_chat[:-4]}_to_dialogue.jsonl' if output_dialogue is None else output_dialogue
        with open(output_dialogue, 'w',encoding= 'utf-8') as outfile:
            for filename in os.listdir(temp_save_folder):
                if filename.endswith('.jsonl'): 
                    filepath = os.path.join(temp_save_folder, filename)

                    # Cheng: 为了防止文件打不开，这里尝试打开三次
                    for i in range(3):
                        try:
                            with open(filepath) as infile:
                                for line in infile:
                                    outfile.write(line)
                            break
                        except:
                            if i == 2:
                                print(f"Warning: Failed to open file {filename} after 3 attempts, skipping...")
                    
                    # with open(filepath) as infile:
                    #     for line in infile:
                    #         outfile.write(line)


if __name__ == '__main__':
    args = parse_args()
    input_chat = args.input_chat
    output_dialogue = args.output_dialogue
    role_name = args.role_name
    other_names_lis = args.other_names

    temp_save_folder = args.temp_save_folder

    if temp_save_folder == None:
        # create output_<role_name>
        temp_save_folder = f"output_{role_name}"

    main(input_chat, output_dialogue, role_name, other_names_lis, temp_save_folder)
