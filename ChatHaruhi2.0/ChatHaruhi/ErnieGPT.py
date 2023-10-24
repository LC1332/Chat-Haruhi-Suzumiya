# ErnieGPT.py
import erniebot 
#以下密钥信息从os环境获取
import os
import copy

# appid = os.environ['APPID']
# api_secret = os.environ['APISecret'] 
# api_key = os.environ['APIKey']
erniebot.api_type = os.environ["APIType"]
erniebot.access_token = os.environ["ErnieAccess"]


from .BaseLLM import BaseLLM

    


class ErnieGPT(BaseLLM):

    def __init__(self,model="ernie-bot"):
        super(ErnieGPT,self).__init__()
        if model not in ["ernie-bot", "ernie-bot-turbo", "ernie-vilg-v2", "ernie-text-embedding"]:
            raise Exception("Unknown Ernie model")
        # SparkApi.answer =""
        self.messages = []
        

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
        chat_messages = copy.deepcopy(self.messages)
        lines = chat_messages[-1]["content"].split('\n')
        lines.insert(-1, '请请模仿上述经典桥段进行回复\n')
        chat_messages[-1]["content"] = '\n'.join(lines)
        # chat_messages[-1]["content"] = "请请模仿上述经典桥段进行回复\n" + chat_messages[-1]["content"] 
        response = erniebot.ChatCompletion.create(model='ernie-bot', messages=chat_messages)
        # message_json = [{"role": "user", "content": self.messages}]
        # SparkApi.answer =""
        # SparkApi.main(appid,api_key,api_secret,self.Spark_url,self.domain,message_json)
        return response["result"]
    
    def print_prompt(self):
        for message in self.messages:
            print(f"{message['role']}: {message['content']}")
