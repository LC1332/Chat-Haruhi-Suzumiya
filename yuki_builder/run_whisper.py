#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
__ToDo："transcribe video to srt via OpenAI Whisper "
__author: "Aria:(https://github.com/ariafyy)"
"""


import argparse
import os
import pathlib
import torch
from typing import Iterator, TextIO
try:
    import whisper
except ImportError:
    print("check requirements: yuki_builder/requirements_run_whisper.txt")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from hanziconv import HanziConv


class Video2Subtitles(object):
    def __init__(self):
        MODEL_WHISPER = "medium"  # or your local model_path
        WHISPER_MODELS = ["tiny", "base", "small", "medium", "large-v1", "large-v2"]
        print("---loading model in your local path or downloading now---")
        self.model = whisper.load_model(MODEL_WHISPER)

    def srt_format_timestamp(self, seconds: float):
        assert seconds >= 0, "non-negative timestamp expected"
        milliseconds = round(seconds * 1000.0)

        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000

        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000

        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000

        return (f"{hours}:") + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def write_srt(self, transcript: Iterator[dict], file: TextIO):
        count = 0
        for segment in transcript:
            count += 1
            print(
                f"{self.srt_format_timestamp(segment['start'])} --> {self.srt_format_timestamp(segment['end'])}\n"
                f"{self.trad2simp(segment['text']).replace('-->', '->').strip()}\n",
                file=file,
                flush=True,
            )

    def trad2simp(self,text):
        """
        # traditional chinese into simplified chinese
        :param text: 
        :return: 
        """
        simp = HanziConv.toSimplified(text)
        return simp

    def transcribe(self, input_video: str, srt_folder: str):
        subtitle_format = "srt"
        lang = "zh"
        verbose = True
        DEVICE = torch.cuda.is_available()
        model = self.model
        input_video_ = input_video if isinstance(input_video, str) else input_video.name
        result = model.transcribe(
            input_video_,
            task="transcribe",
            language=lang,
            verbose=verbose,
            initial_prompt=None,
            word_timestamps=True,
            no_speech_threshold=0.95,
            fp16=DEVICE
        )
        os.makedirs(srt_folder, exist_ok=True)
        subtitle_file = srt_folder + "/" + pathlib.Path(input_video).stem + "." + subtitle_format
        if subtitle_format == "srt":
            with open(subtitle_file, "w") as srt:
                self.write_srt(result["segments"], file=srt)
        print("\nsubtitle_file:", subtitle_file, "\n")
        return subtitle_file


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

    # run whisper
    input_file = args.input_video
    srt_folder = args.srt_folder
    result = Video2Subtitles().transcribe(input_file, srt_folder)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='video to chinese srt with medium ',
        epilog='author:Aria(https://github.com/ariafyy)'
    )
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--input_video', default='input_file', type=str, required=True, help="video path")
    parser.add_argument('--srt_folder', default='out_folder', type=str, required=True, help="srt path")
    args = parser.parse_args()
    parser.print_help()
    run_whisper(args)