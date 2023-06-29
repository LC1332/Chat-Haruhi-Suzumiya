import os
import random
import warnings

import numpy as np

warnings.filterwarnings("ignore")
import librosa


class NoisePerturbAugmentor(object):
    """用于添加背景噪声的增强模型

    :param min_snr_dB: 最小的信噪比，以分贝为单位
    :type min_snr_dB: int
    :param max_snr_dB: 最大的信噪比，以分贝为单位
    :type max_snr_dB: int
    :param noise_path: 噪声文件夹
    :type noise_path: str
    :param sr: 音频采样率，必须跟训练数据的一样
    :type sr: int
    :param prob: 数据增强的概率
    :type prob: float
    """

    def __init__(self, min_snr_dB=10, max_snr_dB=30, noise_path="dataset/noise", sr=16000, prob=0.5):
        self.prob = prob
        self.sr = sr
        self._min_snr_dB = min_snr_dB
        self._max_snr_dB = max_snr_dB
        self._noise_files = self.get_noise_file(noise_path=noise_path)

    # 获取全部噪声数据
    @staticmethod
    def get_noise_file(noise_path):
        noise_files = []
        if not os.path.exists(noise_path): return noise_files
        for file in os.listdir(noise_path):
            noise_files.append(os.path.join(noise_path, file))
        return noise_files

    @staticmethod
    def rms_db(wav):
        """返回以分贝为单位的音频均方根能量

        :return: 均方根能量(分贝)
        :rtype: float
        """
        mean_square = np.mean(wav ** 2)
        return 10 * np.log10(mean_square)

    def __call__(self, wav):
        """添加背景噪音音频

        :param wav: librosa 读取的数据
        :type wav: ndarray
        """
        if random.random() > self.prob: return wav
        # 如果没有噪声数据跳过
        if len(self._noise_files) == 0: return wav
        noise, r = librosa.load(random.choice(self._noise_files), sr=self.sr)
        # 噪声大小
        snr_dB = random.uniform(self._min_snr_dB, self._max_snr_dB)
        noise_gain_db = min(self.rms_db(wav) - self.rms_db(noise) - snr_dB, 300)
        noise *= 10. ** (noise_gain_db / 20.)
        # 合并噪声数据
        noise_new = np.zeros(wav.shape, dtype=np.float32)
        if noise.shape[0] >= wav.shape[0]:
            start = random.randint(0, noise.shape[0] - wav.shape[0])
            noise_new[:wav.shape[0]] = noise[start: start + wav.shape[0]]
        else:
            start = random.randint(0, wav.shape[0] - noise.shape[0])
            noise_new[start:start + noise.shape[0]] = noise[:]
        wav += noise_new
        return wav
