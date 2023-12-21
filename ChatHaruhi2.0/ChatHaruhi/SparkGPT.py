# SparkGPT.py
from . import SparkApi
#以下密钥信息从os环境获取
import os

appid = os.environ['APPID']
api_secret = os.environ['APISecret'] 
api_key = os.environ['APIKey']

from .BaseLLM import BaseLLM

    


class SparkGPT(BaseLLM):

    def __init__(self, model="Spark3.0"):
        super(SparkGPT,self).__init__()
        self.model_type = model
        self.messages = []
        if self.model_type == "Spark2.0":
            self.domain = "generalv2"    # v2.0版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
        elif self.model_type == "Spark1.5":
            self.domain = "general"   # v1.5版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
        elif self.model_type == "Spark3.0":
            self.domain = "generalv3"   # v3.0版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
        else:
            raise Exception("Unknown Spark model")
    
    def initialize_message(self):
        self.messages = []

    def ai_message(self, payload):
        if len(self.messages) == 0:
            self.user_message("请根据我的要求进行角色扮演:")
        elif len(self.messages) % 2 == 1:
            self.messages.append({"role":"assistant","content":payload})
        elif len(self.messages)% 2 == 0:
            self.messages[-1]["content"] += "\n"+ payload

    def system_message(self, payload):
        
        self.messages.append({"role":"user","content":payload}) 
        

    def user_message(self, payload):
        if len(self.messages) % 2 == 0:
            self.messages.append({"role":"user","content":payload})
            # self.messages[-1]["content"] += 
        elif len(self.messages)% 2 == 1:
            self.messages[-1]["content"] += "\n"+ payload

    def get_response(self):
        # question = checklen(getText("user",Input))
        SparkApi.answer =""
        if self.model_type == "Spark2.0":
            self.domain = "generalv2"    # v2.0版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
        elif self.model_type == "Spark1.5":
            self.domain = "general"   # v1.5版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
        elif self.model_type == "Spark3.0":
            self.domain = "generalv3"   # v3.0版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
        else:
            raise Exception("Unknown Spark model")
        SparkApi.main(appid,api_key,api_secret,self.Spark_url,self.domain,self.messages)
        return SparkApi.answer
    
    def print_prompt(self):
        for message in self.messages:
            print(f"{message['role']}: {message['content']}")
