"""
Covert .ass or .srt subtitles to a 4 columns .csv file
"""
import argparse
import os
import pathlib
import csv
import ass
import re

HAS_CHINESE = False
def srt2csv(args):
    if args.verbose:
        print('runing srt2csv')

    # checking if srt_folder is a folder
    if not os.path.isdir(args.srt_folder):
        print('warning: the folder{} is not exist'.format(args.srt_folder))
        # create srt_folder
        os.makedirs(args.srt_folder)
        print('create folder', args.srt_folder)

    # checking if input_srt is a file
    input_srt_file = args.input_srt
    output_folder = args.srt_folder
    if not os.path.isfile(input_srt_file):
        print('Error: The input file {} is not exist'.format(input_srt_file))
        return
    
    # checking if input_srt is a srt_file
    if not (pathlib.Path(input_srt_file).suffix == '.srt' or pathlib.Path(input_srt_file).suffix == '.ass'):
        print('Error: The input file {} must be a .srt or .ass file'.format(input_srt_file))
        return
    convert(input_srt_file, output_folder, True)

#create csv file
def render_csv(final_result, csv_file):
    if os.path.exists(csv_file):
        os.remove(csv_file)
    with open(csv_file, 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["空白","内容","开始时间","结束时间"])
        for i in final_result:    
            if not (i["Text"] and i["TimecodeIn"] and i["TimecodeOut"]):
                #print(i)
                continue
            writer.writerow(['',i["Text"],i["TimecodeIn"],i["TimecodeOut"]])
    return

def is_japenese(line):
    #unicode japanese katakana 
    re_words_1 = re.compile(u"[\u30a0-\u30ff]+") 
    #unicode japanese hiragana 
    re_words_2 = re.compile(u"[\u3040-\u309f]+") 
    m_1 = re_words_1.search(line, 0) 
    m_2 = re_words_2.search(line, 0) 
    if m_1 or m_2:
        # print(line)
        return True
    return False
 
#parse srt
def internalise(lines, keep_japanese):
    result = []
    GET_TEXT = 1
    WAITING = 2
    cue = 0	
    current_state = WAITING
    start_time = ""
    prev_start_time = ""
    prev_end_time = ""
    end_time = ""
    text = ""
    text_line = 0
    current_cue = {}
    for line in lines:
        line = line.strip()
        if "-->" in line:
            cue += 1
            start_time = line.split('-->')[0].strip()
            end_time = line.split('-->')[1].strip()
            #del duplicated interval
            # if start_time == prev_start_time and end_time == prev_end_time:
            #     continue
            # prev_start_time = start_time
            # prev_end_time = end_time
            current_state = GET_TEXT
            text_line = 0
            current_cue["TimecodeIn"] = start_time
            current_cue["TimecodeOut"] = end_time
            continue
        if line == "" or (is_japenese(line) and not keep_japanese): 
            current_cue["Text"] = text
            result.append(current_cue)
            current_cue = {}
            text = ""
            current_state = WAITING
            continue
        if current_state == GET_TEXT:
            if text_line == 0:
                text += line
                text_line += 1
            else:
                text += " " + line
    if current_state == GET_TEXT:
        current_cue["Text"] = text
        result.append(current_cue)
    return result

#read srt file
def read_srt(input_file):
    try:
        file1 = open(input_file, 'r',encoding='utf-8')
        lines = file1.readlines()
        file1.close()
    except Exception as error:
        print(error)
        exit()	
    return lines

#parse ass
def parse_ass(input_file):     
    with open(input_file, encoding='utf-8-sig') as f:
        s = ass.parse(f)
    result = []
    for line in s.events:
        result.append({
        'TimecodeIn': line.start,
        'TimecodeOut': line.end,
        'Text': line.fields['Text']
        })
    return result

def convert(input_srt_file, output_folder, keep_japanese):
    os.makedirs(output_folder, exist_ok=True)
    output_csv_file = output_folder + "/" + pathlib.Path(input_srt_file).stem + "." + 'csv'
    result = None
    if pathlib.Path(input_srt_file).suffix == '.srt':
        lines = read_srt(input_srt_file)
        result = internalise(lines, keep_japanese)     
    elif pathlib.Path(input_srt_file).suffix == '.ass':
        result = parse_ass(input_srt_file)
    render_csv(result, output_csv_file)
    return output_csv_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='convert srt/ass to CSV',
        epilog='author:LengYue(https://github.com/zealot52099)'
    )
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--srt_folder', default='srt_folder', type=str, required=True, help="folder to output .csv files")
    parser.add_argument('--input_srt', default='input_srt', type=str, required=True, help="path of input .srt/.ass file")
    args = parser.parse_args()
    parser.print_help()
    srt2csv(args)

#python srt2csv.py --srt_folder srt_result --input_srt ./test_data/bad_case.srt verbose=True
