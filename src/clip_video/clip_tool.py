import os
import subprocess
import pysrt

import re

from typing import List
from datetime import timedelta


class SubtitleInfo:
    def __init__(self, start_time: str, end_time: str, text: str, file_name: str):
        self.start = start_time
        self.end = end_time
        self.text = text
        self.file_name = file_name

def get_ass_subtitle_infos(data: List[str]) -> List[SubtitleInfo]:
    subtitle_infos = []
    dd = 0
    for line in data:
        if "zhengwen" in line and line.startswith("Dialogue"):
            info = line.split(": ")[1].split(',')
            print(f"start: {info[1]}, end: {info[2]} text: {info[9]}")
            subtitle_infos.append(SubtitleInfo(
                start_time=info[1][2:],
                end_time=info[2][2:],
                text=info[9],
                file_name=f"{dd}.wav",
            ))

            # 取中间时间作为关键帧
            dd += 1

    return subtitle_infos


def make_filename_safe(filename):
    # 将非法字符替换为下划线
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # 去除多余的空格
    filename = re.sub(r'\s+', ' ', filename)
    # 去除开头和结尾的空格
    filename = filename.strip()
    return filename


for file in os.listdir('video'):
    subtitle_file_name = "name.ass"
    print(file)
    # 获取视频文件名
    filename = os.path.splitext(file)[0]
    print(filename)
    # 创建对应的音频文件夹
    os.makedirs(f'audio_output/{filename}', exist_ok=True)
    if subtitle_file_name.endswith(".ass"):
        subtitle_type = "ass"

        f = open(subtitle_file_name, "r") 
        subtitle_file = get_ass_subtitle_infos(f.readlines())
    elif subtitle_file_name.endswith(".srt"):
        subtitle_type = "srt"

    # 获取对应字幕
        subtitle_file = pysrt.open(f'srt/{filename}.srt')
    else:
        # 未知文件
        exit()

    for index, subtitle in enumerate(subtitle_file):
        if subtitle_type == "ass":
            start_time = subtitle.start
            end_time = subtitle.end
        elif subtitle_file == "srt":
        # 获取开始和结束时间
            start_time = subtitle.start.to_time()
            end_time = subtitle.end.to_time()

        print(f'开始时间：{start_time}，结束时间：{end_time}')

        # 使用FFmpeg切割视频
        audio_output = f'audio_output/{filename}/audio_{index}.mp3'
        audio_output = f'audio_output/{filename}/{index}_{make_filename_safe(subtitle.text)}.mp3'
        video_output = f'video_{index}.mp4'
        subprocess.run(['ffmpeg', '-ss', str(start_time), '-to', str(end_time), '-i', f'video/{file}', "-vn", "-acodec", "copy",
                         video_output, '-loglevel', 'quiet'])
        subprocess.run(['ffmpeg', '-i', video_output, audio_output, '-loglevel', 'quiet'])
        # subprocess.run(['ffmpeg', '-i', video_output, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', audio_output])
        # break
        # 删除临时视频文件
        os.remove(video_output)
    # break
exit()
