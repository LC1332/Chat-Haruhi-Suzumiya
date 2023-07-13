import os

import numpy as np

# os.environ['http_proxy'] = "http://127.0.0.1:1450"
# os.environ['https_proxy'] = "http://127.0.0.1:1450"
import argparse
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
from utils import download_models


class ChatGPT:
    def __init__(self, configuration):
        pass
        self.folder = configuration["folder"]
        with open(configuration["system_prompt"], 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
        self.max_len_story = int(configuration["max_len_story"])
        self.max_len_history = int(configuration["max_len_history"])
        self.model = download_models()
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.titles, self.title_to_text = self.read_prompt_data()
        self.embeddings, self.embed_to_title = self.title_text_embedding(self.titles, self.title_to_text)
        openai.api_key = configuration["openai_key_1"] + configuration["openai_key_2"]
        os.environ["OPENAI_API_KEY"] = openai.api_key

    def get_completion_from_messages(self, messages, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,  # 控制模型输出的随机程度
        )
        #  print(str(response.choices[0].message))
        return response.choices[0].message["content"]

    def read_prompt_data(self):
        """
            read prompt-data for in-context-learning
        """
        titles = []
        title_to_text = {}
        for file in os.listdir(self.folder):
            if file.endswith('.txt'):
                title_name = file[:-4]
                titles.append(title_name)

                with open(os.path.join(self.folder, file), 'r', encoding='utf-8') as f:
                    title_to_text[title_name] = f.read()

        return titles, title_to_text


    def get_embedding(self, text):
        tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
        # model = download_models()
        if len(text) > 512:
            text = text[:512]
        texts = [text]
        # Tokenize the text
        inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
        # Extract the embeddings
        # Get the embeddings
        with torch.no_grad():
            embeddings = self.model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
        return embeddings[0]

    def title_text_embedding(self, titles, title_to_text):
        """titles-text-embeddings"""

        embeddings = []
        embed_to_title = []

        for title in titles:
            text = title_to_text[title]

            # divide text with \n\n
            divided_texts = text.split('\n\n')

            for divided_text in divided_texts:
                embed = self.get_embedding(divided_text)
                embeddings.append(embed)
                embed_to_title.append(title)

        return embeddings, embed_to_title

    def get_cosine_similarity(self, embed1, embed2):
        return torch.nn.functional.cosine_similarity(embed1, embed2, dim=0)

    def retrieve_title(self, query_embed, embeddings, embed_to_title, k):
        # compute cosine similarity between query_embed and embeddings
        cosine_similarities = []
        for embed in embeddings:
            cosine_similarities.append(self.get_cosine_similarity(query_embed, embed))

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

    def organize_story_with_maxlen(self, selected_sample):
        maxlen = self.max_len_story
        # title_to_text, _ = self.read_prompt_data()
        story = "凉宫春日的经典桥段如下:\n"

        count = 0

        final_selected = []
        print(selected_sample)
        for sample_topic in selected_sample:
            # find sample_answer in dictionary
            sample_story = self.title_to_text[sample_topic]

            sample_len = len(self.enc.encode(sample_story))
            # print(sample_topic, ' ' , sample_len)
            if sample_len + count > maxlen:
                break

            story += sample_story
            story += '\n'

            count += sample_len
            final_selected.append(sample_topic)

        return story, final_selected

    def organize_message(self, story, history_chat, history_response, new_query):
        messages = [{'role': 'system', 'content': self.system_prompt}, {'role': 'user', 'content': story}]

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
        max_len = self.max_len_history
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
            if count > max_len:
                break
            keep_k += 1

        return history_chat[-keep_k:], history_response[-keep_k:]

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
        query_embed = self.get_embedding(new_query)

        # print("1")
        # embeddings, embed_to_title = self.title_text_embedding(self.titles, self.title_to_text)

        print("2")
        selected_sample = self.retrieve_title(query_embed, self.embeddings, self.embed_to_title, 7)

        print("3")
        story, selected_sample = self.organize_story_with_maxlen(selected_sample)

        ## TODO: visualize seletected sample later
        print('当前辅助sample:', selected_sample)

        messages = self.organize_message_langchain(story, history_chat, history_response, new_query)
        print(messages)
        chat = ChatOpenAI(temperature=0)
        return_msg = chat(messages)

        response = return_msg.content

        return response