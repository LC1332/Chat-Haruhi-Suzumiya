# coding: utf-8
import os.path
import chardet
import codecs
from config import SRT_CONFIG
from read import get_filename

# 检测文件编码
def detect_encoding(file_name):
    with open(file_name, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']


def convert_to_utf8(file_name, new_filename):
    # 源文件编码
    current_encoding = detect_encoding(file_name)

    if current_encoding != 'utf-8':
        # 读取源文件内容
        with codecs.open(file_name, 'r', current_encoding) as source_file:
            contents = source_file.read()
        # 源文件内容 写入新文件 utf-8 编码
        with codecs.open(new_filename, 'w', 'utf-8') as target_file:
            target_file.write(contents)



# 举例：凉宫春日1-28集 原视频字幕所在路径，编码格式是utf-16
directory = SRT_CONFIG['srt_dir_origin']


# 获取所有字幕文件路径
file_lis = get_filename(directory, '.ass')

# 创建utf-8字幕写入的文件夹
if not os.path.exists(directory + '_utf8'):
    os.mkdir(directory + '_utf8')
dir_name = directory.split('/')[-1]

# 批量转化字幕文件格式
for name, file_name in file_lis[:]:
    new_filename = file_name.replace(dir_name, f'{dir_name}_utf8')
    convert_to_utf8(file_name, new_filename)
