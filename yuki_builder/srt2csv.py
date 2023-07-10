import argparse
import os

def srt2csv(args):

    if args.verbose:
        print('runing srt2csv')

    # checking if input_srt is a file
    if not os.path.isfile(args.input_srt):
        print('input_srt is not exist')
        return
    
    # checking if srt_folder is a folder
    if not os.path.isdir(args.srt_folder):
        print('warning srt_folder is not exist')
        # create srt_folder
        os.mkdir(args.srt_folder)
        print('create folder', args.srt_folder)

    ## TODO: run srt2csv
    
    
    pass
