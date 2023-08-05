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
from audio_feature_ext.tool import get_filename,get_subdir
import pandas as pd
from audio_feature_ext.audio_fea_ext import AudioFeatureExtraction
from tqdm import tqdm



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
    filename = re.sub(r'[\\/:*?"<>|_]', '', filename)
    # 去除多余的空格
    filename = re.sub(r'\s+', ' ', filename)
    # 去除开头和结尾的空格
    filename = filename.strip()
    return filename


class video_Segmentation:
    def __init__(self):
        pass


    def ffmpeg_extract_audio(self,video_input,audio_output,start_time,end_time):

        command = ['ffmpeg', '-ss', str(start_time), '-to', str(end_time), '-i', f'{video_input}', "-vn",
                   '-c:a', 'pcm_s16le','-y',
                   audio_output, '-loglevel', 'quiet']

        subprocess.run(command)



    def extract_pkl_feat(self,audio_extractor, role_audios):

        sub_dirs = get_subdir(f'{role_audios}/voice')

        for dir in sub_dirs[:]:
            voice_files = get_filename(dir)
            name = os.path.basename(os.path.normpath(dir))
            for file, pth in tqdm(voice_files, f'extract {name} audio features ,convert .wav to .pkl'):
                new_dir = os.path.join(role_audios, 'feature',name)
                os.makedirs(new_dir, exist_ok=True)
                try:
                    feature = audio_extractor.infer(pth)[0]
                    with open(f"{new_dir}/{file}.pkl", "wb") as f:
                        pickle.dump(feature, f)
                except:
                    continue
        print('音频特征提取完成')

    def extract_new_pkl_feat(self, audio_extractor,input_video, temp_folder):

        file = os.path.basename(input_video)
        filename, format = os.path.splitext(file)  # haruhi_01 .mkv

        # 找到对应的音频文件夹
        sub_dir = f'{temp_folder}/{filename}'

        voice_files = get_filename(f'{sub_dir}/voice')
        for file, pth in tqdm(voice_files,f'extract {filename} audio features ,convert .wav to .pkl'):
            new_dir = os.path.join(sub_dir, 'feature')
            os.makedirs(new_dir, exist_ok=True)
            try:
                feature = audio_extractor.infer(pth)[0]
                with open(f"{new_dir}/{file}.pkl", "wb") as f:
                    pickle.dump(feature, f)
            except:
                continue
        print('音频特征提取完成')

    def clip_audio_bycsv(self,annotate_csv,video_pth,role_audios):
        self.annotate_csv = annotate_csv
        self.video_pth = video_pth
        self.role_audios = role_audios
        srt_data = pd.read_csv(self.annotate_csv).iloc[:,:4]
        srt_data = srt_data.dropna()
        srt_list = srt_data.values.tolist()
        for index, (person,subtitle,start_time,end_time) in enumerate(tqdm(srt_list[:], 'video clip by csv file start')):
            audio_output = f'{self.role_audios}/voice/{person}'
            os.makedirs(audio_output, exist_ok=True)
            index = str(index).zfill(4)
            text = make_filename_safe(subtitle)


            ss = start_time.zfill(11).ljust(12, '0')[:12]
            ee = end_time.zfill(11).ljust(12, '0')[:12]

            name = f'{index}_{ss}_{ee}_{text}'.replace(':', '.')

            audio_output = f'{audio_output}/{name}.wav'
            self.ffmpeg_extract_audio(self.video_pth,audio_output,start_time,end_time)

    def srt_format_timestamp(self, seconds):
        assert seconds >= 0, "non-negative timestamp expected"
        milliseconds = round(seconds * 1000.0)

        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000

        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000

        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000

        return (f"{hours:02d}:") + f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def clip_video_bysrt(self,input_video,input_srt,temp_folder):

        style = ''
        sub_format = input_srt.split('.')[-1]
        voice_dir = 'voice'
        # 获取filename

        file = os.path.basename(input_video)
        filename, format = os.path.splitext(file)  # haruhi_01 .mkv
        print(filename)
        print(voice_dir)
        # 创建对应的音频文件夹
        os.makedirs(f'{temp_folder}/{filename}/{voice_dir}', exist_ok=True)
        print(f'{temp_folder}/{filename}/{voice_dir}')
        # 检测字幕编码
        encoding = detect_encoding(input_srt)

        if sub_format == 'srt':
    
            srt_file = pysrt.open(input_srt, encoding=encoding)
            for index, subtitle in enumerate(tqdm(srt_file[:], 'video clip by srt file start')):
                # 获取开始和结束时间
                start_time = subtitle.start
                end_time = subtitle.end
                start_time = start_time.to_time()
                end_time = end_time.to_time()
                text = make_filename_safe(subtitle.text)
                if text:
                    index = str(index).zfill(4)

                    ss = str(start_time)
                    if len(ss) == 8:
                        ss += '.000'
                    ee = str(end_time)
                    if len(ee) == 8:
                        ee += '.000'
                    ss = ss.ljust(12, '0')[:12]
                    ee = ee.ljust(12, '0')[:12]

                    name = f'{index}_{ss}_{ee}_{text}'.replace(':', '.')

                    # 使用FFmpeg切割视频
                    audio_output = f'{temp_folder}/{filename}/{voice_dir}/{name}.wav'
                    self.ffmpeg_extract_audio(input_video, audio_output, start_time, end_time)
    
        elif sub_format == 'ass':
            # print("this is ass")
            subs = pysubs2.load(input_srt, encoding=encoding)
            if not style:
                style_lis = [sub.style for sub in subs]
                most_1 = most_common_element(style_lis)
                style = most_1[0][0]  
            new_subs = [sub for sub in subs if sub.style == style]
            for index, subtitle in enumerate(new_subs[:]):
                # print(index, subtitle)
                # 获取开始和结束时间
                if subtitle.style == style:
                    text = make_filename_safe(subtitle.text)
                    if text:
                        start_time = subtitle.start
                        end_time = subtitle.end
                        start_time = start_time / 1000
                        end_time = end_time / 1000

                        ss = self.srt_format_timestamp(start_time)
                        ee = self.srt_format_timestamp(end_time)
                        index = str(index).zfill(4)
                        name = f'{index}_{ss}_{ee}_{text}'.replace(':', '.')
                        # 使用FFmpeg切割视频
                        index = str(index).zfill(4)

                        audio_output = f'{temp_folder}/{filename}/{voice_dir}/{name}.wav'
                        print(audio_output)
                        self.ffmpeg_extract_audio(input_video, audio_output, start_time, end_time)
        # exit()



