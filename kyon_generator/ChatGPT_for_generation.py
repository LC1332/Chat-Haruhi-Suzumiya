# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个python程序是src_reform/ChatGPT.py中的一个分支，用于训练数据的生成
# 之后再由冷子昂进行合并

import json
import os
import numpy as np
import openai
import tiktoken
import torch
from scipy.spatial.distance import cosine
from langchain.chat_models import ChatOpenAI
import gradio as gr
import random
import time
import collections
import pickle
from argparse import Namespace
import torch
from PIL import Image
from torch import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import sys

sys.path.append("..")
from src_reform import utils
import re


# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY2")
# openai.proxy = "http://127.0.0.1:7890"

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# folder_name = "Suzumiya"
# current_directory = os.getcwd()
# new_directory = os.path.join(current_directory, folder_name)

# if not os.path.exists(new_directory):
#     os.makedirs(new_directory)
#     print(f"文件夹 '{folder_name}' 创建成功！")
# else:
#     print(f"文件夹 '{folder_name}' 已经存在。")

class ChatGPT:
    def __init__(self, configuration, in_training_generating=False):
        self.configuration = configuration
        self.in_training_generating = True
        self.image_embed_jsonl_path = configuration['image_embed_jsonl_path']
        self.title_text_embed_jsonl_path = configuration['title_text_embed_jsonl_path']
        self.images_folder = configuration['images_folder']
        self.texts_folder = configuration['texts_folder']
        self.system_prompt = configuration['system_prompt']
        with open(self.system_prompt, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        # print(self.system_prompt)
        self.max_len_story = int(configuration['max_len_story'])
        self.max_len_history = int(configuration['max_len_history'])
        self.dialogue_path = configuration['dialogue_path']
        openai.api_key = configuration["openai_key_1"] + configuration["openai_key_2"]
        os.environ["OPENAI_API_KEY"] = openai.api_key
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # 预加载jsonl文件
        self.model = utils.download_models()
        self.image_embed = None
        self.title_text_embed = None
        self.title_to_text = None
        self.titles = None

        self.is_train_generating = False
        self.role_name = ""
        self.other_names = []

    def set_training(self, role_name, other_names):
        self.is_train_generating = True
        self.role_name = role_name
        self.other_names = other_names

    def preload(self):
        self.image_embed = self.load(load_image_embed=True)
        self.title_text_embed, self.title_to_text, self.titles = self.load(load_title_text_embed=True)

    def load(self, load_title_text_embed=False,
             load_image_embed=False):
        if load_title_text_embed:
            text_embed = {}
            title_to_text = {}
            with open(self.title_text_embed_jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    text_embed.update(data)
            for title_text in text_embed.keys():
                res = title_text.split("link")
                title_to_text[res[0]] = res[1]
            return text_embed, title_to_text, list(title_to_text.keys())

        elif load_image_embed:
            image_embed = {}
            if os.path.exists(self.image_embed_jsonl_path):
              with open(self.image_embed_jsonl_path, 'r', encoding='utf-8') as f:
                  for line in f:
                      data = json.loads(line)
                      image_embed.update(data)
              return image_embed
            else:
              return None
        else:
            print("Please specify the loading file！")

    def text_to_image(self, text):
        query_similarity = self.get_cosine_similarity(text, get_image=True)
        key_index = query_similarity.argmax(dim=0)
        text = list(self.image_embed.keys())[key_index]
        image = text + '.jpg'
        if image in os.listdir(self.images_folder):
            res = Image.open(self.images_folder + '/' + image)
            # res.show()
            return res
        else:
            print("Image doesn't exist")

    # 一个封装 OpenAI 接口的函数，参数为 Prompt，返回对应结果
    def get_completion_from_messages(self, messages, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,  # 控制模型输出的随机程度
        )
        #  print(str(response.choices[0].message))
        return response.choices[0].message["content"]

    def get_cosine_similarity(self, texts, get_image=False, get_texts=False):
        """
            计算文本列表的相似度避免重复计算query_similarity
            texts[0] = query
        """
        query_embedding = utils.get_embedding(self.model, texts)[0].reshape(1, -1)
        if get_image:
            jsonl = self.image_embed
        elif get_texts:
            jsonl = self.title_text_embed
        # else:
        #     # 计算query_embed
        #     jsonl = {}
        #     embeddings = utils.get_embedding(self.model, texts[1:]).reshape(-1, 1536)
        #     for text, embed in zip(texts, embeddings):
        #         jsonl[text] = embed
        texts_embeddings = np.array([value for value in jsonl.values()])
        return cosine_similarity(query_embedding, torch.from_numpy(texts_embeddings).to(self.device))

    def retrieve_title(self, query_text, k):
        # compute cosine similarity between query_embed and embeddings
        texts = [query_text]
        embed_to_title = self.titles
        cosine_similarities = self.get_cosine_similarity(texts, get_texts=True).cpu().numpy().tolist()
        # sort cosine similarity
        sorted_cosine_similarities = sorted(cosine_similarities, reverse=True)
        top_k_index = []
        top_k_title = []
        for i in range(len(sorted_cosine_similarities)):
            current_title = embed_to_title[cosine_similarities.index(sorted_cosine_similarities[i])]
            if current_title not in top_k_title:
                top_k_title.append(current_title)
                top_k_index.append(cosine_similarities.index(sorted_cosine_similarities[i]))
            if len(top_k_title) == k:
                break
        return top_k_title

    def organize_stories_with_maxlen_for_training(self, selected_sample):
        stories = []

        count = 0

        for sample_topic in selected_sample:
            # find sample_answer in dictionary
            sample_story = self.title_to_text[sample_topic]

            sample_len = len(self.enc.encode(sample_story))
            # print(sample_topic, ' ' , sample_len)
            if sample_len + count > self.max_len_story:
                break

            stories.append(sample_story)

            count += sample_len

        return stories

    def organize_story_with_maxlen(self, selected_sample):
        story = "\n"

        count = 0

        final_selected = []
        print(selected_sample)
        for sample_topic in selected_sample:
            # find sample_answer in dictionary
            sample_story = self.title_to_text[sample_topic]

            sample_len = len(self.enc.encode(sample_story))
            # print(sample_topic, ' ' , sample_len)
            if sample_len + count > self.max_len_story:
                break

            story += sample_story
            story += '\n'

            count += sample_len
            final_selected.append(sample_topic)

        return story, final_selected

    def organize_message(self, story, history_chat, history_response, new_query):
        messages = [{'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': story}]

        n = len(history_chat)
        if n != len(history_response):
            print('warning, unmatched history_char length, clean and start new chat')
            # clean all
            history_chat = []
            history_response = []
            n = 0

        for i in range(n):
            messages.append({'role': 'user', 'content': history_chat[i]})
            messages.append({'role': 'user', 'content': history_response[i]})

        messages.append({'role': 'user', 'content': new_query})

        return messages

    def keep_tail(self, history_chat, history_response):
        n = len(history_chat)
        if n == 0:
            return [], []

        if n != len(history_response):
            print('warning, unmatched history_char length, clean and start new chat')
            return [], []

        token_len = []
        for i in range(n):
            chat_len = len(self.enc.encode(history_chat[i]))
            res_len = len(self.enc.encode(history_response[i]))
            token_len.append(chat_len + res_len)

        keep_k = 1
        count = token_len[n - 1]

        for i in range(1, n):
            count += token_len[n - 1 - i]
            if count > self.max_len_history:
                break
            keep_k += 1

        return history_chat[-keep_k:], history_response[-keep_k:]

    def divide_story(self, story):
        storys = re.split(r'\n{2,}', story.strip())
        for s in storys:
            lines = s.split('\n')
            for i in range(len(lines)):
                if lines[i].startswith(self.role_name) or any([lines[i].startswith(name) for name in self.other_names]):
                    res = '\n'.join(lines[:i]), '\n'.join(lines[i:])
                    print(res)
                    return res
                    break
        return "", ""

    def organize_message_langchain_for_training(self, storys, history_chat, history_response, new_query):
        messages = [
            SystemMessage(content=self.system_prompt)
        ]

        for story in storys:
            ai_message, human_message = self.divide_story(story)
            messages.append(AIMessage(content=ai_message))
            messages.append(HumanMessage(content=human_message))

        n = len(history_chat)
        if n != len(history_response):
            print('warning, unmatched history_char length, clean and start new chat')
            # clean all
            history_chat = []
            history_response = []
            n = 0

        for i in range(n):
            messages.append(HumanMessage(content=history_chat[i]))
            messages.append(AIMessage(content=history_response[i]))

        # messages.append( {'role':'user', 'content':new_query })
        messages.append(HumanMessage(content=new_query))
        print(messages)
        return messages

    def organize_message_for_generator(self, story, history_chat, history_response, new_query):

        raw_messages = self.divide_story(story)

        messages = [
            SystemMessage(content=self.system_prompt),
        ]
        for raw_message in raw_messages:
            messages.append(AIMessage(content=raw_message[0]))
            messages.append(HumanMessage(content=raw_message[1]))

        n = len(history_chat)
        if n != len(history_response):
            print('warning, unmatched history_char length, clean and start new chat')
            # clean all
            history_chat = []
            history_response = []
            n = 0

        for i in range(n):
            messages.append(HumanMessage(content=history_chat[i]))
            messages.append(AIMessage(content=history_response[i]))

        # messages.append( {'role':'user', 'content':new_query })
        messages.append(HumanMessage(content=new_query))
        print(messages)
        return messages

    def organize_message_langchain(self, story, history_chat, history_response, new_query):
        # messages =  [{'role':'system', 'content':SYSTEM_PROMPT}, {'role':'user', 'content':story}]

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=story)
        ]

        n = len(history_chat)
        if n != len(history_response):
            print('warning, unmatched history_char length, clean and start new chat')
            # clean all
            history_chat = []
            history_response = []
            n = 0

        for i in range(n):
            messages.append(HumanMessage(content=history_chat[i]))
            messages.append(AIMessage(content=history_response[i]))

        # messages.append( {'role':'user', 'content':new_query })
        messages.append(HumanMessage(content=new_query))
        print(messages)
        return messages

    def get_response(self, user_message, chat_history_tuple):

        history_chat = []
        history_response = []

        if len(chat_history_tuple) > 0:
            for cha, res in chat_history_tuple:
                history_chat.append(cha)
                history_response.append(res)

        history_chat, history_response = self.keep_tail(history_chat, history_response)

        print('history done')

        new_query = user_message

        if (self.is_train_generating == False) or (self.role_name == ""):

            selected_sample = self.retrieve_title(new_query, 7)
            print("备选辅助：", selected_sample)
            story, selected_sample = self.organize_story_with_maxlen(selected_sample)

            ## TODO: visualize seletected sample later
            print('当前辅助sample:', selected_sample)
            messages = self.organize_message_langchain(story, history_chat, history_response, new_query)
        else:
            selected_sample = self.retrieve_title(new_query, 7)
            print("备选辅助：", selected_sample)
            stories = self.organize_stories_with_maxlen_for_training(selected_sample)

            messages = self.organize_message_langchain_for_training(stories, history_chat, history_response, new_query)

        chat = ChatOpenAI(temperature=0)
        return_msg = chat(messages)

        response = return_msg.content

        return response
