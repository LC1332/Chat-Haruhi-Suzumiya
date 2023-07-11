import random
import sys

from datetime import datetime

import torch
import librosa
import numpy as np
from torch.utils import data


def load_audio(audio_path,
               feature_method='melspectrogram',
               mode='train',
               sr=16000,
               chunk_duration=3,
               min_duration=0.5,
               augmentors=None):
    """
    加载并预处理音频
    :param audio_path: 音频路径
    :param feature_method: 预处理方法
    :param mode: 对数据处理的方式，包括train，eval，infer
    :param sr: 采样率
    :param chunk_duration: 训练或者评估使用的音频长度
    :param min_duration: 最小训练或者评估的音频长度
    :param augmentors: 数据增强方法
    :return:
    """
    # 读取音频数据
    wav, sr_ret = librosa.load(audio_path, sr=sr)
    num_wav_samples = wav.shape[0]
    # 数据太短不利于训练
    if mode == 'train':
        if num_wav_samples < int(min_duration * sr):
            raise Exception(f'音频长度小于{min_duration}s，实际长度为：{(num_wav_samples/sr):.2f}s')
    # 对小于训练长度的复制补充
    num_chunk_samples = int(chunk_duration * sr)
    if num_wav_samples <= num_chunk_samples:
        shortage = num_chunk_samples - num_wav_samples
        wav = np.pad(wav, (0, shortage), 'wrap')
    # 裁剪需要的数据
    if mode == 'train':
        # 随机裁剪
        num_wav_samples = wav.shape[0]
        num_chunk_samples = int(chunk_duration * sr)
        if num_wav_samples > num_chunk_samples + 1:
            start = random.randint(0, num_wav_samples - num_chunk_samples - 1)
            stop = start + num_chunk_samples
            wav = wav[start:stop]
            # 对每次都满长度的再次裁剪
            if random.random() > 0.5:
                wav[:random.randint(1, sr // 4)] = 0
                wav = wav[:-random.randint(1, sr // 4)]
        # 数据增强
        if augmentors is not None:
            for key, augmentor in augmentors.items():
                if key == 'specaug':continue
                wav = augmentor(wav)
    elif mode == 'eval':
        # 为避免显存溢出，只裁剪指定长度
        num_wav_samples = wav.shape[0]
        num_chunk_samples = int(chunk_duration * sr)
        if num_wav_samples > num_chunk_samples + 1:
            wav = wav[:num_chunk_samples]
    # 获取音频特征
    if feature_method == 'melspectrogram':
        # 计算梅尔频谱
        features = librosa.feature.melspectrogram(y=wav, sr=sr, n_fft=400, n_mels=80, hop_length=160, win_length=400)
    elif feature_method == 'spectrogram':
        # 计算声谱图
        linear = librosa.stft(wav, n_fft=400, win_length=400, hop_length=160)
        features, _ = librosa.magphase(linear)
    else:
        raise Exception(f'预处理方法 {feature_method} 不存在！')
    features = librosa.power_to_db(features, ref=1.0, amin=1e-10, top_db=None)
    # 数据增强
    if mode == 'train' and augmentors is not None:
        for key, augmentor in augmentors.items():
            if key == 'specaug':
                features = augmentor(features)
    # 归一化
    mean = np.mean(features, 0, keepdims=True)
    std = np.std(features, 0, keepdims=True)
    features = (features - mean) / (std + 1e-5)
    return features


# 数据加载器
class CustomDataset(data.Dataset):
    """
    加载并预处理音频
    :param data_list_path: 数据列表
    :param feature_method: 预处理方法
    :param mode: 对数据处理的方式，包括train，eval，infer
    :param sr: 采样率
    :param chunk_duration: 训练或者评估使用的音频长度
    :param min_duration: 最小训练或者评估的音频长度
    :param augmentors: 数据增强方法
    :return:
    """
    def __init__(self, data_list_path,
                 feature_method='melspectrogram',
                 mode='train',
                 sr=16000,
                 chunk_duration=3,
                 min_duration=0.5,
                 augmentors=None):
        super(CustomDataset, self).__init__()
        # 当预测时不需要获取数据
        if data_list_path is not None:
            with open(data_list_path, 'r') as f:
                self.lines = f.readlines()
        self.feature_method = feature_method
        self.mode = mode
        self.sr = sr
        self.chunk_duration = chunk_duration
        self.min_duration = min_duration
        self.augmentors = augmentors

    def __getitem__(self, idx):
        try:
            audio_path, label = self.lines[idx].replace('\n', '').split('\t')
            # 加载并预处理音频
            features = load_audio(audio_path, feature_method=self.feature_method, mode=self.mode, sr=self.sr,
                                  chunk_duration=self.chunk_duration, min_duration=self.min_duration,
                                  augmentors=self.augmentors)
            return features, np.array(int(label), dtype=np.int64)
        except Exception as ex:
            print(f"[{datetime.now()}] 数据: {self.lines[idx]} 出错，错误信息: {ex}", file=sys.stderr)
            rnd_idx = np.random.randint(self.__len__())
            return self.__getitem__(rnd_idx)

    def __len__(self):
        return len(self.lines)

    @property
    def input_size(self):
        if self.feature_method == 'melspectrogram':
            return 80
        elif self.feature_method == 'spectrogram':
            return 201
        else:
            raise Exception(f'预处理方法 {self.feature_method} 不存在！')


# 对一个batch的数据处理
def collate_fn(batch):
    # 找出音频长度最长的
    batch = sorted(batch, key=lambda sample: sample[0].shape[1], reverse=True)
    freq_size = batch[0][0].shape[0]
    max_audio_length = batch[0][0].shape[1]
    batch_size = len(batch)
    # 以最大的长度创建0张量
    inputs = np.zeros((batch_size, freq_size, max_audio_length), dtype='float32')
    input_lens = []
    labels = []
    for x in range(batch_size):
        sample = batch[x]
        tensor = sample[0]
        labels.append(sample[1])
        seq_length = tensor.shape[1]
        # 将数据插入都0张量中，实现了padding
        inputs[x, :, :seq_length] = tensor[:, :]
        input_lens.append(seq_length/max_audio_length)
    input_lens = np.array(input_lens, dtype='float32')
    labels = np.array(labels, dtype='int64')
    # 打乱数据
    return torch.tensor(inputs), torch.tensor(labels), torch.tensor(input_lens)
