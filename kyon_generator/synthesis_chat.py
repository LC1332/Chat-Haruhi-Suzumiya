# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个python程序用于从真实用户的jsonl中，调用特定的方法，进一步生成增广的jsonl文件
# 用法：python synthesis_chat.py -input <input_file> -output <output_file> -method <method_name>
# 其中，input_file是真实用户的jsonl文件，output_file是输出文件，如果不指定，则默认为input_file_syn_by_<method_name>.jsonl
# method_name是增广方法的名字，如果不指定，则默认为foo
#  
# additonal_config是增广方法的配置文件，如果不指定，则默认为config.txt
#
# 方法的例子见synthesis_chat_method_foo.py

import argparse
import os
import importlib

def synthesis_chat(input_file, output_file, method, additional_config=None):
    """
    核心函数，调用特定算法生成增广的jsonl文件
    """
    method_full_name = 'synthesis_chat_method_' + method

    # 检查method_full_name的py文件是否存在
    if not os.path.exists(method_full_name + '.py'):
        print(f"Method {method} not found, file {method_full_name}.py not found")
        exit(1)

    module = importlib.import_module(method_full_name)
    module.generate(input_file, output_file, additional_config)

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Synthesize chat data using a specific method')
    parser.add_argument('-input', required=True, help='Input file path')
    parser.add_argument('-output', help='Output file path')
    parser.add_argument('-method', default='foo', help='Synthesis method name (default: foo)')
    parser.add_argument('-additional_config', default='', help='Additional config file (default: config.txt)')
    args = parser.parse_args()

    # 处理参数
    input_file = args.input
    output_file = args.output
    method = args.method
    additional_config = args.additional_config

    # 如果未指定output文件名，则使用默认命名规则
    if not output_file:
        input_basename = os.path.basename(input_file)
        output_file = input_basename.replace('.jsonl', f'_syn_by_{method}.jsonl')

    # 调用核心函数进行生成
    synthesis_chat(input_file, output_file, method, additional_config = additional_config )