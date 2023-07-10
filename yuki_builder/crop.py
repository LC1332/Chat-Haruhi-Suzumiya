import argparse
import os

def crop(args):

    if args.verbose:
        print('runing crop')

    # checking if annotate_map is a file
    if not os.path.isfile(args.annotate_map):
        print('annotate_map is not exist')
        return
    
    # checking if role_audios is a folder
    if not os.path.isdir(args.role_audios):
        print('role_audios is not exist')
        # create role_audios folder
        os.mkdir(args.role_audios)

    
    pass
