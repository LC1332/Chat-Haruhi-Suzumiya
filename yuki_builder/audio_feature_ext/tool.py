
import os
from collections import Counter
#写一个读取文本文件到列表并返回列表的函数
def read_tolist(file,encoding='utf-8'):
    with open(file,'r',encoding=encoding) as f:
        lines = f.readlines()
        lines = [item.strip() for item in lines if item.strip()]
    return lines


#获取一级子目录
def get_first_subdir(directory):
    subdirectories = [os.path.abspath(os.path.join(directory, name)) for name in os.listdir(directory) if
                      os.path.isdir(os.path.join(directory, name))]
    return subdirectories

def get_onedir(directory):
    subdirectories = next(os.walk(directory))[1]
    subdirectories.sort()
    return subdirectories

#获取子目录
def get_subdir(folder_path):
    subdirectories = [os.path.abspath(os.path.join(folder_path, name)) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    return subdirectories

def most_pre_ele(lst,num=1):
    counter = Counter(lst)
    pre_lis = counter.most_common(num)
    pre_ele = counter.most_common(num)[0][0]
    return pre_lis,pre_ele

def get_filelist(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.startswith('.') and os.path.isfile(file_path):
                file_list.append(file_path)
    file_list.sort()
    return file_list


def get_filelisform(directory,format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.startswith('.') and os.path.isfile(file_path):
                if format:
                    if file.endswith(format):
                        file_list.append(file_path)
                else:
                    file_list.append(file_path)
    file_list.sort()
    return file_list


#把一个字典当作文本文件写入
def read_bigone(file):
    with open(file,'r',encoding='utf-8') as f:
        line = f.readline()
        line = eval(line.strip())

    return line

def get_filename(directory,format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.startswith('.') and os.path.isfile(file_path):
                if format:
                    if file.endswith(format):
                        file_list.append([file,file_path])
                else:
                    file_list.append([file, file_path])
    file_list.sort()
    return file_list





def write_to_file(file,line,mode='w'):
    with open(file,mode=mode,encoding='utf-8') as f:
        f.write(line+'\n')


#把一个列表写入到文本文件
def save_lis2txt(file,lines):
    with open(file,'w',encoding='utf-8') as f:
        for line in lines:
            f.write(str(line)+'\n')