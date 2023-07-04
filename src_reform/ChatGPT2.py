import json
import os
import numpy as np
import utils
# os.environ['http_proxy'] = "http://127.0.0.1:1450"
# os.environ['https_proxy'] = "http://127.0.0.1:1450"
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
import utils

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY2")
# openai.proxy = "http://127.0.0.1:7890"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
folder_name = "Suzumiya"
current_directory = os.getcwd()
new_directory = os.path.join(current_directory, folder_name)

if not os.path.exists(new_directory):
    os.makedirs(new_directory)
    print(f"文件夹 '{folder_name}' 创建成功！")
else:
    print(f"文件夹 '{folder_name}' 已经存在。")

enc = tiktoken.get_encoding("cl100k_base")


class ChatGPT:
    def __init__(self, configuration):
        self.title_to_text_pkl_path = configuration['title_to_text_pkl_path']
        self.text_image_pkl_path = configuration['text_image_pkl_path']
        self.dict_text_pkl_path = configuration['dict_text_pkl_path']
        self.text_embed_jsonl_path = configuration['text_embed_jsonl_path']
        self.dict_path = configuration['dict_path']
        self.image_path = configuration['image_path']
        self.folder = configuration['folder']
        self.system_prompt = configuration['system_prompt']
        self.max_len_story = int(configuration['max_len_story'])
        self.max_len_history = int(configuration['max_len_history'])
        self.save_path = configuration['save_path']
        openai.api_key = configuration["openai_key_1"] + configuration["openai_key_2"]
        os.environ["OPENAI_API_KEY"] = openai.api_key
        # 预加载pkl文件
        self.model = utils.download_models()
        self.dict_text = None
        self.text_image = None
        self.title_to_text = None
        self.text_embed = None
        self.titles = None

    def read_data(self):
        self.dict_text = self.load(load_dict_text=True)
        self.text_image = self.load(load_text_image=True)
        self.title_to_text = self.load(load_title_to_text=True)
        self.text_embed = self.load(load_text_embed=True)
        self.titles = list(self.text_embed.keys())



    def store(self, path, data):
        with open(path, 'wb+') as f:
            pickle.dump(data, f)

    def load(self, load_text_embed=False, load_dict_text=False,
             load_text_image=False, load_title_to_text=False):
        if load_text_embed:
            if self.text_embed_jsonl_path:
                text_embed = {}
                with open(self.text_embed_jsonl_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        data = json.loads(line)
                        text_embed.update(data)
                return text_embed
            else:
                print("No text_embed_pkl_path")
        elif load_dict_text:
            if self.dict_text_pkl_path:
                with open(self.dict_text_pkl_path, 'rb') as f:
                    return pickle.load(f)
            else:
                print("No dict_text_pkl_path")
        elif load_text_image:
            if self.text_image_pkl_path:
                with open(self.text_image_pkl_path, 'rb') as f:
                    return pickle.load(f)
            else:
                print("No text_image_pkl_path")
        elif load_title_to_text:
            if self.title_to_text_pkl_path:
                with open(self.title_to_text_pkl_path, 'rb') as f:
                    return pickle.load(f)
            else:
                print("No title_to_text_pkl_path")
        else:
            print("Please specify the loading file！")

    def text_to_image(self, text):
        """
            给定文本出图片
            计算query 和 texts_source 的相似度，取最高的作为new_query 查询image
            到text_image_dict 读取图片名
            然后到images里面加载该图片然后返回
        """

        # 加载 text-imageName
        keys = list(self.text_image.keys())
        keys.insert(0, text)
        query_similarity = self.get_cosine_similarity(keys, get_image=True)
        key_index = query_similarity.argmax(dim=0)
        text = list(self.text_image.keys())[key_index]

        image = self.text_image[text] + '.jpg'
        if image in os.listdir(self.image_path):
            res = Image.open(self.image_path + '/' + image)
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
            texts_source[0] = query
        """
        if get_image:
            pkl = self.dict_text
        elif get_texts:
            pkl = self.text_embed
        else:
            # 计算query_embed
            pkl = {}
            embeddings = utils.get_embedding(self.model, texts[1:]).reshape(-1, 1536)
            for text, embed in zip(texts, embeddings):
                pkl[text] = embed

        query_embedding = utils.get_embedding(self.model, texts[0]).reshape(1, -1)
        texts_embeddings = np.array([value for value in pkl.values()])
        return cosine_similarity(query_embedding, torch.from_numpy(texts_embeddings))

    def retrieve_title(self, query_text, k):
        # compute cosine similarity between query_embed and embeddings
        embed_to_title = []
        texts = [query_text]
        embed_to_title = self.titles
        cosine_similarities = self.get_cosine_similarity(texts, get_texts=True).numpy().tolist()
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
        story = "凉宫春日的经典桥段如下:\n"

        count = 0

        final_selected = []
        print(selected_sample)
        for sample_topic in selected_sample:
            # find sample_answer in dictionary
            sample_story = self.title_to_text[sample_topic]

            sample_len = len(enc.encode(sample_story))
            # print(sample_topic, ' ' , sample_len)
            if sample_len + count > maxlen:
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
        max_len = self.max_len_history
        n = len(history_chat)
        if n == 0:
            return [], []

        if n != len(history_response):
            print('warning, unmatched history_char length, clean and start new chat')
            return [], []

        token_len = []
        for i in range(n):
            chat_len = len(enc.encode(history_chat[i]))
            res_len = len(enc.encode(history_response[i]))
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

        selected_sample = self.retrieve_title(new_query, 7)
        print("备选辅助：", selected_sample)
        story, selected_sample = self.organize_story_with_maxlen(selected_sample)

        ## TODO: visualize seletected sample later
        print('当前辅助sample:', selected_sample)

        messages = self.organize_message_langchain(story, history_chat, history_response, new_query)
        chat = ChatOpenAI(temperature=0)
        return_msg = chat(messages)

        response = return_msg.content

        return response

    def save_response(self, chat_history_tuple):
        with open(f"{self.save_path}/conversation_{time.time()}.txt", "w", encoding='utf-8') as file:
            for cha, res in chat_history_tuple:
                file.write(cha)
                file.write("\n---\n")
                file.write(res)
                file.write("\n---\n")

    def create_gradio(self):
        # from google.colab import drive
        # drive.mount(drive_path)
        with gr.Blocks() as demo:
            gr.Markdown(
                """
                ## Chat凉宫春日 ChatHaruhi
                项目地址 [https://github.com/LC1332/Chat-Haruhi-Suzumiya](https://github.com/LC1332/Chat-Haruhi-Suzumiya)
                骆驼项目地址 [https://github.com/LC1332/Luotuo-Chinese-LLM](https://github.com/LC1332/Luotuo-Chinese-LLM)
                此版本为图文版本，非最终版本，将上线更多功能，敬请期待
                """
            )
            image_input = gr.Textbox(visible=False)
            with gr.Row():
                chatbot = gr.Chatbot()
                image_output = gr.Image()
            role_name = gr.Textbox(label="角色名", placeholde="输入角色名")
            msg = gr.Textbox(label="输入")
            with gr.Row():
                clear = gr.Button("Clear")
                sub = gr.Button("Submit")
                image_button = gr.Button("给我一个图")

            def respond(role_name, user_message, chat_history):
                role_name = "阿虚" if role_name in ['', ' '] else role_name
                role_name = role_name[:10] if len(role_name) > 10 else role_name
                user_message = user_message[:200] if len(user_message) > 200 else user_message
                special_chars = [':', '：', '「', '」', '\n']
                for char in special_chars:
                    role_name = role_name.replace(char, 'x')
                    user_message = user_message.replace(char, ' ')

                input_message = role_name + ':「' + user_message + '」'
                bot_message = self.get_response(input_message, chat_history)
                chat_history.append((input_message, bot_message))
                self.save_response(chat_history)
                # time.sleep(1)
                return "", chat_history, bot_message

            msg.submit(respond, [role_name, msg, chatbot], [msg, chatbot, image_input])
            clear.click(lambda: None, None, chatbot, queue=False)
            sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input])
            image_button.click(self.text_to_image, inputs=image_input, outputs=image_output)

        demo.launch(debug=True, share=True)



