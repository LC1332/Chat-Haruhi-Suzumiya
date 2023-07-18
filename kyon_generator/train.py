'''
FILE_NAME: Train.py
First Edition
Edited by 睡觉鱼, Jul 18 2023
'''
%pip install -qU protobuf transformers==4.30.2 cpm_kernels torch>=2.0 mdtex2html sentencepiece accelerate
%pip install -qU datasets loralib
%pip install -qU jupyter
%pip install -qU git+https://github.com/huggingface/peft.git

from transformers import AutoTokenizer, AutoModel
from datasets import load_dataset
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model
from transformers import Trainer, TrainingArguments
from huggingface_hub import login

DATA_PATH = 'train_data.csv'
HF_TOKEN = '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'

login(token= HF_TOKEN)

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()

train_dataset = load_dataset('csv',data_files= DATA_PATH)
def preprocess_dialogue(example):
    prompt = example["context"]
    target = example["target"]
    prompt_ids = tokenizer.encode(prompt,truncation=True,add_special_tokens=True)
    target_ids = tokenizer.encode(target,truncation=True,add_special_tokens=False)
    input_ids = prompt_ids + target_ids
    return {"input_ids": input_ids, "seq_len": len(prompt_ids)}

model_inputs = train_dataset.map(preprocess_dialogue)

for param in model.parameters():
  param.requires_grad = False  # freeze the model - train adapters later
  if param.ndim == 1:
    # cast the small parameters (e.g. layernorm) to fp32 for stability
    param.data = param.data.to(torch.float32)

model.gradient_checkpointing_enable()  # reduce number of stored activations
model.enable_input_require_grads()
model.is_parallelizable = True
model.model_parallel = True

config = LoraConfig(
    r=16,
    lora_alpha=32,
    inference_mode=False,
    lora_dropout=0.05,
    #bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)

#以下Part还没有完全搞懂，大概是参考作者写的统一字长的手段，大佬们可以尝试修改
def data_collator(features: list) -> dict:
    len_ids = [len(feature["input_ids"]) for feature in features]
    longest = max(len_ids)
    input_ids = []
    labels_list = []
    for ids_l, feature in sorted(zip(len_ids, features), key=lambda x: -x[0]):
        ids = feature["input_ids"]
        seq_len = feature["seq_len"]
        labels = (
            [-100] * (seq_len - 1) + ids[(seq_len - 1) :] + [-100] * (longest - ids_l)
        )
        ids = ids + [tokenizer.pad_token_id] * (longest - ids_l)
        _ids = torch.LongTensor(ids)
        labels_list.append(torch.LongTensor(labels))
        input_ids.append(_ids)
    input_ids = torch.stack(input_ids)
    labels = torch.stack(labels_list)
    return {
        "input_ids": input_ids,
        "labels": labels,
    }

class ModifiedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        return model(
            input_ids=inputs["input_ids"],
            labels=inputs["labels"],
        ).loss

training_args = TrainingArguments(
    num_train_epochs = 2,
    max_steps = -1,
    evaluation_strategy = "no",
    gradient_accumulation_steps = 1,
    group_by_length=False,
    save_strategy = "steps",
    save_steps = 500,
    output_dir = 'output',
    remove_unused_columns = False,
    per_device_train_batch_size = 32,
    per_device_eval_batch_size = 32,
    learning_rate = 1e-4,
    fp16 = True,
    seed=2023,
    data_seed=2023
)

trainer = ModifiedTrainer(
    model=model,
    train_dataset=model_inputs['train'],
    #eval_dataset=model_inputs['test'],
    args=training_args,
    data_collator=data_collator,
)
trainer.train()

model.push_to_hub("Jyshen/Chat_Suzumiya_GLM2LoRA", use_auth_token=True)