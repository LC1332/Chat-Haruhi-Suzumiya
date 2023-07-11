import argparse

import os

def run_whisper(args):

    if args.verbose:
        print('runing whisper')

    # checking if input_video is a file
    if not os.path.isfile(args.input_video):
        print('input_video is not exist')
        return
    
    # checking if srt_folder is a folder
    if not os.path.isdir(args.srt_folder):
        print('warning srt_folder is not exist')
        # create srt_folder
        os.mkdir(args.srt_folder)
        print('create folder', args.srt_folder)

    ## TODO: run whisper

    pass
