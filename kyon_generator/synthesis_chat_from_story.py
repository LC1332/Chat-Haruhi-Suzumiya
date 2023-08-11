from argparse import Namespace
import glob
import os
import argparse
import random 
import openai
import json


"""
python3 synthesis_chat_from_story.py --role_name "乔峰" --world_name "天龙八部" --story_folder "/Users/pufferfish/Chat-Haruhi-Suzumiya/characters/qiaofeng/texts" --output "/Users/pufferfish/Chat-Haruhi-Suzumiya/kyon_generator/qiaofeng.txt"
"""

# api_key1 = "sk-V7X5Kq1E91fkKalyQ0yxT"
# api_key2 = "3BlbkFJSGzqxobu1DqsYGUvlCNa"
# api_key = api_key1 + api_key2
# api_key = "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"


openai.api_base = "http://api.ai-gaochao.com/v1"
api_key1 = "sk-RwVzjYxlKJTxUDZE89"
api_key2 = "CaA512C6164a92A683E55f60Ce953b"

openai.api_key = api_key1+api_key2

instruction = "You are asked to come up with a set of 10 diverse dialogues. These dialogues will be used to test a ChatBot that plays the role of {role_name} from the {world_name}. We will evaluate how well this ChatBot completes these dialogues. "
requirements = """
You are asked to come up with a set of 10 diverse dialogues. These dialogues will be used to test a ChatBot that plays the role of {role_name} from the {world_name}. We will evaluate how well this ChatBot completes these dialogues.
The requirements are:

1. Try not to repeat verbs in the dialogues to maximize diversity. 

2. The language used in the dialogues also should be diverse. For example, you should combine statements and questions.

3. The types of dialogues should be diverse. It should include open-ended questions, questions about the ChatBot's identity, suggestions for activities, pushing the story forward, etc.

4. The ChatBot should be able to answer these questions. For example, do not ask the ChatBot to generate any visual or audio output. Also, do not ask the ChatBot to perform any actions.

5. The dialogues should be in Chinese. 

6. Each dialogue should be 1-2 sentences long. Statements and questions are permitted.

7. You should generate appropriate questioning input for each dialogue. The input should provide an engaging context, ideally no more than 100 words.
"""

def find_elements_with_prefix(my_list, prefix):
    return [index for index, item in enumerate(my_list) if item.startswith(prefix)]

def get_all_characters(my_list):
    return list(set([item[:2] for item in my_list]))

def merge_list(mylist):
    merged_list = [i for i in mylist]
    
    jumped_index = []
    cur_value = mylist[0]
    for index, value in enumerate(mylist):
        if value[:2] == cur_value[:2]:
            jumped_index.append(index)
            merged_list[index] = merged_list[index] + mylist[index]
        else:
            cur_value = value
    # counter = 0 
    for i,v in enumerate(merged_list):
        if i in jumped_index:
            merged_list[i] = ""
    merged_list[0] = mylist[0]
    
    # lst = []
    # print(len(jumped_index))
    # for i,v in enumerate(merged_list):
        # if (v != ''):
        #     merged_list[i] = mylist[i] + "\n" + v
        # if (v == '' and i not in jumped_index):
            # merged_list[i] = mylist[i]
            # lst.append(i)
            # print("________")
            # print("这个是原句的i : ", i, mylist[i])
            # print("这个是一个合并后的v : ", v)
            # print(merged_list[i])
            # print("________")
            # counter += 1
    # print(merged_list)
    # print("this is counter : ", counter)
    # print(jumped_index)
    # print(lst)
    filtered_list = [item for item in merged_list if item != '']
    # print("这个是filtered ", len(filtered_list))
    # lst = []
    return merged_list

def generate_examples(my_list, role_index, number):
    random_elements = random.sample(role_index, number)
    example_lst = [[my_list[i-1],my_list[i]] for i in random_elements]
    return example_lst

def find_elements_before_marker(lst, marker):
    result = []
    for i in range(len(lst)):
        if lst[i] == marker:
            if i > 0:  # Make sure not to access an index before the start of the list
                result.append(lst[i - 1])
    return result

def save2json(role_name, mystring, output):
    pass
    lines_list = mystring.splitlines()
    r_list = find_elements_before_marker(lines_list, "ChatBot Answer:")
    for i in r_list:
        dialogue = i.split(":")
        if (role_name not in dialogue[0]):
            role = dialogue[0]
            if "「" in dialogue[1]:
                text = dialogue[1].replace("「","")
            if "」" in dialogue[1]:
                text = text.replace("」","")
            savejson = {"role": f"{role}", "text": f"{text}","source":"synthesized"}
            json_string = json.dumps(savejson, ensure_ascii=False)
            with open(output, "a", encoding='utf-8') as file:
                file.write(json_string + "\n")

