import os
import argparse
import openai
import tiktoken
import torch
from scipy.spatial.distance import cosine
from transformers import AutoModel, AutoTokenizer
from argparse import Namespace
from langchain.chat_models import ChatOpenAI
import gradio as gr
import random
import time
from tqdm import tqdm
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
from text import Text

def download_models():
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                            init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)
    return model

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY2")
# openai.api_key = 'sk-DfFomLnch'  # 在这里输入你的OpenAI API Token

# os.environ["OPENAI_API_KEY"] = openai.api_key

folder_name = "Suzumiya"
current_directory = os.getcwd()
new_directory = os.path.join(current_directory, folder_name)


pkl_path = './pkl/texts.pkl'
text_image_pkl_path='./pkl/text_image.pkl'
dict_path = "../characters/haruhi/text_image_dict.txt"
dict_text_pkl_path = './pkl/dict_text.pkl'

image_path = "../characters/haruhi/images"
model = download_models()
text = Text("../characters/haruhi/texts", text_image_pkl_path=text_image_pkl_path,
                dict_text_pkl_path=dict_text_pkl_path, model=model, num_steps=50, pkl_path=pkl_path,
                dict_path=dict_path, image_path=image_path)

if not os.path.exists(new_directory):
    os.makedirs(new_directory)
    print(f"文件夹 '{folder_name}' 创建成功！")
else:
    print(f"文件夹 '{folder_name}' 已经存在。")

enc = tiktoken.get_encoding("cl100k_base")


class Run:
    def __init__(self, **params):
        """
            * 命令行参数的接入
            * 台词folder,记录台词
            * system prompt存成txt文件，支持切换
            * 支持设定max_len_story 和max_len_history
            * 支持设定save_path
            * 实现一个colab脚本，可以clone转换后的项目并运行，方便其他用户体验
        """
        self.text_folder = params['text_folder']
        # self.system_prompt = params['system_prompt']
        with open(params['system_prompt'], 'r') as f:
                    self.system_prompt = f.read()

        DEFAULT_GRADIO_HEADER = """
## Chat凉宫春日 ChatHaruhi
项目地址 [https://github.com/LC1332/Chat-Haruhi-Suzumiya](https://github.com/LC1332/Chat-Haruhi-Suzumiya)
骆驼项目地址 [https://github.com/LC1332/Luotuo-Chinese-LLM](https://github.com/LC1332/Luotuo-Chinese-LLM)
此版本为图文版本，非最终版本，将上线更多功能，敬请期待
        """

        if params['gradio_header'] != None and params["gradio_header"] != '':
            try:
                with open(params['gradio_header'], 'r') as f:
                            self.gradio_header = f.read()
            except:
                self.gradio_header = DEFAULT_GRADIO_HEADER
        else:
            self.gradio_header = DEFAULT_GRADIO_HEADER
        
        self.role_name_full = params['role_name_full']
        self.role_name_short = params['role_name_short']
        # self.role_name = params['role_name']
        self.max_len_story = params['max_len_story']
        self.max_len_history = params['max_len_history']
        self.save_path = params['save_path']
        
        self.titles, self.title_to_text = self.read_prompt_data()
        self.embeddings, self.embed_to_title = self.title_text_embedding(self.titles, self.title_to_text)
        # self.embeddings, self.embed_to_title = [], []
        # 一个封装 OpenAI 接口的函数，参数为 Prompt，返回对应结果

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
        for file in os.listdir(self.text_folder):
            if file.endswith('.txt'):
                title_name = file[:-4]
                titles.append(title_name)

                with open(os.path.join(self.text_folder, file), 'r') as f:
                    title_to_text[title_name] = f.read()

        return titles, title_to_text


    def get_embedding(self, text):
        tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
        model = download_models()
        if len(text) > 512:
            text = text[:512]
        texts = [text]
        # Tokenize the text
        inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
        # Extract the embeddings
        # Get the embeddings
        with torch.no_grad():
            embeddings = model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
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
        story = self.role_name_full + "的经典桥段如下:\n"

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
        chat = ChatOpenAI(temperature=0)
        return_msg = chat(messages)

        response = return_msg.content

        return response

    def save_response(self, chat_history_tuple):
        with open(f"{self.save_path}/conversation_{time.time()}.txt", "w") as file:
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
                self.gradio_header
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
                input_message = role_name + ':「' + user_message + '」'
                bot_message = self.get_response(input_message, chat_history)
                chat_history.append((input_message, bot_message))
                self.save_response(chat_history)
                # time.sleep(1)
                return "" , chat_history, bot_message

            msg.submit(respond, [role_name, msg, chatbot], [msg, chatbot, image_input])
            clear.click(lambda: None, None, chatbot, queue=False)
            sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input])
            # with gr.Tab("text_to_text"):
            #     text_input = gr.Textbox()
            #     text_output = gr.Textbox()
            #     text_button = gr.Button('begin')

            # text_button.click(text.text_to_text, inputs=text_input, outputs=text_output)
            


            # with gr.Tab("text_to_iamge"):
                # with gr.Row():
                    # image_input = gr.Textbox()
                    # image_output = gr.Image()
            # image_button = gr.Button("给我一个图")
        
            image_button.click(text.text_to_image, inputs=image_input, outputs=image_output)

        demo.launch(debug=True,share=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="-----[Chat凉宫春日]-----")
    parser.add_argument("--role_name_full", default="凉宫春日", help="完整的角色名")
    parser.add_argument("--role_name_short", default="春日", help="对话时使用的缩略角色名")
    parser.add_argument("--gradio_header", default = "", help="gradio header file")
    parser.add_argument("--text_folder", default="../characters/haruhi/texts_source", help="text folder")
    parser.add_argument("--system_prompt", default="../characters/haruhi/system_prompt.txt", help="store system_prompt")
    parser.add_argument("--max_len_story", default=1500, type=int)
    parser.add_argument("--max_len_history", default=1200, type=int)
    # parser.add_argument("--save_path", default="/content/drive/MyDrive/GPTData/Haruhi-Lulu/")
    parser.add_argument("--save_path", default=os.getcwd()+"/Suzumiya")
    options = parser.parse_args()
    params = {
        "role_name_full": options.role_name_full, # "Haruhi
        "role_name_short": options.role_name_short,
        "gradio_header": options.gradio_header,
        "text_folder": options.text_folder,
        "system_prompt": options.system_prompt,
        "max_len_story": options.max_len_story,
        "max_len_history": options.max_len_history,
        "save_path": options.save_path
    }
    run = Run(**params)
    run.create_gradio()

    
    # history_chat = []
    # history_response = []
    # chat_timer = 5
    # new_query = '鲁鲁:你好我是新同学鲁鲁'

    # query_embed = run.get_embedding(new_query)
    # titles, title_to_text = run.read_prompt_data()
    # embeddings, embed_to_title = run.title_text_embedding(titles, title_to_text)
    # selected_sample = run.retrieve_title(query_embed, embeddings, embed_to_title, 7)

    # print('限制长度之前:', selected_sample)

    # story, selected_sample = run.organize_story_with_maxlen(selected_sample)

    # print('当前辅助sample:', selected_sample)

    # messages = run.organize_message(story, history_chat, history_response, new_query)

    # response = run.get_completion_from_messages(messages)

    # print(response)

    # history_chat.append(new_query)
    # history_response.append(response)

    # history_chat, history_response = run.keep_tail(history_chat, history_response)
    # print(history_chat, history_response)