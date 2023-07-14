import os
import numpy as np
import torch
import pickle


import requests
from .modules.ecapa_tdnn import EcapaTdnn, SpeakerIdetification
from .data_utils.reader import load_audio, CustomDataset

class AudioFeatureExtraction:
    def __init__(self,model_director='./audio_feature_ext/models', audio_duration=3, feature_method='melspectrogram' ):
        self.use_model = ''
        self.audio_duration = audio_duration
        self.model_director = model_director
        self.feature_method = feature_method
        self.model = None
        self.device = None
        self.load_model()

    def init_models(self,path):
        model_urls = ['https://huggingface.co/scixing/voicemodel/resolve/main/model.pth',
                      'https://huggingface.co/scixing/voicemodel/resolve/main/model.state',
                      'https://huggingface.co/scixing/voicemodel/resolve/main/optimizer.pth']
        listdir = os.listdir(path)
        for url in model_urls:
            filename = url.split('/')[-1]
            if filename in listdir:
                continue
            r = requests.get(url, allow_redirects=True)
            print(f'downloading model pth {filename}')
            open(f'{path}/{filename}', 'wb').write(r.content)
            print(f'{filename} success download')
    def load_model(self):
        dataset = CustomDataset(data_list_path=None, feature_method=self.feature_method)
        ecapa_tdnn = EcapaTdnn(input_size=dataset.input_size)
        self.model = SpeakerIdetification(backbone=ecapa_tdnn)
        self.device = torch.device("cuda")
        self.model.to(self.device)

        if not os.path.exists(self.model_director):
            os.makedirs(self.model_director)
        model_files = ['model.pth', 'model.state', 'optimizer.pth']
        for file in model_files:
            if not os.path.exists(f'{self.model_director}/{file}'):
                self.init_models(self.model_director)

        # 加载模型
        model_path = os.path.join(self.model_director, 'model.pth')
        model_dict = self.model.state_dict()
        param_state_dict = torch.load(model_path)
        for name, weight in model_dict.items():
            if name in param_state_dict.keys():
                if list(weight.shape) != list(param_state_dict[name].shape):
                    param_state_dict.pop(name, None)
        self.model.load_state_dict(param_state_dict, strict=False)
        print(f"成功加载模型参数和优化方法参数：{model_path}")
        self.model.eval()

    def infer(self, audio_path):
        data = load_audio(audio_path, mode='infer', feature_method=self.feature_method,
                          chunk_duration=self.audio_duration)
        data = data[np.newaxis, :]
        data = torch.tensor(data, dtype=torch.float32, device=self.device)
        feature = self.model.backbone(data)
        return feature.data.cpu().numpy()

    def extract_features(self, root_dir):
        sub_dirs = get_subdir(root_dir)

        for dir in sub_dirs[:]:
            voice_files = get_filename(os.path.join(dir, 'voice'))
            for file, pth in voice_files:
                new_dir = os.path.join(dir, 'feature')
                os.makedirs(new_dir, exist_ok=True)
                try:
                    feature = self.infer(pth)[0]
                    with open(f"{new_dir}/{file}.pkl", "wb") as f:
                        pickle.dump(feature, f)
                except:
                    continue
        print('音频特征提取完成')

    def extract_pkl_feat(self, root_dir):
        sub_dirs = get_subdir(root_dir)

        for dir in sub_dirs[:]:
            voice_files = get_filename(os.path.join(dir, 'voice'))
            for file, pth in voice_files:
                new_dir = os.path.join(dir, 'feature')
                os.makedirs(new_dir, exist_ok=True)
                try:
                    feature = self.infer(pth)[0]
                    with open(f"{new_dir}/{file}.pkl", "wb") as f:
                        pickle.dump(feature, f)
                except:
                    continue
        print('音频特征提取完成')

if __name__ == '__main__':
    pass
