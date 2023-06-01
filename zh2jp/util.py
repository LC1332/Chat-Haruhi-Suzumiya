#coding=utf-8
import os


def read_tolist(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    return lines


def write_to_file(file,line,mode='w'):
    with open(file,mode,encoding='utf-8') as f:
        f.write(line+'\n')