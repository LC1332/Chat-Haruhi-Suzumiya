import json
import pickle

import torch


def check(fileName):
    with open(fileName, 'rb') as f:
        print(len(list(pickle.load(f).keys())))


# check('./dict_text.pkl')
# check('./text_embed.pkl')
# pkl -> jsonl

def pkl_to_json(filename):
    with open(filename, 'rb') as f, open(filename[:-3]+'jsonl', 'w+', encoding='utf-8') as f2:
        data = pickle.load(f)
        for k, v in data.items():
            if isinstance(v, torch.Tensor):
                v = v.numpy().tolist()
            item = {k:v}
            json.dump(item, f2, ensure_ascii=False)
            f2.write('\n')

# pkl_to_json('dict_text.pkl')
# pkl_to_json('text_image.pkl')
# pkl_to_json('title_to_text.pkl')
with open('dict_text.jsonl', 'r') as f:
    for line in f:
        print(json.load(f))