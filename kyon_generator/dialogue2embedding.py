'''
FILE_NAME: dialogue2embedding.py
First Edition
Edited by 睡觉鱼, Jul 18 2023
'''

import json
import torch
import torch.nn as nn
from argparse import Namespace
from transformers import AutoTokenizer, AutoModel

def dialogue2embedding(dialogues,tokenizer,model):
    texts = dialogues['context']
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
                
        embeddings.append(embed.numpy().tolist())
    
    dialogues['embedding'] = embeddings
    return dialogues

if __name__ == '__main__':
    DATA_PATH = 'dialogue.json'
    luotuo_tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False, init_embeddings_model=None)
    luotuo_model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)

    with open ('dialogue.json') as f:
        dialogues = json.load(f)

    dialogue_embeddings = dialogue2embedding(dialogues,luotuo_tokenizer,luotuo_model)
    with open("myfile.json", "w") as o:
        json.dump(dialogue_embeddings,o)
    
