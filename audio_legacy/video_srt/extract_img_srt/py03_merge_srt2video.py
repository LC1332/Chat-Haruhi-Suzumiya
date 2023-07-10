# coding: utf-8
import subprocess

from read import get_filelisform
from config import SRT_CONFIG

def convert_video_with_subtitles_cpu(input_file, subtitles_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"subtitles={subtitles_file}",
        "-c:v", "libx264",
        "-crf", "18",
        "-c:a", "copy",
        "-c:s", "copy",
        output_file
    ]
    subprocess.run(command)


def convert_video_with_subtitles_gpu(input_file, subtitles_file, output_file):
    command = [
        "ffmpeg",
        "-hwaccel", "cuda",  # 启用CUDA硬件加速
        "-i", input_file,
        "-vf", f"subtitles={subtitles_file}",
        "-c:v", "h264_nvenc",  # 使用NVIDIA GPU进行视频编码
        "-preset", "fast",  # 设置编码速度为快速
        "-crf", "18",
        "-c:a", "copy",
        "-c:s", "copy",
        output_file
    ]
    subprocess.run(command)


# 字幕文件所在路径 自定义
srt_dir = SRT_CONFIG['srt_dir_origin']
zimu_filelis = get_filelisform(srt_dir, '.ass')
zimu_filelis.sort()

# 原视频所在路径
video_dir = SRT_CONFIG['video_origin']
video_format = SRT_CONFIG['video_format']
srt_video_format = SRT_CONFIG['srt_video_format']

video_filelis = get_filelisform(video_dir, video_format) # 通过后缀 获取原视频
video_filelis.sort()

# 单个视频 字幕压制到视频中 命令行模式
# ffmpeg -i Haruhi_01.mkv -vf "subtitles=Haruhi_01.ass" -c:v libx264 -crf 18 -c:a copy -c:s copy  Haruhi_01_srt.mkv

# 批量字幕和视频 压制
for subtitles_file, input_file in zip(zimu_filelis[:], video_filelis[:]):
    output_file = input_file.replace(video_format, srt_video_format) # 输出压制了字幕的视频还在原文件夹中，仅仅添加了后缀 _srt
    # 如果没有gpu 选择convert_video_with_subtitles_cpu
    convert_video_with_subtitles_gpu(input_file, subtitles_file, output_file)