def remove_duplicates(file_path):
    pass
    seen_texts = set()
    with open(file_path, encoding='utf-8') as f_in:
        with open(file_path+"nodup", 'w', encoding='utf-8') as f_out:
            for line in f_in:
                obj = json.loads(line)
                text = obj['text']
                if text not in seen_texts:
                    f_out.write(line)
                    seen_texts.add(text)

def synthesis(**params):
    pass
    if (params.get("role_name")):
        role_name = params["role_name"]
    if (params.get("world_name")):
        world_name = params["world_name"]
    if (params.get("story_folder")):
        story_folder = params["story_folder"]
    if (params.get("output")):
        output = params["output"]
    txt_files = glob.glob(os.path.join(story_folder, '*.txt'))
    all_stories = []
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.readlines()
            all_stories += content
            # print(f"Contents of {txt_file}:")
            # print(len(content))
    # print(len(all_stories))
    merged_stories = merge_list(all_stories)

    role_list = find_elements_with_prefix(merged_stories, role_name)
    random_examples = generate_examples(merged_stories, role_list, 5)
    print(random_examples)
    content = requirements
    for i in random_examples:
        if (len(i[0]) < 10 or len(i[1]) < 10):
            continue
        content += "\n"
        content += "###"
        content += "\n"
        content += "Question:"
        content += "\n"
        content += i[0]
        content += "ChatBot Answer:"
        content += "\n"
        content += i[1]
    content += "\n"
    content += "###"
    content += "\n"
    content += "Question:"
    # print(content)
    
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": content},
        ],
        temperature = 0.1
    )
    # print(result['choices'][0]['message']['content'])
    save2json(role_name, result['choices'][0]['message']['content'], output)
    remove_duplicates(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--role_name', type=str)
    parser.add_argument('--world_name', type=str)
    parser.add_argument('--story_folder', type=str)
    parser.add_argument('--output', type=str)
    
    args = parser.parse_args()
    params_dict = vars(args)

    for j in range(50):
        try:
            synthesis(**params_dict)
        except:
            continue
        

    # folder_names = ['tangshiye','weixiaobao','murongfu','liyunlong',\
    #             'Luna','wangduoyu','Ron','jiumozhi',\
    #             'Snape','haruhi','Malfoy','xuzhu',\
    #             'xiaofeng','duanyu','Hermione','Dumbledore',\
    #             'wangyuyan','qiaofeng',\
    #             'yuqian','Harry','McGonagall' ,\
    #             'baizhantang','tongxiangyu','guofurong',\
    #             'wanderer','zhongli','hutao',\
    #             'Sheldon','Raj','Penny']

    # role_names = ['汤师爷','韦小宝','慕容复','李云龙',\
    #           'Luna','王多鱼','Ron','鸠摩智',\
    #           'Snape','春日','Malfoy','虚竹',\
    #           '萧峰','段誉','Hermione','Dumbledore',\
    #           '王语嫣','乔峰',\
    #           '于谦','Harry','Professor McGonagall',\
    #           '白展堂','佟湘玉','郭芙蓉',\
    #           '流浪者','钟离','胡桃',\
    #           'Sheldon','Raj','Penny']

    # world_names = ['让子弹飞','鹿鼎记','天龙八部','亮剑',\
    #           'HarryPotter','西虹市首富','HarryPotter','天龙八部',\
    #           'HarryPotter','凉宫春日','HarryPotter','天龙八部',\
    #           '天龙八部','天龙八部','HarryPotter','HarryPotter',\
    #           '天龙八部','天龙八部',\
    #           '相声','HarryPotter','HarryPotter',\
    #           '同福客栈','同福客栈','同福客栈',\
    #           '原神','原神','原神',\
    #           'BigBang', 'BigBang','BigBang']          

    # for i,v in enumerate(folder_names):
    #     folder_path = "/Users/pufferfish/Chat-Haruhi-Suzumiya/characters/"
    #     out_path = "/Users/pufferfish/Chat-Haruhi-Suzumiya/kyon_generator/"
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument('--role_name', type=str, default=role_names[i])
    #     parser.add_argument('--world_name', type=str, default=world_names[i])
    #     parser.add_argument('--story_folder', type=str, default=folder_path+v+"/texts")
    #     parser.add_argument('--output', type=str, default=out_path+v)
    #     args = parser.parse_args()
    #     params_dict = vars(args)
    #     for j in range(50):
    #         try:
    #             synthesis(**params_dict)
    #         except:
    #             continue
    # remove_duplicates(params_dict.get("output"))
