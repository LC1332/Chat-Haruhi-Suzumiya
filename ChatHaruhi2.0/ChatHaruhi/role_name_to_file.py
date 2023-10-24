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
# 
# if you have attempt to add a new character, please add the role name here
# 

role_name_Haruhiu = {'汤师爷': 'tangshiye', 'tangshiye': 'tangshiye', 'Tangshiye': 'tangshiye', 
                     '慕容复': 'murongfu', 'murongfu': 'murongfu', 'Murongfu': 'murongfu', 
                     '李云龙': 'liyunlong', 'liyunlong': 'liyunlong', 'Liyunlong': 'liyunlong', 
                     'Luna': 'Luna', '王多鱼': 'wangduoyu', 'wangduoyu': 'wangduoyu', 
                     'Wangduoyu': 'wangduoyu', 'Ron': 'Ron', '鸠摩智': 'jiumozhi', 
                     'jiumozhi': 'jiumozhi', 'Jiumozhi': 'jiumozhi', 'Snape': 'Snape', 
                     '凉宫春日': 'haruhi', 'haruhi': 'haruhi', 'Haruhi': 'haruhi', 
                     'Malfoy': 'Malfoy', '虚竹': 'xuzhu', 'xuzhu': 'xuzhu', 
                     'Xuzhu': 'xuzhu', '萧峰': 'xiaofeng', 
                     'xiaofeng': 'xiaofeng', 'Xiaofeng': 'xiaofeng', '段誉': 'duanyu', 
                     'duanyu': 'duanyu', 'Duanyu': 'duanyu', 'Hermione': 'Hermione', 
                     'Dumbledore': 'Dumbledore', '王语嫣': 'wangyuyan', 'wangyuyan': 
                     'wangyuyan', 'Wangyuyan': 'wangyuyan', 'Harry': 'Harry', 
                     'McGonagall': 'McGonagall', '白展堂': 'baizhantang', 
                     'baizhantang': 'baizhantang', 'Baizhantang': 'baizhantang', 
                     '佟湘玉': 'tongxiangyu', 'tongxiangyu': 'tongxiangyu', 
                     'Tongxiangyu': 'tongxiangyu', '郭芙蓉': 'guofurong', 
                     'guofurong': 'guofurong', 'Guofurong': 'guofurong', '流浪者': 'wanderer', 
                     'wanderer': 'wanderer', 'Wanderer': 'wanderer', '钟离': 'zhongli', 
                     'zhongli': 'zhongli', 'Zhongli': 'zhongli', '胡桃': 'hutao', 'hutao': 'hutao', 
                     'Hutao': 'hutao', 'Sheldon': 'Sheldon', 'Raj': 'Raj', 
                     'Penny': 'Penny', '韦小宝': 'weixiaobao', 'weixiaobao': 'weixiaobao', 
                     'Weixiaobao': 'weixiaobao', '乔峰': 'qiaofeng', 'qiaofeng': 'qiaofeng', 
                     'Qiaofeng': 'qiaofeng', '神里绫华': 'ayaka', 'ayaka': 'ayaka', 
                     'Ayaka': 'ayaka', '雷电将军': 'raidenShogun', 'raidenShogun': 'raidenShogun', 
                     'RaidenShogun': 'raidenShogun', '于谦': 'yuqian', 'yuqian': 'yuqian', 
                     'Yuqian': 'yuqian', 'Professor McGonagall': 'McGonagall', 
                     'Professor Dumbledore': 'Dumbledore'}

# input role_name , nick name is also allowed
# output folder_role_name and url url = f'https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/character_in_zip/{role_name}.zip'
def get_folder_role_name(role_name):
    if role_name in role_name_Haruhiu:
        folder_role_name = role_name_Haruhiu[role_name]
        url = f'https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/character_in_zip/{folder_role_name}.zip'
        return folder_role_name, url
    else:
        print('role_name {} not found, using haruhi as default'.format(role_name))
        return get_folder_role_name('haruhi')