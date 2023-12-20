import torch
from .BaseLLM import BaseLLM
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from peft import PeftModel

tokenizer_Llama = AutoTokenizer.from_pretrained("../../../llm/Llama-2-7b-hf/",
                                                use_fast=True, trust_remote_code=True)
model_Llama = None


def initialize_Llama2LORA():
    global model_Llama, tokenizer_Llama

    if model_Llama is None:
        model_Llama = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-2-7b",
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        model_Llama = PeftModel.from_pretrained(
            model_Llama,
            "silk-road/RoleLLM_Llama2_7B"
        )
        model_Llama.generation_config = GenerationConfig.from_pretrained(
            "meta-llama/Llama-2-7b"
        )

    if tokenizer_Llama is None:
        tokenizer_Llama = AutoTokenizer.from_pretrained(
            "meta-llama/Llama-2-7b",
            use_fast=True,
            trust_remote_code=True
        )

    return model_Llama, tokenizer_Llama


def Llama_tokenizer(text):
    return len(tokenizer_Llama.encode(text))


class Llama2GPT(BaseLLM):
    def __init__(self, model="roleLLM-llama"):
        super(Llama2GPT, self).__init__()
        if model == "llama2-7b":
            self.tokenizer = AutoTokenizer.from_pretrained(
                "meta-llama/Llama-2-7b",
                use_fast=True,
                trust_remote_code=True
            ),
            self.model = AutoModelForCausalLM.from_pretrained(
                "meta-llama/Llama-2-7b",
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
            )
            self.model.generation_config = GenerationConfig.from_pretrained(
                "meta-llama/Llama-2-7b"
            )
        elif model == "roleLLM-llama":
            # self.model, self.tokenizer = initialize_Llama2LORA()
            # 改回去
            self.model = None
            self.tokenizer = AutoTokenizer.from_pretrained(
                "../../../llm/Llama-2-7b-hf/",
                use_fast=True, trust_remote_code=True)
        else:
            raise Exception("Unknown Llama Model! Currently supported: [Llama2-7B, roleLLM-llama]")
        self.messages = ""

    def initialize_message(self):
        self.messages = ""

    # 待修改
    def ai_message(self, payload):
        self.messages = self.messages + "\n" + payload

    # 待修改
    def system_message(self, payload):
        self.messages = self.messages + "\n" + payload

    # 待修改
    def user_message(self, payload):
        self.messages = self.messages + "\n" + payload

    def get_response(self):
        with torch.no_grad():
            response = self.model.chat(self.tokenizer, self.messages)
        return response

    def print_prompt(self):
        print(type(self.messages))
        print(self.messages)