# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个python程序用于处理Chat凉宫春日项目中的文本，从故事文本中抽取所有非主角的对话
# 用法：python story2chat.py -story_folder <story_folder> -output <output_file> -role <role_name> -other_names <other_names>
# 其中，story_folder是故事文本文件夹，output_file是输出文件，如果不指定，则默认为input_file_one_line_chat.jsonl
# role_name是主角的名字，如果不指定，则默认为春日
# other_names是主角的其他名字（对于凉宫春日来说，有凉宫春日，凉宫），如果不指定，则默认为空

import argparse
import os
import glob
import json

def process_dialogue(input_files, output_file, role, other_names):
    result = []
    output_dir = os.path.abspath(os.path.dirname(output_file))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cnt = 0
    for file in input_files:
        cnt += 1
        f_read = open(file, 'r',encoding='utf-8')
        lines = f_read.readlines()
        last_content = ""
        for line in lines:
            if ":" in line:
                current_role = line.split(":")[0]
            elif '：' in line:
                current_role = line.split("：")[0]
            else:
                current_role = ""
            
            if current_role in other_names + [role]:
                if not last_content == "": 
                    result.append(last_content)
                last_content = ""
            else:
                last_content = line
    return generage_jsonl(result, output_file)



def generage_jsonl(result, output_file):
    fw = open(output_file, 'w+', encoding='utf-8')
    """
    {"role": "阿虚", "text": "「奇特的社团和运动社团有什么不同？」", "source": "synthesized "}
    """
    # remove duplicate element from result
    seen = set()
    new_result = []
    for item in result:
        if item not in seen:
            seen.add(item)
            new_result.append(item)
            
    for content in new_result:       
        content = content.strip()
        if content:
            if ":" in content:
                res = content.split(':')
            elif '：' in content:
                res = content.split('：')
            if res[1] != '':
                text = res[1]
                if text[0] == "「":
                    text = text[1:]
                if text[-1] == "」":
                    text = text[:-1]
                json.dump({"role": res[0], "text": text , "source": "story"}, fw, ensure_ascii=False)
                fw.write("\n")
    fw.close()

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='Process story data for Chat Haruhi Suzumiya project',
        epilog='author:LengYue(https://github.com/zealot52099)'
    )


    parser.add_argument('-story_folder', required=True, help='Story folder path')
    parser.add_argument('-output', required=True, help='Output file path')
    parser.add_argument('-role', default='春日', help='Main role name (default: 春日)')
    parser.add_argument('-other_names', nargs='*', default=[], help='Other role names (default: None)')
    args = parser.parse_args()

    # 处理参数
    story_folder = args.story_folder
    output_file = args.output
    role = args.role
    other_names = args.other_names

    # 检查story_folder下是否有txt文件
    txt_files = glob.glob(os.path.join(story_folder, '*.txt'))
    if not txt_files:
        print(f"No txt files found in {story_folder}")
        exit(1)

    # 调用核心函数进行处理
    process_dialogue(txt_files, output_file, role, other_names)

# if __name__ == '__main__':
#     main()


#python story2chat.py -story_folder "/characters/haruhi/texts" -output ./output/chat_from_story.json -role "春日" -other_names 凉宫 凉宫春日