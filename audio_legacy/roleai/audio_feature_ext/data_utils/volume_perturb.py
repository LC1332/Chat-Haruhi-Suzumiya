import random


class VolumePerturbAugmentor(object):
    """添加随机音量大小

    :param min_gain_dBFS: 最小增益
    :type min_gain_dBFS: int
    :param max_gain_dBFS: 最小增益大
    :type max_gain_dBFS: int
    :param prob: 数据增强的概率
    :type prob: float
    """

    def __init__(self, min_gain_dBFS=-15, max_gain_dBFS=15, prob=0.5):
        self.prob = prob
        self._min_gain_dBFS = min_gain_dBFS
        self._max_gain_dBFS = max_gain_dBFS

    def __call__(self, wav):
        """改变音量大小

        :param wav: librosa 读取的数据
        :type wav: ndarray
        """
        if random.random() > self.prob: return wav
        gain = random.uniform(self._min_gain_dBFS, self._max_gain_dBFS)
        wav *= 10.**(gain / 20.)
        return wav
