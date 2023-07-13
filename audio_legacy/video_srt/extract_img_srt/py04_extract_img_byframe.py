# coding: utf-8
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from read import get_filelisform
from config import SRT_CONFIG


def extract_frame_with_timestamp(input_file, output_file):

    command = [
        "ffmpeg",
        "-hwaccel", "cuda",  # 启用CUDA硬件加速 没有gpu 把本句注销
        # "-frames", str(num_frames)
        "-i", input_file,
        "-vf", "fps=1",
        "-qscale:v", "2",
        "-s", "853x480",
        "-f", "image2",
        output_file  # 输出文件命名格式
    ]
    subprocess.run(command)


directory = SRT_CONFIG['video_origin']
srt_video_format = SRT_CONFIG['srt_video_format']
# 获取压制了字幕的视频列表  在py03中 压制了字幕的视频和原视频是同一个文件夹内
video_lis = get_filelisform(directory, srt_video_format)  # 通过后缀 获取压制了字幕的视频
num_frames = 1
video_lis.sort()  # 视频名称排序 从小到大

# 创建线程池
with ThreadPoolExecutor(max_workers=12) as executor:
    # 循环遍历视频
    for idx, input_file in enumerate(video_lis[:],1):

        out_dir = SRT_CONFIG['img_out_dir']  # 切割出的图片的总文件夹
        single_out_dir = out_dir + f'/{str(idx).zfill(2)}'  # 切割出的图片的分集文件夹 例： 01 02 03
        if not os.path.exists(single_out_dir):
            os.makedirs(single_out_dir)
        output_file = f'{single_out_dir}/%04d.jpg'  # 输出图片的格式
        # 提交任务到线程池并执行
        executor.submit(extract_frame_with_timestamp, input_file, output_file)
