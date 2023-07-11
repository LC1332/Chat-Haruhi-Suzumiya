#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
__ToDo："whisper with speaker diarization"
__author: "Aria:(https://github.com/ariafyy)"
Speech Recognition is based on models from OpenAI Whisper
Speaker diarization model and pipeline from by pyannote
inspired by vumichien
"""

from faster_whisper import WhisperModel
import datetime
import pandas as pd
import time
import os
import pathlib
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import torch
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
import filetype
import wave
import contextlib
from transformers import pipeline

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class UtilsTranscribe(object):
    def __init__(self):
        pass

    def convert_time(self, secs):
        return datetime.timedelta(seconds=round(secs))

    def _file_kind(self, file_mime):
        # 找到最后一个 "/" 的索引
        index = file_mime.rfind("/")
        # 如果找到了，则返回 "/" 前面的字符，否则返回原始字符串
        if index != -1:
            file_kind = file_mime[:index]
            return file_kind
        else:
            return file_mime

    def get_file_format(self, upload_file_path):
        kind = filetype.guess(upload_file_path)
        if kind is None:
            print('Cannot guess file type!')
            return
        # print('File extension: %s' % kind.extension)
        # print('File MIME type: %s' % kind.mime)
        file_format = self._file_kind(kind.mime)
        # print('File mime: %s' % file_format)
        return file_format

    def upload_file_preprocessing(self, upload_file_path):
        if (upload_file_path == None):
            raise ValueError("Error no file input")
        file_format = self.get_file_format(upload_file_path)
        # print('File mime: %s' % file_format)
        if file_format == "video":
            try:
                # Read and convert video
                _, file_ending = os.path.splitext(f'{upload_file_path}')
                # print(f'file enging is {file_ending}')
                audio_file = upload_file_path.replace(file_ending, ".wav")
                # print("starting conversion to wav")
                if os.path.exists(audio_file):
                    print(audio_file, "has exist!!!")
                else:
                    os.system(f'ffmpeg -i "{upload_file_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{audio_file}"')
                # os.system(f'ffmpeg -i "{upload_file_path}" -ar 16000 -ac 1 "{audio_file}"')
                return audio_file
            except Exception as e:
                raise RuntimeError("Error converting video to audio")
        if file_format == "audio":
            audio_file = upload_file_path
            return audio_file


class FastWhipserSpeaker(object):
    def __init__(self):
        self.embedding_model = PretrainedSpeakerEmbedding(
            "speechbrain/spkrec-ecapa-voxceleb",
            device=DEVICE)

    def get_audio_duration(self, audio_file):
        with contextlib.closing(wave.open(audio_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        print(f"audio duration: {duration}")
        return duration

    def segment_embedding(self, segment, duration, audio_file):
        audio = Audio()
        start = segment["start"]
        end = min(duration, segment["end"])
        clip = Segment(start, end)
        waveform, sample_rate = audio.crop(audio_file, clip)
        return self.embedding_model(waveform[None])

    def find_best_num_speakers(self, num_speakers, embeddings):
        if num_speakers == 0:
            score_num_speakers = {}
            for num_speakers in range(2, 10 + 1):
                clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
                score = silhouette_score(embeddings, clustering.labels_, metric='euclidean')
                score_num_speakers[num_speakers] = score
            best_num_speaker = max(score_num_speakers, key=lambda x: score_num_speakers[x])
            print(
                f"The best number of speakers: {best_num_speaker} with {score_num_speakers[best_num_speaker]} score")
        else:
            best_num_speaker = num_speakers
        return best_num_speaker

    def get_speaker_label(self, best_num_speaker, embeddings, segments):
        clustering = AgglomerativeClustering(best_num_speaker).fit(embeddings)
        labels = clustering.labels_
        for i in range(len(segments)):
            segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)
        objects = {
            'Start': [],
            'End': [],
            'Speaker': [],
            'Text': []
        }
        text = ''
        for (i, segment) in enumerate(segments):
            if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
                objects['Start'].append(str(UtilsTranscribe().convert_time(segment["start"])))
                objects['Speaker'].append(segment["speaker"])
                if i != 0:
                    objects['End'].append(str(UtilsTranscribe().convert_time(segments[i - 1]["end"])))
                    objects['Text'].append(text)
                    text = ''
            text += segment["text"] + ' '
        objects['End'].append(str(UtilsTranscribe().convert_time(segments[i - 1]["end"])))
        objects['Text'].append(text)
        return objects

    def transcribe_w_speaker(self, input_file: str, lang: str, MODEL_WHISPER: str, task: str, num_speakers: int,
                             out_transcript_dir):
        time_start = time.time()
        try:
            audio_file = UtilsTranscribe().upload_file_preprocessing(input_file)
            duration = self.get_audio_duration(audio_file)
            self.MODEL_NAME = "openai/whisper-" + MODEL_WHISPER
            self.pipe = pipeline(
                task="automatic-speech-recognition",
                model=self.MODEL_NAME,
                chunk_length_s=30,
                device=DEVICE,
            )
            self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language=lang,
                                                                                                   task=task)
            #  compute_type="int8_float16")
            model = WhisperModel(MODEL_WHISPER, device="auto", compute_type="int8")
            segments_raw, info = model.transcribe(audio_file,
                                                  task=task,
                                                  language=lang,
                                                  beam_size=5,
                                                  best_of=5,
                                                  vad_filter=True,
                                                  )

            segments = []
            i = 0
            for segment_chunk in segments_raw:
                chunk = {}
                chunk["start"] = segment_chunk.start
                chunk["end"] = segment_chunk.end
                chunk["text"] = segment_chunk.text
                segments.append(chunk)
                i += 1
            print("transcribe done")
        except Exception as e:
            raise RuntimeError("Error converting video to audio")

        try:

            embeddings = np.zeros(shape=(len(segments), 192))
            for i, segment in enumerate(segments):
                embeddings[i] = self.segment_embedding(segment, duration, audio_file)
            embeddings = np.nan_to_num(embeddings)
            best_num_speaker = self.find_best_num_speakers(num_speakers, embeddings)
            objects = self.get_speaker_label(best_num_speaker, embeddings, segments)
            time_end = time.time()
            print("time cost:", time_end - time_start)
            df_results = pd.DataFrame(objects)
            os.makedirs(out_transcript_dir, exist_ok=True)
            out_transcript_path = out_transcript_dir + pathlib.Path(input_file).stem + ".csv"
            print("out_transcript_path:", out_transcript_path)
            df_results.to_csv(out_transcript_path, index=False)
            print("\n", df_results.head())
            return df_results, out_transcript_path

        except Exception as e:
            raise RuntimeError("Error Running inference with local model", e)


if __name__ == '__main__':
    """
           Start      End    Speaker                        Text
    0  0:00:01  0:00:08  SPEAKER 1  大熊怎么了 为什么你不吃呢 我记得你很喜欢吃樱桃啊 
    1  0:00:08  0:00:10  SPEAKER 4                    我现在还不上吃 
    2  0:00:11  0:00:15  SPEAKER 3           你不吃啊 你不吃的话那天给我吃吧
    3  0:00:15  0:00:18  SPEAKER 2            哆啦啊梦你很无情耶， 怎么都不担心 
    4  0:00:18  0:00:21  SPEAKER 4        我为什么不想吃 我是关心我是不是没吃鱼 
    """
    input_video = "demo.mp4"
    inwav_path = "demo.wav"
    input_file = inwav_path # 支持视频或者语音输入
    out_transcript_dir = "/outputs/"
    WHISPER_MODELS = ["tiny", "base", "small", "medium", "large-v1", "large-v2"]
    MODEL_WHISPER = "tiny"
    lang = "zh"
    num_speakers = 4
    FastWhipserSpeaker().transcribe_w_speaker(input_file,
                                              lang=lang,
                                              MODEL_WHISPER=MODEL_WHISPER,
                                              task="transcribe",
                                              num_speakers=num_speakers,
                                              out_transcript_dir=out_transcript_dir)
