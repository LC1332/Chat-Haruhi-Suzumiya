'''
FILE_NAME: Train.py
GLM2-LoRA Edition
Edited by 冷子昂，睡觉鱼, Aug 14 2023
'''

# %pip install -qU protobuf transformers==4.30.2 cpm_kernels torch>=2.0 mdtex2html sentencepiece accelerate
# %pip install -qU datasets loralib
# %pip install -qU jupyter
# %pip install -qU git+https://github.com/huggingface/peft.git
import json
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import os
import jsonlines
from torch.utils.data import ConcatDataset
from transformers import AutoTokenizer, AutoModel
from datasets import load_dataset,Dataset
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model
from transformers import Trainer, TrainingArguments
from huggingface_hub import login
from dataset import CharacterDataset, read_jsonl_file, collate_fn

# DATA_PATH = 'train_data.csv'
# HF_TOKEN = 'hflcAlYNF'
# HF_TOKEN = "nPhmtMVuXy"
# login(token=HF_TOKEN)

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()

'''
这里放你的dataloader
'''
# jsonl_file_path = '/Users/pufferfish/Downloads/real_train_data/'
# character_path = "/Users/pufferfish/Chat-Haruhi-Suzumiya/characters/"
# file_names = ['xiaofeng_test_output_dialogue.jsonl', 'baizhantang_test_output_dialogue.jsonl', 'wangduoyu_test_output_dialogue.jsonl', 'guofurong_test_output_dialogue.jsonl', 'weixiaobao_test_output_dialogue.jsonl', 'haruhi_synthesis_dialogue.jsonl', 'murongfu_test_output_dialogue.jsonl', 'McGonagall_test_output_dialogue.jsonl', 'Ron_test_output_dialogue.jsonl', 'Sheldon_test_output_dialogue.jsonl', 'yuqian_test_output_dialogue.jsonl', 'duanyu_test_output_dialogue.jsonl', 'xuzhu_test_output_dialogue.jsonl', 'jiumozhi_test_output_dialogue.jsonl', 'liyunlong_synthesis_dialogue.jsonl', 'Malfoy_test_output_dialogue.jsonl', 'tongxiangyu_test_output_dialogue.jsonl', 'ayaka_test_output_dialogue.jsonl', 'Raj_test_output_dialogue.jsonl', 'Harry_test_output_dialogue.jsonl', 'Snape_test_output_dialogue.jsonl', 'Penny_test_output_dialogue.jsonl', 'zhongli_test_output_dialogue.jsonl', 'tangshiye_test_output_dialogue.jsonl', 'Luna_test_output_dialogue.jsonl', 'hutao_test_output_dialogue.jsonl', 'Dumbledore_test_output_dialogue.jsonl', 'Hermione_test_output_dialogue.jsonl', 'qiaofeng_test_output_dialogue.jsonl', 'wangyuyan_test_output_dialogue.jsonl', 'wanderer_test_output_dialogue.jsonl', 'raidenShogun_test_output_dialogue.jsonl']
# all_datasets = []
# for file_name in file_names:
#     character_name = file_name.split("_")[0]
#     character = os.path.join(character_path, character_name)
#     jsonl_file = os.path.join(jsonl_file_path, file_name)
#     jsonl_data = read_jsonl_file(jsonl_file)
#     c = CharacterDataset(jsonl_data, character, 8, 2000)
#     all_datasets.append(c)

# combined_dataset = ConcatDataset(all_datasets)

# batch_size = 1
# data_loader = DataLoader(combined_dataset, batch_size=batch_size, collate_fn=collate_fn)

# # train_dataset = {'train':[]}
# context = []
# target = []

# for i,item in enumerate(data_loader):
#     # print(item[0][0])
#     context.append(item[0][0])
#     target.append(item[1][0])

# train_dataset = {"context":context, "target":target}
# train_dataset = Dataset.from_dict(train_dataset)
# train_dataset.push_to_hub("silk-road/Chat_Suzumiya_Fusion", private=False)


dataset = load_dataset('silk-road/Chat_Suzumiya_Fusion')
print(dataset)

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

# model.push_to_hub("Jyshen/Chat_Suzumiya_GLM2LoRA", use_auth_token=True)
