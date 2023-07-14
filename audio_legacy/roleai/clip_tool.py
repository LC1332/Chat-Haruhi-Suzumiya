import os
import re
import subprocess
from collections import Counter

import chardet
import pysrt
import pysubs2
from tool import get_filename,read_bigone
from tqdm import tqdm

def detect_encoding(file_name):
    with open(file_name, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def most_common_element(lst,num=1):
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

class VideoSegmentation:
    def __init__(self, video_lis_pth,audio_out_dir,subtitle_dir):
        self.video_lis_pth = video_lis_pth
        self.audio_out_dir = audio_out_dir
        self.subtitle_dir = subtitle_dir


    def process(self):
        video_lis = get_filename(self.video_lis_pth)
        
        style = ''
        sub_format = ''
        voice_dir = 'voice'
        for file, pth in tqdm(video_lis[1:2], desc='Processing Videos'):
            name = file.split('.')[0]
            filename, format = os.path.splitext(file)
            # 创建对应的音频文件夹
            os.makedirs(f'{self.audio_out_dir}/{filename}', exist_ok=True)
            os.makedirs(f'{self.audio_out_dir}/{filename}/{voice_dir}', exist_ok=True)
        
            if self.subtitle_dir:
                if not sub_format:
                    # 选择一个字幕文件 获取字幕文件的格式和编码
                    one_subtitle_file = os.path.join(self.subtitle_dir,os.listdir(self.subtitle_dir)[0])
                    sub_file,sub_format = os.path.splitext(one_subtitle_file)
                    encoding = detect_encoding(one_subtitle_file)
        
                # 获取当前视频对应的字幕文件
                cur_sub_file = f'{self.subtitle_dir}/{filename}{sub_format}'
                # 获取对应字幕
                if sub_format == '.srt':
        
                    srt_file = pysrt.open(cur_sub_file, encoding=encoding)
                    for index, subtitle in enumerate(srt_file[:]):
                        # 获取开始和结束时间
        
                        start_time = subtitle.start
                        end_time = subtitle.end
                        text = subtitle.text
                        # if text in new_dic[name]:
        
                        start_time = start_time.to_time()
                        end_time = end_time.to_time()
                        # print(f'开始时间：{start_time}，结束时间：{end_time}')

                        # 使用FFmpeg切割视频 改成mp3就无法输出
                        audio_output = f'{self.audio_out_dir}/{filename}/{voice_dir}/{index}_{make_filename_safe(subtitle.text)}.wav'

                        command = ['ffmpeg', '-ss', str(start_time), '-to', str(end_time), '-i', f'{pth}', "-vn",  '-c:a', 'pcm_s16le',
                                         audio_output,  '-loglevel', 'quiet']

                        subprocess.run(command)
                elif sub_format == '.ass':
                    subs = pysubs2.load(cur_sub_file, encoding=encoding)
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
        
        
                            # 使用FFmpeg切割视频 改成mp3就无法输出

                            audio_output = f'{self.audio_out_dir}/{filename}/{voice_dir}/{index}_{make_filename_safe(subtitle.text)}.wav'
        
                            command = ['ffmpeg', '-ss', str(start_time), '-to', str(end_time), '-i', f'{pth}', "-vn",  '-c:a', 'pcm_s16le',
                                             audio_output,  '-loglevel', 'quiet']
        
                            subprocess.run(command)
        
        exit()
