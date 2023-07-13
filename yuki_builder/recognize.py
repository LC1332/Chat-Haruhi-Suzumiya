import argparse
import os

def recognize(args):

    if args.verbose:
        print('runing recognize')

    # checking if input_video is a file
    if not os.path.isfile(args.input_video):
        print('input_video is not exist')
        return
    
    # checking if input_srt is a file
    if not os.path.isfile(args.input_srt):
        print('input_srt is not exist')
        return
    
    # checking if role_audios is a folder
    if not os.path.isdir(args.role_audios):
        print('role_audios is not exist')
        return
    
    # checking if output_folder is a folder
    if not os.path.isdir(args.output_folder):
        print('warning output_folder is not exist')
        # create output_folder
        os.mkdir(args.output_folder)
        print('create folder', args.output_folder)

    
    pass
