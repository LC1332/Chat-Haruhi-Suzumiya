# coding: utf-8

import argparse
import os
import re
import subprocess
from collections import Counter
import chardet
import pysrt
import pysubs2
import pickle
from audio_feature_ext.tool import get_filename,get_subdir,get_onedir
import pandas as pd
from audio_feature_ext import AudioFeatureExtraction


def detect_encoding(file_name):
    with open(file_name, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']


def most_common_element(lst, num=1):
    counter = Counter(lst)
    most = counter.most_common(num)
    return most


def make_filename_safe(filename):
    # 将非法字符替换为下划线
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # 去除多余的空格
    filename = re.sub(r'\s+', ' ', filename)
    # 去除开头和结尾的空格
    filename = filename.strip()
    return filename


class video_Segmentation:
    def __init__(self):
        pass

    def clip_video_bycsv(self,annotate_csv,video_pth,role_audios):
        self.annotate_csv = annotate_csv
        self.video_pth = video_pth
        self.role_audios = role_audios
        srt_data = pd.read_csv(self.annotate_csv)
        srt_data = srt_data.dropna()
        srt_list = srt_data.values.tolist()
        for index, (person,subtitle,start_time,end_time) in enumerate(srt_list[:]):
            audio_output = f'{self.role_audios}/voice/{person}'
            os.makedirs(audio_output, exist_ok=True)
            index = str(index).zfill(4)
            subtitle = make_filename_safe(subtitle)

            audio_output = f'{audio_output}/{index}_{subtitle}.wav'
            self.ffmpeg_extract(self.video_pth,audio_output,start_time,end_time)


    def ffmpeg_extract(self,video_input,audio_output,start_time,end_time):

        command = ['ffmpeg', '-ss', str(start_time), '-to', str(end_time), '-i', f'{video_input}', "-vn",
                   '-c:a', 'pcm_s16le',
                   audio_output, '-loglevel', 'quiet']

        subprocess.run(command)


    def extract_pkl_feat(self,audio_extractor, role_audios):

        sub_dirs = get_subdir(f'{role_audios}/voice')

        for dir in sub_dirs[:]:
            voice_files = get_filename(dir)
            name = dir.split('/')[-1]
            for file, pth in voice_files:
                new_dir = os.path.join(role_audios, 'feature',name)
                os.makedirs(new_dir, exist_ok=True)
                try:
                    feature = audio_extractor.infer(pth)[0]
                    with open(f"{new_dir}/{file}.pkl", "wb") as f:
                        pickle.dump(feature, f)
                except:
                    continue
        print('音频特征提取完成')

    def extract_new_pkl_feat(self, audio_extractor, role_audios):
        sub_dir = get_onedir(f'{role_audios}')[0]


        voice_files = get_filename(f'{role_audios}/{sub_dir}/voice')
        for file, pth in voice_files:
            new_dir = os.path.join(role_audios, sub_dir, 'feature')
            os.makedirs(new_dir, exist_ok=True)
            try:
                feature = audio_extractor.infer(pth)[0]
                with open(f"{new_dir}/{file}.pkl", "wb") as f:
                    pickle.dump(feature, f)
            except:
                continue
        print('音频特征提取完成')

    def clip_video_bysrt(self,input_video,input_srt,output_folder):

        style = ''
        sub_format = input_srt.split('.')[-1]
        voice_dir = 'voice'
        file = input_video.split('/')[-1]
        filename, format = os.path.splitext(file)  # haruhi_01 .mkv
        
        # 创建对应的音频文件夹
        os.makedirs(f'{output_folder}/{filename}/{voice_dir}', exist_ok=True)

        # 检测字幕编码
        encoding = detect_encoding(input_srt)

        if sub_format == 'srt':
    
            srt_file = pysrt.open(input_srt, encoding=encoding)
            for index, subtitle in enumerate(srt_file[:]):
                # 获取开始和结束时间
                start_time = subtitle.start
                end_time = subtitle.end
                start_time = start_time.to_time()
                end_time = end_time.to_time()
                # 使用FFmpeg切割视频 
                index = str(index).zfill(4)
                text = make_filename_safe(subtitle.text)             
                audio_output = f'{output_folder}/{filename}/{voice_dir}/{index}_{text}.wav'
                self.ffmpeg_extract(input_video, audio_output, start_time, end_time)
    
        elif sub_format == 'ass':
            subs = pysubs2.load(input_srt, encoding=encoding)
            if not style:
                style_lis = [sub.style for sub in subs]
                most_1 = most_common_element(style_lis)
                style = most_1[0][0]  
            new_subs = [sub for sub in subs if sub.style == style]
            for index, subtitle in enumerate(new_subs[:]):
                # 获取开始和结束时间
                if subtitle.style == style:
                    start_time = subtitle.start
                    end_time = subtitle.end
                    start_time = start_time / 1000
                    end_time = end_time / 1000
                    # 使用FFmpeg切割视频 
                    index = str(index).zfill(4)
                    text = make_filename_safe(subtitle.text)
                    audio_output = f'{output_folder}/{filename}/{voice_dir}/{index}_{text}.wav'
                    self.ffmpeg_extract(input_video, audio_output, start_time, end_time)
        exit()



def crop(args):

    if args.verbose:
        print('runing crop')

    # checking if annotate_map is a file
    if not os.path.isfile(args.annotate_map):
        print('annotate_map is not exist')
        return


    # checking if role_audios is a folder
    if not os.path.isdir(args.role_audios):
        print('role_audios is not exist')
        # create role_audios folder
        os.mkdir(args.role_audios)

    data = pd.read_csv(args.annotate_map)
    for index, (annotate_csv,video_pth) in data.iterrows():
        # if annotate_csv and video_pth:
        # srt = csv2srt(annotate_csv)
        video_pth_segmentor = video_Segmentation()
        video_pth_segmentor.clip_video_bycsv(annotate_csv, video_pth, args.role_audios)

        # 音频提取特征 wav→pkl
        model_pth = '/mnt/sda/huggingface_weight/voicemodel/'
        audio_feature_extractor = AudioFeatureExtraction(model_pth)
        video_pth_segmentor.extract_pkl_feat(audio_feature_extractor,args.role_audios)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract audio by subtitle time stamp',
        epilog='author:fengyunzaidushi(https://github.com/fengyunzaidushi)'
    )
    # video_pth, role_audios, annotate_csv
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--annotate_map', default='./data_crop/haruhi_EP3_annotate_map.csv', type=str, required=True, help="list of video_pth and subtitle paths")
    parser.add_argument('--role_audios', default='/mnt/sda/baidu_disk/lg/scixing/roles', type=str, required=True, help= "directory of the role audio to save")

    args = parser.parse_args()
    parser.print_help()
    crop(args)