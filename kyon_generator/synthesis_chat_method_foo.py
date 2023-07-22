# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个程序是一个synthesis_chat method的简单例子
from typing import List, Dict, Tuple
import numpy as np
from tqdm import tqdm
import random
from configparser import ConfigParser
import os
import openai
from joblib import Parallel, delayed
from langchain.chat_models import ChatOpenAI
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

chatModel = ChatOpenAI(temperature=0)

'''
[Synthesis]
OPENAI_API_KEY = sk
stop_words = 春日,阿虚,凉宫,凉宫春日
input1 = 阿虚:「我无意中听到一件事。」
    春日:「反正不会是什么重要的事。」
output1 = {"Entity": ["不重要的事","阿虚","春日"]}
input2 = 阿虚:「你为什么要剪头发啊？」
    春日:「没什么理由，就是想剪了而已。」
output2 = {"Entity": ["剪头发","没什么理由"]}
KEYWORD_PROMPT = 提取反引号文本中的关键字Entity，以list的形式输出在一个json中。
TANSFER_PROMPT = 根据keywords的内容补全text
    text为对于凉宫春日剧情的一些讨论问题，role不可以是春日或者凉宫春日
    role可以是阿虚、朝比奈、老师等凉宫春日中，非春日的其他角色
    role也可以是任意其他动漫中的角色
    用一致性的语言风格，根据每行中的json内容，根据keywords中的关键字，补全text的内容。
'''

keyword_list = []
role_list =[]

def generate(input_file, output_file, additional_config=None):
    """
    核心函数，使用foo方法将input_file生成增广的jsonl文件保存到output_file
    """
    with open(input_file, 'r',encoding = 'utf-8') as f:
        # 读取input_file的内容
        data = f.read()
    
    # 获取配置
    config = ConfigParser()
    config.read(additional_config)
    os.environ["OPENAI_API_KEY"] = config['Synthesis']['OPENAI_API_KEY']
    stop_words = config['Synthesis']['stop_words'].split(',')
    input1 = config['Synthesis']['input1']
    output1 = config['Synthesis']['output1']
    input2 = config['Synthesis']['input2']
    output2 = config['Synthesis']['output2']
    KEYWORD_PROMPT = config['Synthesis']['KEYWORD_PROMPT']
    TANSFER_PROMPT = config['Synthesis']['TANSFER_PROMPT']
 
    # 多线程提取全部关键词
    def extract_keywords( new_query ):
        messages = [
            SystemMessage(content=KEYWORD_PROMPT),
            HumanMessage(content=input1),
            AIMessage(content=output1),
            HumanMessage(content=input2),
            AIMessage(content=output2)
        ]
        messages.append(HumanMessage(content=new_query['text']))
        return_msg = chatModel(messages)
        response = return_msg.content
        new_query['keywords'] = response['Entity']

    # 并行或串行处理数据
    multiply_process = True  # 在测试的时候可以改成False
    if multiply_process:  # 并行运行
        Parallel(n_jobs=max(os.cpu_count() - 1, 1))(
                delayed(extract_keywords)(item)
                for item in tqdm(data)
                )
    else:  # 串行运行
        for item in tqdm(data):
            extract_keywords(item)
 

    
    # foo_sample, foo_input
    n = len(data)
    sel_all = random.sample(range(0, n), 20)
    sel_sample = sel_all[:10]
    sel_input = sel_all[10:]
    sample_input, sample_output, sample_keywords = foo_sample(sel_sample)
    query_input = foo_input(sel_input, sample_keywords)

    # 去除停用关键词

    data = remove_stop_words(data, stop_words)
    sample_keywords = remove_stop_words(sample_keywords, stop_words)


    # 用keyword生成
    def generate_with_keywords( sample_input, sample_output, query_input ):
        div_k = 4
        input1 = list_to_string( sample_input[:div_k] )
        output1 = list_to_string( sample_output[:div_k] )
        input2 = list_to_string( sample_input[div_k:] )
        output2 = list_to_string( sample_output[div_k:] )

        query = list_to_string(query_input)

        messages = [
            SystemMessage(content=TANSFER_PROMPT),
            HumanMessage(content=input1),
            AIMessage(content=output1),
            HumanMessage(content=input2),
            AIMessage(content=output2),
            HumanMessage(content=query)
        ]
        return_msg = chatModel(messages)
        return return_msg.content   
    

    # 。。。没完全看懂，先抄了，并行后面再加
    data_story = DataLoader(sample_keywords, 10)
    data_chat_as_story = DataLoader(data, 10)
    data_chat = DataLoader(data, 10)


    batch_size = 10
    for iter_time in tqdm(range(700),desc='autoGenerating'):

        chat_data = []

        for _ in range(batch_size):
            chat_data.append( data_chat.get_data() )

        sample_input, sample_output, sample_keywords = organize_samples(chat_data)

        #这里我们还要组织query_input

        query_input = []

        for input in sample_input:
            target_n = len( input['keywords'] )
            target_n = max(2, target_n )

            count_time = 0
            max_len = -999
            max_len_plan = []

            while count_time < 15:
                #随机抽取一个story的keyword
                count_time = count_time + 1
                if iter_time % 2 == 0:
                    story_keyword = data_story.get_data()
                else:
                    story_keyword = data_chat_as_story.get_data()

                filtered_keyword = [w for w in story_keyword["keywords"] if w not in sample_keywords]
                if len(filtered_keyword) >= target_n:
                    story_keyword['keywords'] = random.sample(filtered_keyword, min(target_n, len(filtered_keyword)))
                    break
                else:
                    if len(filtered_keyword)>max_len:
                        max_len = len(filtered_keyword)
                        # story_keyword['keywords'] = filtered_keyword
                        max_len_plan = filtered_keyword.copy()

            if len(story_keyword['keywords'] ) < target_n:
                story_keyword['keywords'] = max_len_plan
                # print('use max len plan ', target_n - len(story_keyword['keywords'] ))
            query_input.append( {'keywords':story_keyword['keywords']} )

            for keyword in story_keyword['keywords']:
                sample_keywords.append(keyword)

        # response = generate_with_keywords( sample_input, sample_output, query_input )
        try:
            response = generate_with_keywords(sample_input, sample_output, query_input)
        except Exception as e:
            print(f"An error occurred while running the script: {e}")
            break


    #写回文件？new一个data，然后append each response？
    with open(output_file, 'w') as f:
        # 将增广数据写入output_file
        f.write(data)



