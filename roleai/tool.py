
import os

#获取子目录
def get_subdir(directory):
    subdirectories = []
    for dirpath, dirnames, files in os.walk(directory):
        for dirname in dirnames:
            subdirectories.append(os.path.join(dirpath, dirname))
    subdirectories.sort()
    return subdirectories

def get_filename(directory,format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if format:
                if file.endswith(format):
                    file_path = os.path.join(root, file)
                    file_list.append([file,file_path])
            else:
                file_path = os.path.join(root, file)
                file_list.append([file, file_path])
    file_list.sort()
    return file_list


#获取一级子目录
def get_first_subdir(directory):
    subdirectories = []
    for name in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, name)):
            subdirectories.append(os.path.join(directory, name))
    subdirectories.sort()
    return subdirectories