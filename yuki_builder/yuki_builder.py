import argparse

from run_whisper import run_whisper
from srt2csv import srt2csv
from crop import crop
from recognize import recognize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YukiBuilder')

    parser.add_argument('-verbose', action='store_true')

    subparsers = parser.add_subparsers(dest='subcommand')

    whisper_parser = subparsers.add_parser('whisper')
    whisper_parser.add_argument('-input_video', required=True)
    whisper_parser.add_argument('-srt_folder', required=True)

    srt2csv_parser = subparsers.add_parser('srt2csv')
    srt2csv_parser.add_argument('-input_srt', required=True)
    srt2csv_parser.add_argument('-srt_folder', required=True)

    crop_parser = subparsers.add_parser('crop')
    crop_parser.add_argument('-annotate_map', required=True)
    crop_parser.add_argument('-role_audios', required=True)

    recognize_parser = subparsers.add_parser('recognize')
    recognize_parser.add_argument('-input_video', required=True)
    recognize_parser.add_argument('-input_srt', required=True)
    recognize_parser.add_argument('-role_audios', required=True)
    recognize_parser.add_argument('-output_folder', required=True)

    args = parser.parse_args()

    if args.subcommand == 'whisper':
        run_whisper(args)
    elif args.subcommand == 'srt2csv':
        srt2csv(args)
    elif args.subcommand == 'crop':
        crop(args)
    elif args.subcommand == 'recognize':
        recognize(args)