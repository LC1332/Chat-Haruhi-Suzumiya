import os
import subprocess
import pysrt

import re

def make_filename_safe(filename):
    # 将非法字符替换为下划线
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # 去除多余的空格
    filename = re.sub(r'\s+', ' ', filename)
    # 去除开头和结尾的空格
    filename = filename.strip()
    return filename


for file in os.listdir('video'):
    print(file)
    # 获取视频文件名
    filename = os.path.splitext(file)[0]
    print(filename)
    # 创建对应的音频文件夹
    os.makedirs(f'audio_output/{filename}', exist_ok=True)
    # 获取对应字幕
    srt_file = pysrt.open(f'srt/{filename}.srt')
    for index, subtitle in enumerate(srt_file):
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
