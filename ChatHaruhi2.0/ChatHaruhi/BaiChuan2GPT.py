import torch
from .BaseLLM import BaseLLM
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from peft import PeftModel

tokenizer_BaiChuan = None
model_BaiChuan = None

def initialize_BaiChuan2LORA():
    global model_BaiChuan, tokenizer_BaiChuan
    
    if model_BaiChuan is None:
        model_BaiChuan = AutoModelForCausalLM.from_pretrained(
            "baichuan-inc/Baichuan2-13B-Chat",
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        model_BaiChuan = PeftModel.from_pretrained(
            model_BaiChuan,
            "silk-road/Chat-Haruhi-Fusion_Baichuan2_13B"
        )
        model_BaiChuan.generation_config = GenerationConfig.from_pretrained(
            "baichuan-inc/Baichuan2-13B-Chat"
        )
    
    if tokenizer_BaiChuan is None:
        tokenizer_BaiChuan =  AutoTokenizer.from_pretrained(
            "baichuan-inc/Baichuan2-13B-Chat", 
            use_fast=True, 
            trust_remote_code=True
        )
    
    return model_BaiChuan, tokenizer_BaiChuan

def BaiChuan_tokenizer(text):
    return len(tokenizer_BaiChuan.encode(text))

class BaiChuan2GPT(BaseLLM):
    def __init__(self, model = "haruhi-fusion-baichuan"):
        super(BaiChuan2GPT, self).__init__()
        if model == "baichuan2-13b":
            self.tokenizer = AutoTokenizer.from_pretrained(
                "baichuan-inc/Baichuan2-13B-Chat", 
                use_fast=True, 
                trust_remote_code=True
            ),
            self.model = AutoModelForCausalLM.from_pretrained(
                "baichuan-inc/Baichuan2-13B-Chat",
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
            )
            self.model.generation_config = GenerationConfig.from_pretrained(
                "baichuan-inc/Baichuan2-13B-Chat"
            )
        elif model == "haruhi-fusion-baichuan":
            self.model, self.tokenizer = initialize_BaiChuan2LORA()
        else:
            raise Exception("Unknown BaiChuan Model! Currently supported: [BaiChuan2-13B, haruhi-fusion-baichuan]")
        self.messages = []

    def initialize_message(self):
        self.messages = []

    def ai_message(self, payload):
        self.messages.append({"role": "assistant", "content": payload})

    def system_message(self, payload):
        self.messages.append({"role": "system", "content": payload})

    def user_message(self, payload):
        self.messages.append({"role": "user", "content": payload})

    def get_response(self):
        with torch.no_grad():
            response = self.model.chat(self.tokenizer, self.messages)
        return response
        
    def print_prompt(self):
        print(type(self.messages))
        print(self.messages)