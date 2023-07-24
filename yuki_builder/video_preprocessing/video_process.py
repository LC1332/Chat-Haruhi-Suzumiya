from .uvr5 import uvr_prediction, uvr5_names
from argparse import Namespace
import os
import shutil
import argparse

def run_bgm_remover(args: Namespace):

    # checking if input_file is a file
    if not os.path.isfile(args.input_file):
        print('input_file is not exist')
        return

    # checking if opt_vocal_root is a folder
    if not os.path.isdir(args.opt_vocal_root):
        print('warning opt_vocal_root is not exist')
        # create opt_vocal_root
        shutil.rmtree(args.opt_vocal_root, ignore_errors=True)
        os.makedirs(args.opt_vocal_root, exist_ok=True)
        print('create folder', args.opt_vocal_root)
    # checking if opt_ins_root is a folder
    if not os.path.isdir(args.opt_ins_root):
        print('warning opt_ins_root is not exist')
        # create opt_ins_root
        shutil.rmtree(args.opt_ins_root, ignore_errors=True)
        os.makedirs(args.opt_ins_root, exist_ok=True)
        print('create folder', args.opt_ins_root)

    # 人声提取激进程度
    agg = 10
    # format
    format0 = ["wav", "flac", "mp3", "m4a"]
    vocal_path, others_path = uvr_prediction(uvr5_names[5], args.input_file,
                                             args.opt_vocal_root,
                                             args.opt_ins_root,
                                             agg,
                                             format0[0]
                                             )

    return  vocal_path, others_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='uvr5 processing of vocal accompaniment separation'
    )
    parser.add_argument('--input_file', default='input_file', type=str, required=True, help="source path")
    parser.add_argument('--opt_vocal_root', default='out_folder', type=str,  help="vocal path")
    parser.add_argument('--opt_ins_root', default='out_folder', type=str,  help="instrument path")
    args = parser.parse_args()
    parser.print_help()
    run_bgm_remover(args)
