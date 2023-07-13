import os
import numpy as np
import torch
import pickle


# from modules.ecapa_tdnn import EcapaTdnn, SpeakerIdetification
# from data_utils.reader import load_audio, CustomDataset
from audio_legacy.roleai.tool import get_subdir, get_filename
from .modules.ecapa_tdnn import EcapaTdnn, SpeakerIdetification
from .data_utils.reader import load_audio, CustomDataset

class AudioFeatureExtraction:
    def __init__(self, model_local_pth,audio_duration=3, feature_method='melspectrogram', ):
        self.use_model = ''
        self.audio_duration = audio_duration
        self.feature_method = feature_method
        self.resume = model_local_pth
        self.model = None
        self.device = None
        self.load_model()

    def load_model(self):
        dataset = CustomDataset(data_list_path=None, feature_method=self.feature_method)
        ecapa_tdnn = EcapaTdnn(input_size=dataset.input_size)
        self.model = SpeakerIdetification(backbone=ecapa_tdnn)
        self.device = torch.device("cuda")
        self.model.to(self.device)

        # 加载模型
        model_path = os.path.join(self.resume, self.use_model, 'model.pth')
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
