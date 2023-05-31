#coding: utf-8
from util import  read_tolist, write_to_file
from transformers import pipeline

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # 指定要使用的GPU设备编号
pipe = pipeline(model="engmatic-earth/mt5-zh-ja-en-trimmed-fine-tuned-v1", device=0)
def translate_sentence(sentence):
    return pipe(f'<-zh2ja-> {sentence}')[0]['translation_text']

sentences = read_tolist('./data/消失_中文.txt')
result = '\n'.join(translate_sentence(s) for s in sentences)
print(result)
write_to_file('模型1—中日.txt', result)
