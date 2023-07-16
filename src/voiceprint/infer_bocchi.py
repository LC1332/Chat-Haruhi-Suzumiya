import argparse
import functools
import os

import numpy as np
import torch

from modules.ecapa_tdnn import EcapaTdnn, SpeakerIdetification
from data_utils.reader import load_audio, CustomDataset
from utils.utility import add_arguments, print_arguments

import pickle
import requests


def init_models(path):
    model_urls = ['https://huggingface.co/scixing/voicemodel/resolve/main/model.pth',
               'https://huggingface.co/scixing/voicemodel/resolve/main/model.state',
               'https://huggingface.co/scixing/voicemodel/resolve/main/optimizer.pth'] 
    listdir = os.listdir(path)
    for url in model_urls:
        filename = url.split('/')[-1]
        if filename in listdir:
            continue
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)

use_model = 'ecapa_tdnn'
audio_path1 = 'audio/a_1.wav'
audio_path2 = 'audio/b_2.wav'
threshold = 0.5
audio_duration = 3
feature_method = 'melspectrogram'
resume = 'models/'

if not os.path.exists(resume):
    os.makedirs(resume)
init_models(resume)

# 初始化一个已知声音列表
voice_list = []
feature_list = []
dataset = CustomDataset(data_list_path=None, feature_method=feature_method)

ecapa_tdnn = EcapaTdnn(input_size=dataset.input_size)
model = SpeakerIdetification(backbone=ecapa_tdnn)
# 指定使用设备
device = torch.device("cuda")
model.to(device)
# 加载模型
model_path = os.path.join(resume, use_model, 'model.pth')
model_dict = model.state_dict()
param_state_dict = torch.load(model_path)
for name, weight in model_dict.items():
    if name in param_state_dict.keys():
        if list(weight.shape) != list(param_state_dict[name].shape):
            param_state_dict.pop(name, None)
model.load_state_dict(param_state_dict, strict=False)
print(f"成功加载模型参数和优化方法参数：{model_path}")
model.eval()


# 预测音频
def infer(audio_path):
    data = load_audio(audio_path, mode='infer', feature_method=feature_method, chunk_duration=audio_duration)
    data = data[np.newaxis, :]
    data = torch.tensor(data, dtype=torch.float32, device=device)
    # 执行预测
    feature = model.backbone(data)
    return feature.data.cpu().numpy()

patha = f"your path"
os.makedirs("feature", exist_ok=True)
for file in os.listdir(patha):
    if file.endswith(".wav") or file.endswith(".mp3"): 
        # 计算特征
        feature = infer(patha + file)[0]
        with open(f"feature/{file}.pkl", "wb") as f:
            pickle.dump(feature, f)
    

