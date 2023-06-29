import configparser
from ChatGPT import ChatGPT

class ChatPerson:
    def __init__(self, **params):
        pass
        self.configuration = {}
        if not params.keys():
            print("载入默认角色")
            self.readConfig()
            self.checkCharacter()
            self.loadCharacter()
        else:
            print("载入新建角色")
            checkCharacter()

    def checkCharacter(self):
        pass
        print("检查角色文件是否缺失")
        
    def readConfig(self, character="DEFAULT"):
        pass
        print("载入配置文件")
        config = configparser.ConfigParser()
        config.read('config.ini')
        sections = config.sections()
        items = config.items(character)
        print(f"正在加载: {character} 角色")
        for key, value in items:
            self.configuration[key]=value
        print("配置文件载入完成")

    def loadCharacter(self):
        pass
        if (self.configuration["gpt"]):
            print("选择使用GPT作为语言模型")
            self.initGPT()

    def getFunction(self):
        pass

    def initLocalLLM(self):
        pass

    def initGPT(self):
        pass
        print("正在载入角色GPT所需资源")
        self.ChatGPT = ChatGPT(self.configuration)

    def getResponse(self, user_message, chat_history_tuple):
        pass
        if (self.configuration["gpt"]):
            print("正在获取GPT回复")
            response = self.ChatGPT.get_response(user_message, chat_history_tuple)
            print("获取回复完毕")
            return response
            
        
# ChatPerson()