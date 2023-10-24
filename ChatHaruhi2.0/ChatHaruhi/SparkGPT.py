# SparkGPT.py
from . import SparkApi
#以下密钥信息从os环境获取
import os

appid = os.environ['APPID']
api_secret = os.environ['APISecret'] 
api_key = os.environ['APIKey']

from .BaseLLM import BaseLLM

    


class SparkGPT(BaseLLM):

    def __init__(self, model="Spark2.0"):
        super(SparkGPT,self).__init__()
        if model == "Spark2.0":
            self.domain = "generalv2"    # v2.0版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
        elif model == "Spark1.5":
            self.domain = "general"   # v1.5版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
        else:
            raise Exception("Unknown Spark model")

        self.messages = ""
        

    def initialize_message(self):
        self.messages = ""

    def ai_message(self, payload):
        self.messages = self.messages + "AI: " + payload  + "\n"

    def system_message(self, payload):
        self.messages = self.messages + "System: " + payload + "\n"

    def user_message(self, payload):
        self.messages = self.messages + "User: " + payload  + "\n"

    def get_response(self):
        # question = checklen(getText("user",Input))
        message_json = [{"role": "user", "content": self.messages}]
        SparkApi.answer =""
        SparkApi.main(appid,api_key,api_secret,self.Spark_url,self.domain,message_json)
        return SparkApi.answer
    
    def print_prompt(self):
        # print(type(self.messages))
        print(self.messages)