def crop(args):

    if args.verbose:
        print('runing crop')

    # checking if annotate_map is a file
    if not os.path.isfile(args.annotate_map):
        print(f'annotate_map {args.annotate_map} is not exist')
        return

    # checking if role_audios is a folder
    if not os.path.isdir(args.role_audios):
        print(f'role_audios {args.role_audios} is not exist')
        # create role_audios folder
        os.mkdir(args.role_audios)

    data = pd.read_csv(args.annotate_map)
    video_pth_segmentor = video_Segmentation()
    audio_feature_extractor = AudioFeatureExtraction()
    for index, (annotate_csv,video_pth) in data.iterrows():
        # clip audio segement according to the subtile file timestamp ; output: *.wav
        # the subtile file has been labeled by role, here is a .csv format file
        video_pth_segmentor.clip_audio_bycsv(annotate_csv, video_pth, args.role_audios)

        # audio feature extract wav→pkl
        video_pth_segmentor.extract_pkl_feat(audio_feature_extractor,args.role_audios)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract audio by subtitle time stamp',
        epilog='author:fengyunzaidushi(https://github.com/fengyunzaidushi)'
    )
    # video_pth, role_audios, annotate_csv
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--annotate_map', default='./input_folder/haruhi_EP3_annotate_map.csv', type=str, required=True, help="list of video_pth and subtitle paths")
    parser.add_argument('--role_audios', default='./input_folder/role_audios', type=str, required=True, help= "audio directories and feature directories categorized by role") # Better change it to your own path
    # parser.add_argument('--model_directory', default='./audio_feature_ext/models', type=str, required=False, help= "huggine face model weight download pth")

    args = parser.parse_args()
    parser.print_help()
    # print(args)
    crop(args)

"""
cd yuki_builder/
python verbose=True 
        --annotate_map ./input_folder/haruhi_EP3_annotate_map.csv'
        --role_audios ./input_folder/role_audios          # Better change it to your own path
"""
