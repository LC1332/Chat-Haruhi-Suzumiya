import configparser
from ChatGPT2 import ChatGPT
from checkCharacter import checkCharacter

class ChatPerson:
    def __init__(self, **params):
        pass
        self.configuration = {}
        if not params.keys():
            print("载入默认角色")
            self.readConfig()
            check_result, error_code, error_msg = self.checkCharacter()
            if not check_result:
                print(error_msg)
                return error_code
            self.loadCharacter()
        else:
            print("载入新建角色")
            check_result, error_code, error_msg = self.checkCharacter()
            if not check_result:
                print(error_msg)
                return error_code

    def checkCharacter(self):
        pass
        return checkCharacter(self.configuration)
        
        
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
        # print(self.configuration)
        self.ChatGPT = ChatGPT(self.configuration)
        self.ChatGPT.read_data()

    def getResponse(self, user_message, chat_history_tuple):
        pass
        if (self.configuration["gpt"]):
            print("正在获取GPT回复")
            response = self.ChatGPT.get_response(user_message, chat_history_tuple)
            print("获取回复完毕")
            return response
        
    def switchCharacter(self, characterName):
        pass
        print("正在切换角色")
        self.readConfig(character=characterName)
        check_result, error_code, error_msg = self.checkCharacter()
        if not check_result:
                print(error_msg)
                return error_code
        self.loadCharacter()
        print("角色切换完成")

# person = ChatPerson()
# person.switchCharacter("liyunlong")
# print(person.configuration)