def foo_sample(sel_sample):
    sel_chat_data = [chat_datas[i] for i in sel_sample]

    sample_input, sample_output, sample_keywords = organize_samples(sel_chat_data)

    return sample_input, sample_output, sample_keywords
    

def foo_input(sel_input, sample_keywords):
    sel_chat_data = [chat_datas[i] for i in sel_input]

    sample_input, _ , _ = organize_samples(sel_chat_data)

    return sample_input


def list_to_string(lst):
    result = ''
    for item in lst:
        result += str(item) + '\n'
    return result

def remove_stop_words(data, stop_words):
    stop_words_set = set(stop_words) # 转换为set方便查找
    for item in data:
        item["keywords"] = [w for w in item["keywords"] if w not in stop_words_set]
    return data

def organize_samples(sel_chat_datas: List[Dict[str, str]]) -> Tuple[List[Dict], List[Dict], List[str]]:
    sample_input = []
    sample_output = []
    all_keywords = set()
    for element in sel_chat_datas:
        keywords = element['keywords']  # [kw for kw in element['keywords'] if kw not in stop_words]
        np.random.shuffle(keywords)
        sample_input.append({'keywords': keywords})
        output_element = {
            'keywords': keywords,
            'role': element['role'],
            'text': element['text'],
        }
        sample_output.append(output_element)
        for kw in keywords:
            all_keywords.add(kw)
    return sample_input, sample_output, list(all_keywords)

class DataLoader:
    def __init__(self, data, k=10):
        self.data = data
        self.n = len(data)
        self.k = k
        self.current_id = 0
        self.shuffle_id = list(range(self.n))
        random.shuffle(self.shuffle_id)
        self.previous_tail = self.shuffle_id[-self.k+1:]

    def shuffle(self):
        if self.n <= 2 * self.k:
            random.shuffle(self.shuffle_id)
        else:
            random.shuffle(self.shuffle_id)
            head = self.shuffle_id[:self.k-1]
            flag = True
            count = 0

            min_ovlp_num = 999
            min_ovlp_plan = []

            while count < 10 and flag == True:
                count = count + 1
                inverse_flag = False
                ovlp_num = 0
                for id in head:
                    if id in self.previous_tail:
                        ovlp_num = ovlp_num + 1
                        inverse_flag = True

                if ovlp_num < min_ovlp_num:
                    min_ovlp_num = ovlp_num
                    min_ovlp_plan = self.shuffle_id.copy()

                if False == inverse_flag:
                    flag = False
                    break

                random.shuffle(self.shuffle_id)
                head = self.shuffle_id[:self.k-1]

            # print('shuffle test time ', count, ' min ovlp = ', min_ovlp_num)

            if min_ovlp_num > 0:
                self.shuffle_id = min_ovlp_plan

            head = self.shuffle_id[self.k-1:]
            tail = self.shuffle_id[-self.k+1:]

            self.shuffle_id = head + self.shuffle_id[:self.k-1] + tail
            random.shuffle(self.shuffle_id)
            self.previous_tail = tail

    def get_data(self):
        if self.current_id >= self.n:
            self.shuffle()
            self.current_id = 0
        data = self.data[self.shuffle_id[self.current_id]]
        self.current_id += 1
        return data

        
# if __name__ == '__main__':
#     input_file = r"D:\Misc\Chat-Haruhi-Suzumiya\Haruhi_first_merge_res.jsonl"
#     output_file = r"D:\Misc\Chat-Haruhi-Suzumiya\Haruhi_first_merge_res_out.jsonl"
#     config_file = r"D:\Misc\Chat-Haruhi-Suzumiya\config.ini"
#     generate(input_file,output_file,config_file)