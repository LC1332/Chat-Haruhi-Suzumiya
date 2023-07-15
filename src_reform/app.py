import configparser
from ChatGPT import ChatGPT
from checkCharacter import checkCharacter

class ChatPerson:
    def __init__(self, **params):
        pass
        self.configuration = {}
        self.sections = [] # config中的角色区块
        if not params.keys():
            print("载入默认角色")
            self.readConfig()
            check_result, error_code, error_msg = self.checkCharacter()
            if not check_result:
                print(error_msg)
                # return error_code
                # raise EOFError(error_msg)
            self.loadCharacter()
        else:
            print("载入新建角色")
            check_result, error_code, error_msg = self.checkCharacter()
            if not check_result:
                print(error_msg)
                # return error_code
                # raise Error

    def checkCharacter(self):
        pass
        return checkCharacter(self.configuration)
        
        
    def readConfig(self, character="DEFAULT"):
        pass
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.sections = self.config.sections()
        items = self.config.items(character)
        print(f"正在加载: {character} 角色")
        for key, value in items:
            self.configuration[key]=value
        print("配置文件载入完成")

    def loadCharacter(self):
        pass
        if (self.configuration["gpt"].lower == "true"):
            print("选择使用GPT作为语言模型")
            self.initGPT()
        if (self.configuration["gpt"].lower == "false"):
            print("选择使用本地模型作为语言模型")
            self.initLocalLLM()

    def getCharacters(self):
        pass
        r_list = []
        for character in self.sections:
            items = self.config.items(character)
            r_list.append(character)
            for key, value in items:
                if key == "local_model" and not bool(value):
                    r_list.append(f"{character}_local")    
        return r_list

    def initLocalLLM(self):
        pass
        

    def initGPT(self):
        pass
        print("正在载入角色GPT所需资源")
        # print(self.configuration)
        self.ChatGPT = ChatGPT(self.configuration)
        self.ChatGPT.preload()

    def getResponse(self, user_message, chat_history_tuple):
        pass
        if (self.configuration["gpt"].lower == "true"):
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
# person.getCharacters()
# person.switchCharacter("liyunlong")
# print(person.configuration)
