# ChatHaruhi: Reviving Anime Character in Reality via Large Language Model
#
# ChatHaruhi 2.0, built by Cheng Li and Weishi Mi
#
# chengli.thu@gmail.com, mws22@mails.tsinghua.edu.cn
# 
# Weishi Mi is a second-year graduate student at Tsinghua University, majoring in computer science.
# Weishi Mi is pursuing a job or a PhD position, which who will be available next year
# 
# homepage https://github.com/LC1332/Chat-Haruhi-Suzumiya
# 
# ChatHaruhi is a chatbot that can revive anime characters in reality.
# the 2.0 version was built by Cheng Li and Weishi Mi.
# 
# Please cite our paper if you use this code for research: 
#
# @misc{li2023chatharuhi,
#       title={ChatHaruhi: Reviving Anime Character in Reality via Large Language Model}, 
#       author={Cheng Li and Ziang Leng and Chenxi Yan and Junyi Shen and Hao Wang and Weishi MI and Yaying Fei and Xiaoyang Feng and Song Yan and HaoSheng Wang and Linkang Zhan and Yaokai Jia and Pingyu Wu and Haozhen Sun},
#       year={2023},
#       eprint={2308.09597},
#       archivePrefix={arXiv},
#       primaryClass={cs.CL}
# }


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
from .BaseLLM import BaseLLM

class LangChainGPT(BaseLLM):

    def __init__(self, model="gpt-3.5-turbo"):
        super(LangChainGPT,self).__init__()
        self.chat = ChatOpenAI(model=model)
        self.messages = []

    def initialize_message(self):
        self.messages = []

    def ai_message(self, payload):
        self.messages.append(AIMessage(content = payload))

    def system_message(self, payload):
        self.messages.append(SystemMessage(content = payload))

    def user_message(self, payload):
        self.messages.append(HumanMessage(content = payload))

    def get_response(self):
        response = self.chat(self.messages)
        return response.content
    
    def print_prompt(self):
        for message in self.messages:
            print(message)
