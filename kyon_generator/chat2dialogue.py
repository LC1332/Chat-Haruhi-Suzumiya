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

import json
import argparse
import configparser
from ChatGPT_for_generation import ChatGPT


def load_chat(filename):
    with open(filename, 'r') as f:
        chats = [json.loads(line) for line in f]
    return chats


def save_dialogue(filename, dialogue):
    with open(filename, 'w') as f:
        for message in dialogue:
            f.write(json.dumps(message) + '\n')



def parse_args():
    parser = argparse.ArgumentParser(description='Chat to Dialogue Conversion')
    parser.add_argument('-input_chat', type=str, required=True, help='input chat file (jsonl)')
    parser.add_argument('-output_dialogue', type=str, default=None, help='output dialogue file (jsonl)')
    parser.add_argument('-config', type=str, default='config.ini', help='configuration file (ini)')
    parser.add_argument('-role_name', type=str, required=True, help='role name')
    parser.add_argument('-other_names', type=str, default='', help='other names')
    return parser.parse_args()


def main(input_chat, output_dialogue, config_file, role_name, other_names):
    # Load chat data
    chat_data = load_chat(input_chat)

    # Load config
    configuration = {}
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    sections = config.sections()
    items = config.items(role_name)
    for key, value in items:
        configuration[key] = value

    # Initialize ChatGPT
    chatgpt = ChatGPT(configuration)

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
        dialogue.append({"dialogue": [{"role": role, "text": text}, {"role": role_name, "text": response}]})

    # Save dialogue to output file
    if output_dialogue is None:
        output_dialogue = f'{input_chat}_to_dialogue.jsonl'
    save_dialogue(output_dialogue, dialogue)


if __name__ == '__main__':
    args = parse_args()
    main(args.input_chat, args.output_dialogue, args.config, args.role_name, args.other_names)