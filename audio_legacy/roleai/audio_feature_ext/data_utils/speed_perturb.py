import random

import numpy as np


class SpeedPerturbAugmentor(object):
    """添加随机语速增强

    :param min_speed_rate: 新采样速率下限不应小于0.9
    :type min_speed_rate: float
    :param max_speed_rate: 新采样速率的上界不应大于1.1
    :type max_speed_rate: float
    :param prob: 数据增强的概率
    :type prob: float
    """

    def __init__(self, min_speed_rate=0.9, max_speed_rate=1.1, num_rates=3, prob=0.5):
        if min_speed_rate < 0.9:
            raise ValueError("Sampling speed below 0.9 can cause unnatural effects")
        if max_speed_rate > 1.1:
            raise ValueError("Sampling speed above 1.1 can cause unnatural effects")
        self.prob = prob
        self._min_speed_rate = min_speed_rate
        self._max_speed_rate = max_speed_rate
        self._num_rates = num_rates
        if num_rates > 0:
            self._rates = np.linspace(self._min_speed_rate, self._max_speed_rate, self._num_rates, endpoint=True)

    def __call__(self, wav):
        """改变音频语速

        :param wav: librosa 读取的数据
        :type wav: ndarray
        """
        if random.random() > self.prob: return wav
        if self._num_rates < 0:
            speed_rate = random.uniform(self._min_speed_rate, self._max_speed_rate)
        else:
            speed_rate = random.choice(self._rates)
        if speed_rate == 1.0: return wav

        old_length = wav.shape[0]
        new_length = int(old_length / speed_rate)
        old_indices = np.arange(old_length)
        new_indices = np.linspace(start=0, stop=old_length, num=new_length)
        wav = np.interp(new_indices, old_indices, wav)
        return wav
