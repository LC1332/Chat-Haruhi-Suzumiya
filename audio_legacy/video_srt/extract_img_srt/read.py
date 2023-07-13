# coding=utf-8
import os

#获取文件夹下 所有文件路径
def get_filelisform(directory, format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if format:
                if file.endswith(format):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
            else:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


#获取文件夹下所有文件路径和名称
def get_filename(directory, format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if format:
                if file.endswith(format):
                    file_path = os.path.join(root, file)
                    file_list.append([file, file_path])
            else:
                file_path = os.path.join(root, file)
                file_list.append([file, file_path])
    return file_list


# 把一个字符串写入到文本文件
def write_to_file(file, line):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(line + '\n')


# 把一个字典当作文本文件写入
def read_bigone(file):
    with open(file, 'r', encoding='utf-8') as f:
        line = f.readline()
        line = eval(line.strip())
    return line
