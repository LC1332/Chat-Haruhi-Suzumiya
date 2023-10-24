# ChatHaruhi: Reviving Anime Character in Reality via Large Language Model
#
# ChatHaruhi 2.0, built by Cheng Li and Weishi Mi
#
# chengli.thu@gmail.com, mws22@mails.tsinghua.edu.cn
# 
# Weishi Mi is a second-year graduate student at Tsinghua University, majoring in computer science.
# Weishi Mi is pursuing a job or a PhD position, which who will be available next year
# 
# homepage https://github.com/LC1332/Chat-Haruhi-Suzumiya
# 
# ChatHaruhi is a chatbot that can revive anime characters in reality.
# the 2.0 version was built by Cheng Li and Weishi Mi.
# 
# Please cite our paper if you use this code for research: 
#
# @misc{li2023chatharuhi,
#       title={ChatHaruhi: Reviving Anime Character in Reality via Large Language Model}, 
#       author={Cheng Li and Ziang Leng and Chenxi Yan and Junyi Shen and Hao Wang and Weishi MI and Yaying Fei and Xiaoyang Feng and Song Yan and HaoSheng Wang and Linkang Zhan and Yaokai Jia and Pingyu Wu and Haozhen Sun},
#       year={2023},
#       eprint={2308.09597},
#       archivePrefix={arXiv},
#       primaryClass={cs.CL}
# }
from abc import ABC, abstractmethod

class BaseLLM(ABC):

    def __init__(self):
        pass
    
    @abstractmethod
    def initialize_message(self):
        pass

    @abstractmethod    
    def ai_message(self, payload):
        pass

    @abstractmethod
    def system_message(self, payload):
        pass

    @abstractmethod
    def user_message(self, payload):
        pass

    @abstractmethod
    def get_response(self):
        pass

    @abstractmethod
    def print_prompt(self):
        pass


