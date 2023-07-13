#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
__info："convert video into subtitles with Whisper(py>=3.9)"
__author:"Aria:(https://github.com/ariafyy)"
"""

import ffmpeg
import tempfile
import torch
import whisper
from whisper.utils import get_writer
from typing import Iterator, TextIO


class Video2Subtitles(object):
    def __init__(self):
        pass

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
                # f"{count}\n"
                f"{self.srt_format_timestamp(segment['start'])} --> {self.srt_format_timestamp(segment['end'])}\n"
                f"{segment['text'].replace('-->', '->').strip()}\n",
                file=file,
                flush=True,
            )

    def transcribe(self, input_video: str, lang: str, MODEL_WHISPER: str, task: str, subtitle_format: str,
                   AddSrtToVideo: bool):
        """

        Parameters
        ----------
        input_video:
        lang: language of your input file
        MODEL_WHISPER: tiny/small /base/large,you can also download into your local path  eg. /tiny.pt
        task: transcribe/translate(any language to english)
        subtitle_format:"txt", "vtt", "srt", "tsv",  "json",
        AddSrtToVideo:

        Returns
        -------
        }
        """
        DEVICE = torch.cuda.is_available()
        model = whisper.load_model(MODEL_WHISPER)
        input_video_ = input_video if isinstance(input_video, str) else input_video.name
        result = model.transcribe(
            input_video_,
            task=task,
            language=lang,
            verbose=True,
            initial_prompt=None,
            word_timestamps=False,
            fp16=DEVICE
        )
        subtitle_file = input_video_.rsplit(".", 1)[0] + "." + subtitle_format
        print("subtitle_file:", subtitle_file)
        writer = get_writer(subtitle_format, str(tempfile.gettempdir()))
        writer(result, subtitle_file)
        if subtitle_format == "srt":
            with open(subtitle_file, "w") as srt:
                self.write_srt(result["segments"], file=srt)
        if AddSrtToVideo:
            return self.add_srt_to_video(input_video_, subtitle_file)
        return subtitle_file

    def add_srt_to_video(self, input_video_, subtitle_file):
        video_out = input_video_ + "_output.mp4"
        input_ffmpeg = ffmpeg.input(input_video_)
        input_ffmpeg_sub = ffmpeg.input(subtitle_file)
        input_video = input_ffmpeg['v']
        input_audio = input_ffmpeg['a']
        input_subtitles = input_ffmpeg_sub['s']
        stream = ffmpeg.output(
            input_video, input_audio, input_subtitles, video_out,
            vcodec='copy', acodec='copy', scodec=subtitle_format
        )
        stream = ffmpeg.overwrite_output(stream)
        ffmpeg.run(stream)
        return video_out


if __name__ == '__main__':
    input_video = "input.mp4"
    MODEL_WHISPER = "tiny or your downloaded model path"
    lang = "zh"
    task = "transcribe"
    AddSrtToVideo = False
    subtitle_format = "srt"
    Video2Subtitles().transcribe(input_video, lang, MODEL_WHISPER, task, subtitle_format, AddSrtToVideo)
