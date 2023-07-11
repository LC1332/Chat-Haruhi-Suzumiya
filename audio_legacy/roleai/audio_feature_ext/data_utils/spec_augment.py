import random

import numpy as np
from PIL import Image
from PIL.Image import BICUBIC


class SpecAugmentor(object):
    """Augmentation model for Time warping, Frequency masking, Time masking.

    SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition
        https://arxiv.org/abs/1904.08779
    SpecAugment on Large Scale Datasets
        https://arxiv.org/abs/1912.05533
    """

    def __init__(self,
                 F=10,
                 T=50,
                 n_freq_masks=2,
                 n_time_masks=2,
                 p=1.0,
                 W=40,
                 adaptive_number_ratio=0,
                 adaptive_size_ratio=0,
                 max_n_time_masks=20,
                 replace_with_zero=True,
                 prob=0.5):
        """SpecAugment class.
        Args:
            :param F: 频率屏蔽参数
            :type F: int
            :param T: 时间屏蔽参数
            :type T: int
            :param n_freq_masks: 频率屏蔽数量
            :type n_freq_masks: int
            :param n_time_masks: 时间屏蔽数量
            :type n_time_masks: int
            :param p: 时间屏蔽上限参数
            :type p: float
            :param W: 时间变形参数
            :type W: int
            :param adaptive_number_ratio: 时间屏蔽的自适应多重比
            :type adaptive_number_ratio: float
            :param adaptive_size_ratio: 时间屏蔽的自适应大小比
            :type adaptive_size_ratio: float
            :param max_n_time_masks: 时间屏蔽的最大数目
            :type max_n_time_masks: int
            :param replace_with_zero: 如果真的话，在pad补0，否则使用平均值
            :type replace_with_zero: bool
            :param prob: 数据增强的概率
            :type prob: float
        """
        super().__init__()
        self.inplace = True
        self.replace_with_zero = replace_with_zero

        self.prob = prob
        self.W = W
        self.F = F
        self.T = T
        self.n_freq_masks = n_freq_masks
        self.n_time_masks = n_time_masks
        self.p = p

        # adaptive SpecAugment
        self.adaptive_number_ratio = adaptive_number_ratio
        self.adaptive_size_ratio = adaptive_size_ratio
        self.max_n_time_masks = max_n_time_masks

        if adaptive_number_ratio > 0:
            self.n_time_masks = 0
        if adaptive_size_ratio > 0:
            self.T = 0

        self._freq_mask = None
        self._time_mask = None

    @property
    def freq_mask(self):
        return self._freq_mask

    @property
    def time_mask(self):
        return self._time_mask

    def __repr__(self):
        return f"specaug: F-{self.F}, T-{self.T}, F-n-{self.n_freq_masks}, T-n-{self.n_time_masks}"

    def __call__(self, x):
        """

        :param x: 经过预处理的音频数据
        :type x: ndarray
        """
        if random.random() > self.prob: return x
        return self.transform_feature(x)

    def time_warp(self, x):
        """time warp for spec augment
        move random center frame by the random width ~ uniform(-window, window)

        Args:
            x (np.ndarray): spectrogram (time, freq)

        Raises:
            NotImplementedError: [description]
            NotImplementedError: [description]

        Returns:
            np.ndarray: time warped spectrogram (time, freq)
        """
        window = self.W
        if window == 0:
            return x
        t = x.shape[0]
        if t - window <= window:
            return x
        # NOTE: randrange(a, b) emits a, a + 1, ..., b - 1
        center = random.randrange(window, t - window)
        warped = random.randrange(center - window, center + window) + 1  # 1 ... t - 1
        left = Image.fromarray(x[:center]).resize((x.shape[1], warped), BICUBIC)
        right = Image.fromarray(x[center:]).resize((x.shape[1], t - warped), BICUBIC)
        if self.inplace:
            x[:warped] = left
            x[warped:] = right
            return x
        return np.concatenate((left, right), 0)

    def mask_freq(self, x, replace_with_zero=False):
        """freq mask

        Args:
            x (np.ndarray): spectrogram (time, freq)
            replace_with_zero (bool, optional): Defaults to False.

        Returns:
            np.ndarray: freq mask spectrogram (time, freq)
        """
        n_bins = x.shape[1]
        for i in range(0, self.n_freq_masks):
            f = int(random.uniform(a=0, b=self.F))
            f_0 = int(random.uniform(a=0, b=n_bins - f))
            assert f_0 <= f_0 + f
            if replace_with_zero:
                x[:, f_0:f_0 + f] = 0
            else:
                x[:, f_0:f_0 + f] = x.mean()
            self._freq_mask = (f_0, f_0 + f)
        return x

    def mask_time(self, x, replace_with_zero=False):
        """time mask

        Args:
            x (np.ndarray): spectrogram (time, freq)
            replace_with_zero (bool, optional): Defaults to False.

        Returns:
            np.ndarray: time mask spectrogram (time, freq)
        """
        n_frames = x.shape[0]

        if self.adaptive_number_ratio > 0:
            n_masks = int(n_frames * self.adaptive_number_ratio)
            n_masks = min(n_masks, self.max_n_time_masks)
        else:
            n_masks = self.n_time_masks

        if self.adaptive_size_ratio > 0:
            T = self.adaptive_size_ratio * n_frames
        else:
            T = self.T

        for i in range(n_masks):
            t = int(random.uniform(a=0, b=T))
            t = min(t, int(n_frames * self.p))
            t_0 = int(random.uniform(a=0, b=n_frames - t))
            assert t_0 <= t_0 + t
            if replace_with_zero:
                x[t_0:t_0 + t, :] = 0
            else:
                x[t_0:t_0 + t, :] = x.mean()
            self._time_mask = (t_0, t_0 + t)
        return x

    def transform_feature(self, x: np.ndarray):
        """
        Args:
            x (np.ndarray): `[T, F]`
        Returns:
            x (np.ndarray): `[T, F]`
        """
        assert isinstance(x, np.ndarray)
        assert x.ndim == 2
        x = self.time_warp(x)
        x = self.mask_freq(x, self.replace_with_zero)
        x = self.mask_time(x, self.replace_with_zero)
        return x
