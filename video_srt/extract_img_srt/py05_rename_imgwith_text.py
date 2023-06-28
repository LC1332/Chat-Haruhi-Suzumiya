# coding: utf-8
import os
import shutil

from read import read_bigone
from config import SRT_CONFIG

def rename_file_new(old_out_dir,new_out_dir,num, dic):
    i = 1
    for id, text in dic.items():
        new_name = f'{i}_{text}.jpg'
        old_pth = os.path.join(old_out_dir, f'{num}/{id}.jpg')

        new_dir = os.path.join(new_out_dir, f'{num}')
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        new_pth = os.path.join(new_dir, new_name)
        shutil.copy(old_pth, new_pth)
        i += 1


if __name__ == '__main__':

    srt_dic_file = SRT_CONFIG['srt_dic_file']
    old_out_dir = SRT_CONFIG['img_out_dir']  # 切割出的图片的总文件夹
    new_out_dir = SRT_CONFIG['rename_img_dir']

    dic_data = read_bigone(srt_dic_file)
    lth = len(dic_data)
    for idx in range(lth):
        num = str(idx+1).zfill(2)
        rename_file_new(old_out_dir,new_out_dir,num, dic_data[num])
