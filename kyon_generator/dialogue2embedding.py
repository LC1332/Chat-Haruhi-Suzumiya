# -*- coding: utf-8 -*-

'''
FILE_NAME: dialogue2embedding.py
Edited by 冷子昂, Aug 8 2023
'''

import json
import os
# import torch
# import torch.nn as nn
import argparse
from argparse import Namespace
# from transformers import AutoTokenizer, AutoModel
from utils import download_models, get_embedding

model = download_models()

def filter_continuous_sequence(numbers):
    if not numbers:
        return []
    
    result = [numbers[0]]
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1] + 1:
            result.append(numbers[i])
    
    return result


def organize_json(file_path, out_path):
    pass
    # 不知道为什么我们的json格式非常奇怪，只能重新梳理，真迷
    # jsonl_file_path = '/Users/pufferfish/Downloads/story_synthesis_data/tangshiye_test_output_dialogue.jsonl'
    filename = file_path.split("/")[-1]
    out_path = out_path + filename
    print(out_path)
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            json_data = json.loads(line)
            # print(json_data["dialogue"][1])
            parts = json_data["dialogue"][0].split(':')
            # print(parts)
            new_dict = {"role":parts[0], "text":parts[1]}
            # new_json = json.dump(new_dict,ensure_ascii=False)
            json_data["dialogue"][0] = new_dict
            with open(out_path, 'a') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False)
                json_file.write('\n')

def contain_role(dialogue, role_name):
    pass
    role_name_length = len(role_name)
    for i,v in enumerate(dialogue):
        if v["role"][:role_name_length] == role_name:
            return True
    return False

def get_role_name_index(dialogue, role_name):
    pass
    index_list = []
    role_name_length = len(role_name)
    for i,v in enumerate(dialogue):
        if v["role"][:role_name_length] == role_name:
            index_list.append(i)
    return index_list


def train_json_file(dialogue, index_list, source, out_path):
    
    def get_message(sentence_json):
        return sentence_json["role"]+":"+sentence_json["text"]

    def write_json(query, chat_history, answer, embedding, out_path):
        json_line = {
                "query": query,
                "answer": answer,
                "chat_history": chat_history,
                "embedding": embedding,
                "source": "story-synthesised"
            }
        # print(json_line)
        with open(out_path, 'a', encoding='utf-8') as json_file:
            json.dump(json_line, json_file, ensure_ascii=False)
        return
    
    def get_history(dialogue):
        history = []
        for i in dialogue:
            history.append(get_message(i))
        return history

    chat_history = []
    query = ""
    embedding = []
    answer = ""

    index_list = filter_continuous_sequence(index_list)

    for index in index_list:
        pass
        if index == 0:
            chat_history.append(get_message(dialogue[0]))
        if index == 1:
            query = get_message(dialogue[index-1])
            chat_history = []
            answer = get_message(dialogue[index])
            embedding = get_embedding(model, query) # 要填充
            write_json(query, chat_history, answer, embedding, out_path)
        else:
            query = get_message(dialogue[index-1])
            chat_history = get_history(dialogue[:index-2])
            answer = get_message(dialogue[index])
            embedding = get_embedding(model, query) #要填充
            write_json(query, chat_history, answer, embedding, out_path)
            # print(index)
            # print(query)
            # print(chat_history)



def dialogue2embed(file_path, role_names, out_path):
    pass
    filename = file_path.split("/")[-1]
    out_path = out_path + filename
    if type(role_names) != list:
        role_names = [role_names]
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            dialogue = json.loads(line)["dialogue"]
            source = json.loads(line)["source"]
            for role_name in role_names:
                if contain_role(dialogue, role_name):
                    index_list = get_role_name_index(dialogue,role_name)
                    train_json_file(dialogue, index_list, source, out_path)
            # print(json.loads(line)["dialogue"])
            

# file_names = os.listdir("/Users/pufferfish/Downloads/story_synthesis_data")
# print(file_names)
# for file_name in file_names:
#     organize_json(
#         file_path = "/Users/pufferfish/Downloads/story_synthesis_data/"+file_name,
#         out_path = "/Users/pufferfish/Chat-Haruhi-Suzumiya/kyon_generator/organized_data/"
#     )

# dialogue2embed(
#     file_path = "/Users/pufferfish/Chat-Haruhi-Suzumiya/kyon_generator/organized_data/Harry_test_output_dialogue.jsonl", 
#     role_names = "Harry",
#     out_path = "/Users/pufferfish/Chat-Haruhi-Suzumiya/kyon_generator/training_data/")


# numbers = [1, 2, 3, 6, 8, 9, 10]
# filtered_numbers = filter_continuous_sequence(numbers)
# print(filtered_numbers)


# dic = {"tangshiye":['汤师爷'],
#        "murongfu":['慕容复'],
#        "liyunlong":['李云龙'],
#        "Luna":['Luna'],
#        "wangduoyu":['王多鱼'],
#        "Ron":['Ron', '罗恩'],
#        "jiumozhi":['鸠摩智'],
#        "Snape":['Snape'],
#        "haruhi":['春日', '凉宫春日', '涼宮ハルヒ', '涼宮'],
#        "Malfoy":['Malfoy'],
#        "xuzhu":['虚竹'],
#        "xiaofeng":['萧峰'],
#        "duanyu":['段誉'],
#        "Hermione":['Hermione', '赫敏'],
#        "Dumbledore":['Dumbledore', '邓布利多'],
#        "wangyuyan":['王语嫣'],
#        "Harry":['Harry', '哈利'],
#        "McGonagall":['McGonagall', 'Professor McGonagall'],
#        "baizhantang":['白展堂', '展堂'],
#        "tongxiangyu":['佟湘玉'],
#        "guofurong":['郭芙蓉'],
#        "wanderer":['旅行者', '流浪者'],
#        "zhongli":['钟离'],
#        "hutao":['胡桃'],
#        "Sheldon":['Sheldon'],
#        "Raj":['Raj'],
#        "Penny":['Penny'],
#        "weixiaobao":['韦小宝'],
#        "qiaofeng":['乔峰'],
#        "ayaka":['神里绫华'],
#        "raidenShogun":['雷电将军'],
#        "yuqian":['于谦']}
