import torch 
from .BaseLLM import BaseLLM
from transformers import AutoTokenizer, AutoModel
from peft import PeftModel

tokenizer_GLM = None
model_GLM = None

def initialize_GLM2LORA():
    global model_GLM, tokenizer_GLM

    if model_GLM is None:
        model_GLM = AutoModel.from_pretrained(
            "THUDM/chatglm2-6b",
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        model_GLM = PeftModel.from_pretrained(
            model_GLM,
            "silk-road/Chat-Haruhi-Fusion_B"
        )

    if tokenizer_GLM is None:
        tokenizer_GLM = AutoTokenizer.from_pretrained(
            "THUDM/chatglm2-6b", 
            use_fast=True,
            trust_remote_code=True
        )

    return model_GLM, tokenizer_GLM

def GLM_tokenizer(text):
    return len(tokenizer_GLM.encode(text))

class ChatGLM2GPT(BaseLLM):
    def __init__(self, model = "haruhi-fusion"):
        super(ChatGLM2GPT, self).__init__()
        if model == "glm2-6b":
            self.tokenizer = AutoTokenizer.from_pretrained(
                "THUDM/chatglm2-6b", 
                use_fast=True,
                trust_remote_code=True
            )
            self.model = AutoModel.from_pretrained(
                "THUDM/chatglm2-6b",
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
        if model == "haruhi-fusion":
            self.model, self.tokenizer = initialize_GLM2LORA()
        else:
            raise Exception("Unknown GLM model")
        self.messages = ""

    def initialize_message(self):
        self.messages = ""

    def ai_message(self, payload):
        self.messages = self.messages + "\n " + payload 

    def system_message(self, payload):
        self.messages = self.messages + "\n " + payload 

    def user_message(self, payload):
        self.messages = self.messages + "\n " + payload 

    def get_response(self):
        with torch.no_grad():
            response, history = self.model.chat(self.tokenizer, self.messages, history=[])
            # print(response)
        return response
        
    def print_prompt(self):
        print(type(self.messages))
        print(self.messages)

    