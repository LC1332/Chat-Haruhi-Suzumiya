# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个python程序用于处理Chat凉宫春日项目中的聊天记录，将聊天记录转换为对话形式，并去除重复的对话
# 用法：python chatlog2dialogue.py -input <input_file> -output <output_file>
# 其中，input_file是聊天记录文件，output_file是输出文件，如果不指定，则默认为input_file_dedup.jsonl


import argparse
import json

# TODO: 定义处理函数，对记录后的对话中重复的对话进行去除
def deduplicate_dialogue(input_file, output_file):
    pass

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="Process chat logs in jsonl format")

    # 添加命令行参数
    parser.add_argument("-input", type=str, required=True, help="Input file in jsonl format")
    parser.add_argument("-output", type=str, help="Output file in jsonl format")

    # 解析命令行参数
    args = parser.parse_args()

    # 设置输出文件名
    output_file = args.output if args.output else args.input.rstrip('.jsonl') + '_dedup.jsonl'

    # 打印程序来源
    print("")

    # 调用处理函数
    deduplicate_dialogue(args.input, output_file)