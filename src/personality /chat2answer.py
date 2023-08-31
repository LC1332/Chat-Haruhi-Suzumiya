#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
__ToDo："answer personality questions with ChatHaruhi 2.0"
__author: "Aria:(https://github.com/ariafyy)"
"""

OPENAI_API_KEY = str(input("OPENAI_API_KEY :  "))
import os
import json, openai
openai.api_key = OPENAI_API_KEY
api_key = OPENAI_API_KEY
custom_api_key = OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = openai.api_key
from tqdm import tqdm
from chatharuhi import ChatHaruhi
import pandas as pd


class Chat2Answer(object):
    def __init__(self):
        pass

    def get_chat(self, role_name, query, system_prompt, story_text_folder):
        chatbot = ChatHaruhi(
            system_prompt=system_prompt,
            # story_db=story_chroma_folder,
            story_text_folder=story_text_folder,
            llm='openai')
        pre_prompt= """Answer in english with the following statement, option: correct, generally correct, partially correct, neither correct nor wrong, partially wrong, generally wrong, or wrong. \n"""
        response = chatbot.chat(text=pre_prompt+query, role='测试人员')
        return response

    def save_mbti_answers(self, role_name, mbti_question_path, out_csv_path, system_prompt, story_text_folder):
        data = []
        with open(mbti_question_path, 'r') as f:
            data_dict = json.load(f)
            questions_list = data_dict['questions']
            for i in tqdm(range(len(questions_list))):
                # for i in tqdm(range(2)):
                query = questions_list[i]["text"]
                answer = self.get_chat(role_name, query, system_prompt, story_text_folder)
                data.append([role_name, query, answer])
            df = pd.DataFrame(data, columns=["role", "question", "answer"])
            df.to_csv(out_csv_path, index=False)
            return df

    def get_role_mbti_answers(self, role_name, mbti_question_path, out_csv_path, system_prompt, story_text_folder):
        return self.save_mbti_answers(role_name, mbti_question_path, out_csv_path, system_prompt, story_text_folder)


if __name__ == '__main__':
    role_list = ["lilulu", "ayaka", "guofurong", "Hermione", "Malfoy", "murongfu",
                 "qiaofeng", "Ron", "tangshiye", "wangduoyu", "xiaofeng", "yuqian",
                 "baizhantang", "duanyu", "Harry", "hutao", "liyunlong", "McGonagall",
                 "Penny", "raidenShogun", "Sheldon", "tongxiangyu", "wangyuyan",
                 "xuzhu", "zhongli", "Dumbledore", "haruhi",
                 "jiumozhi", "Luna", "Megumi", "Raj", "Snape",
                 "wanderer", "weixiaobao", "yaemiko"]
    # for role_name in role_list:
    role_name = role_list[0]
    root_dir = str(input("项目绝对路径:eg.home/usr/Chat-Haruhi-Suzumiya:  "))
    # mbti 问题
    mbti_question_path = f"{root_dir}/src/personality/mbti_questions/mbti_en_61.json"
    # characters system_prompt
    system_prompt = f"{root_dir}/characters/{role_name}/system_prompt"
    # characters texts
    story_text_folder = f"{root_dir}/characters/{role_name}/texts"
    print("story_text_folder:  ", story_text_folder, '\n')
    out_csv_dir = f"{root_dir}/src/personality/" + 'outputs'
    if not os.path.exists(out_csv_dir):
        os.makedirs(out_csv_dir)
    out_csv_path = f"{root_dir}/src/personality/outputs/{role_name}.csv"
    Chat2Answer().get_role_mbti_answers(role_name, mbti_question_path, out_csv_path, system_prompt, story_text_folder)
