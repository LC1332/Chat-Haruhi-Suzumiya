import argparse
import os
import json

# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个python程序用于处理Chat凉宫春日项目中的聊天记录，从聊天记录中抽取所有非主角的对话
# 用法：python dialogue2chat.py -input <input_file> -output <output_file> -role <role_name> -other_names <other_names>
# 其中，input_file是聊天记录文件，output_file是输出文件，如果不指定，则默认为input_file_one_line_chat.jsonl
# role_name是主角的名字，如果不指定，则默认为春日
# other_names是主角的其他名字（对于凉宫春日来说，有凉宫春日，凉宫），如果不指定，则默认为空

def process_dialogue(input_file, output_file, role, other_names):
    """
    核心函数，用于处理聊天记录，从中抽取非主角的对话
    """
    result = []
    output_dir = os.path.abspath(os.path.dirname(output_file))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cnt = 0
    
    f_read = open(input_file, 'r',encoding='utf-8')
    lines = f_read.readlines()
    last_item = {}
    for line in lines:
        cnt += 1
        content = json.loads(line)["dialogue"]
        for item in content:
            current_role = item["role"]
            if current_role in other_names + [role]:
                if last_item and not last_item["text"] == "": 
                    result.append(last_item)
                last_item = {}
            else:
                last_item = item
    return generage_jsonl(result, output_file)



def generage_jsonl(result, output_file):
    fw = open(output_file, 'w+', encoding='utf-8')
    for content in result:       
        if content:
            content["text"] = content["text"].strip()
            if content["text"] != '':
                json.dump({"role": content["role"], "text": content["text"], "source": "dialogue"}, fw, ensure_ascii=False)
                fw.write("\n")
    fw.close()



if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Process dialogue data for Chat Haruhi Suzumiya project')
    parser.add_argument('-input', required=True, help='Input file path')
    parser.add_argument('-output', help='Output file path')
    parser.add_argument('-role', default='春日', help='Main role name (default: 春日)')
    parser.add_argument('-other_names', nargs='*', default=[], help='Other role names (default: None)')
    args = parser.parse_args()

    # 处理参数
    input_file = args.input
    output_file = args.output if args.output else input_file.replace('.jsonl', '_one_line_chat.jsonl')
    role = args.role
    other_names = args.other_names

    # 调用核心函数进行处理
    process_dialogue(input_file, output_file, role, other_names)


    
#python dialogue2chat.py -input ./data/Haruhi-Lulu_Dialogues.jsonl -output ./output/chat_from_dialogue.jsonl -role "春日" -other_names 凉宫 凉宫春日