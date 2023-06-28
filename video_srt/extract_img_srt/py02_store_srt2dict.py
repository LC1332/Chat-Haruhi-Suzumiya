# coding: utf-8
import math
import re
from collections import Counter
import pysubs2
from read import get_filename,write_to_file
from config import SRT_CONFIG

def contains_japanese(text):
    pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\uFF65-\uFF9F]')
    match = re.search(pattern, text)
    return bool(match)


def begin_start(text):
    pattern = re.compile(r'^[(\[{]')
    match = re.search(pattern, text)
    return bool(match)


def convert_ms_to_timestamp(ms):
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    milliseconds = ms % 1000

    milliseconds = "%02d" % (milliseconds // 10)
    timestamp = f"{hours:01d}:{minutes:02d}:{seconds:02d}.{milliseconds}"
    return timestamp


def extract_chinese_subtitles(subtitle):
    chinese_line = re.findall(r'[\u4e00-\u9fff]+', subtitle)
    if chinese_line and not contains_japanese(subtitle) and not begin_start(subtitle):
        subtitle = re.sub(r'{.*?}', '', subtitle)
        chinese_line = re.findall(r'[\u4e00-\u9fff]+', subtitle)
        text = ''.join(chinese_line)
        return text
    else:
        return None


def exist_middle_integer(a, b):
    int_a = math.ceil(a)
    int_b = math.floor(b)

    return int_a != int_b


def find_middle_integer(a, b):
    int_a = math.ceil(a)
    int_b = math.floor(b)

    if int_a == int_b:
        return None  # 没有整数存在

    min_val = min(int_a, int_b)
    max_val = max(int_a, int_b)

    num_integers = max_val - min_val - 1

    middle_integer = min_val + math.ceil(num_integers / 2)

    return middle_integer


def count_element_frequency(lst):
    counter = Counter(lst)
    sorted_items = counter.most_common(10)
    return sorted_items


def ge_half(decimal):
    return decimal % 1 >= 0.5


if __name__ == '__main__':

    # 某一部动漫的所有字幕文件 ，已转化为utf8编码 自定义
    directory = SRT_CONFIG['srt_dir_origin']+ '_utf8' # or SRT_CONFIG['srt_dir_utf8']
    file_lis = get_filename(directory, '.ass')
    file_lis.sort(key=lambda x: x[0])

    # 主要提取字幕的正文，开头和片尾曲还有一些注释类的字幕不提取
    # style_lis = ['zhengwen', 'Default']
    srt_style = SRT_CONFIG['srt_style']

    # 某一部动漫所有分集 存储在总字典中
    all_dic = {}
    for idx, (name, file_name) in enumerate(file_lis[:]):
        subs = pysubs2.load(file_name)
        video_name = str(idx+1).zfill(2)
        jilu_lis = []

        # 每一集动漫储存在一个字典中
        new_dic = {}
        best_lis = []
        not_exist_mid_lis = []
        for sub in subs:
            if sub.style == srt_style:  # 这里要根据字幕文件中的styel选择
                content = extract_chinese_subtitles(sub.text)
                if content:
                    start, end, text = sub.start / 1000, sub.end / 1000, sub.text
                    mid = (start + end) / 2
                    mid = round(mid, 2)

                    # 获取某一个字幕 开始和结束的平均时间 单位s
                    best_num = round(mid)
                    id = str(best_num).zfill(4)
                    if jilu_lis:
                        if start > jilu_lis[-1]:
                            jilu_lis.extend([start, end])
                            if best_num not in best_lis:
                                best_lis.append(best_num)
                                new_dic[id] = text

                    else:
                        jilu_lis.extend([start, end])
                        if best_num not in best_lis:
                            best_lis.append(best_num)
                            new_dic[id] = text
        all_dic[video_name] = new_dic

    # 验证效果
    for k, new_dic in all_dic.items():
        print(k)
        for key in list(new_dic.keys())[:10]:
            print(key, new_dic[key])

    # 自定义输出路径
    write_to_file(SRT_CONFIG['srt_dic_file'], str(all_dic))
    # 如果输出的文件内容为空，检查style的值是否正确