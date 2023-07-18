'''
FILE_NAME: dialogue2embedding.py
First Edition
Edited by 睡觉鱼, Jul 18 2023
'''

from datasets import load_dataset,concatenate_datasets,Dataset
import torch
import torch.nn as nn
from argparse import Namespace
from transformers import AutoTokenizer, AutoModel

def dialogue2embedding(dialogues,tokenizer,model):
    texts = dialogues['train']['context'][0]
    embeddings = []

    for text in texts:
        input = [text]
        inputs = tokenizer(input,
                    padding=True,
                    truncation=True,
                    return_tensors='pt')
        # Extract the embeddings
        with torch.no_grad():
            embed = model(**inputs,
                        output_hidden_states=True,
                        return_dict=True,
                        sent_emb=True).pooler_output    
                
        embeddings.append(embed)
    
    embed_dict = {'embedding':[embeddings]}
    embed_dict = Dataset.from_dict(embed_dict)

    dialogues['train'] = concatenate_datasets([dialogues['train'], embed_dict], axis=1)
    return dialogues

if __name__ == '__main__':
    DATA_PATH = 'dialogue.json'
    luotuo_tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False, init_embeddings_model=None)
    luotuo_model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)

    dialogues = load_dataset("json", data_files= DATA_PATH)
    dialogue_embeddings = dialogue2embedding(dialogues,luotuo_tokenizer,luotuo_model)
    dialogue_embeddings['train'].to_json("dataset.json")
