import torch 
from .BaseLLM import BaseLLM
from transformers import AutoTokenizer, AutoModel
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

tokenizer_qwen = None
model_qwen = None



def initialize_Qwen2LORA(model):
    global model_qwen, tokenizer_qwen

    if model_qwen is None:
        model_qwen = AutoModelForCausalLM.from_pretrained(
            model,
            device_map="auto",
            trust_remote_code=True
        )
        model_qwen = model_qwen.eval()
        # model_qwen = PeftModel.from_pretrained(
        #     model_qwen,
        #     "silk-road/Chat-Haruhi-Fusion_B"
        # )

    if tokenizer_qwen is None:
        tokenizer_qwen = AutoTokenizer.from_pretrained(
            model, 
            # use_fast=True,
            trust_remote_code=True
        )

    return model_qwen, tokenizer_qwen

def Qwen_tokenizer(text):
    return len(tokenizer_qwen.encode(text))

class Qwen118k2GPT(BaseLLM):
    def __init__(self, model):
        super(Qwen118k2GPT, self).__init__()
        global model_qwen, tokenizer_qwen
        if model == "Qwen/Qwen-1_8B-Chat":
            tokenizer_qwen = AutoTokenizer.from_pretrained(
                "Qwen/Qwen-1_8B-Chat", 
                trust_remote_code=True
            )
            model_qwen = AutoModelForCausalLM.from_pretrained(
                "Qwen/Qwen-1_8B-Chat", 
                device_map="auto", 
                trust_remote_code=True
            ).eval()
            self.model = model_qwen
            self.tokenizer = tokenizer_qwen
        elif "silk-road/" in model :
            self.model, self.tokenizer = initialize_Qwen2LORA(model)
        else:
            raise Exception("Unknown Qwen model")
        self.messages = ""

    def initialize_message(self):
        self.messages = ""

    def ai_message(self, payload):
        self.messages = "AI: " +  self.messages + "\n " + payload 

    def system_message(self, payload):
        self.messages = "SYSTEM PROMPT: " + self.messages + "\n " + payload 

    def user_message(self, payload):
        self.messages = "User: " + self.messages + "\n " + payload 

    def get_response(self):
        with torch.no_grad():
            response, history = self.model.chat(self.tokenizer, self.messages, history=[])
            # print(response)
        return response
        
    def print_prompt(self):
        print(type(self.messages))
        print(self.messages)

    
