import argparse
import os
import pathlib
import csv

def srt2csv(args):
    if args.verbose:
        print('runing srt2csv')

    # checking if srt_folder is a folder
    if not os.path.isdir(args.srt_folder):
        print('warning srt_folder is not exist')
        # create srt_folder
        os.mkdir(args.srt_folder)
        print('create folder', args.srt_folder)

    # checking if input_srt is a file
    input_srt_file = args.input_srt
    if not os.path.isfile(input_srt_file):
        print('input_srt is not exist')
        return
    
    # checking if input_srt is a srt_file
    if not (pathlib.Path(args.input_srt).suffix == '.srt' or pathlib.Path(args.input_srt).suffix == '.ass'):
        print('input must be a srt file')
        return
  

    # # checking if csv_folder is a folder
    # if not os.path.isdir(args.csv_folder):
    #     print('warning csv_folder is not exist')
    #     # create csv_folder
    #     os.mkdir(args.csv_folder)
    #     print('create folder', args.csv_folder)
    
    convert(input_srt_file, args.srt_folder)

#create csv file
def render_csv(final_result, csv_file):
    if os.path.exists(csv_file):
        os.remove(csv_file)
    with open(csv_file, 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["空白","内容","开始时间","结束时间"])
        for i in final_result:    
            writer.writerow(['',i["Translation"],i["TimecodeIn"],i["TimecodeOut"]])
    return

#parse srt
def internalise(lines):
    cues = []
    GET_TEXT = 1
    WAITING = 2
    cue = 0	
    current_state = WAITING
    start_time = ""
    end_time = ""
    text = ""
    duration = 0
    text_line = 0
    current_cue = {}
    for line in lines:
        line = line.strip()
        if "-->" in line:
            cue += 1
            start_time = line[0:12]
            end_time = line[17:]
            current_state = GET_TEXT
            text_line = 0
            current_cue["TimecodeIn"] = start_time
            current_cue["TimecodeOut"] = end_time
            current_cue["Duration"] = duration
            continue
        if line == "":
            current_cue["Translation"] = text
            cues.append(current_cue)
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
        current_cue["Translation"] = text
        cues.append(current_cue)
    return cues

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

def convert(input_srt_file, csv_folder):
    os.makedirs(csv_folder, exist_ok=True)
    output_csv_file = csv_folder + "/" + pathlib.Path(input_srt_file).stem + "." + 'csv'
    lines = read_srt(input_srt_file)
    cues = internalise(lines)
    render_csv(cues, output_csv_file)
    return output_csv_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='convert srt to CSV',
        epilog='author:LengYue(https://github.com/zealot52099)'
    )
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--input_video', default='input_file', type=str, required=False, help="video path")
    parser.add_argument('--srt_folder', default='out_folder', type=str, required=True, help="srt path")
    parser.add_argument('--csv_folder', default='csv_folder', type=str, required=False, help="csv output path")
    parser.add_argument('--input_srt', default='input_srt', type=str, required=True, help="srt file path")
    args = parser.parse_args()
    parser.print_help()
    srt2csv(args)

#python srt2csv.py --srt_folder srt_result --input_srt news_20s.srt verbose=True