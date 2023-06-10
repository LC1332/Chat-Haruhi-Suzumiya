import io
import logging
import time
from pathlib import Path

import librosa
import numpy as np
import soundfile

from inference import infer_tool
from inference import slicer
from inference.infer_tool import Svc
import uuid

logging.getLogger('numba').setLevel(logging.WARNING)
# chunks_dict = infer_tool.read_temp("inference/chunks_temp.json")
infer_tool.mkdir(["./results"])
model_path = "vits_models/Haruhi_54000.pth"
config_path = "configs/config.json"
svc_model = Svc(model_path, config_path)


def set_model_path(path):
    global model_path
    model_path = path


def infer_to(spk, tran, voice):
    slice_db = -40
    
    wav_format = 'wav'
    # audio_file = io.BytesIO(voice)
    audio_file = voice
    chunks = slicer.cut(audio_file, db_thresh=slice_db)
    # audio_file = io.BytesIO(voice)
    audio_data, audio_sr = slicer.chunks2audio(audio_file, chunks)
    audio = []
    for (slice_tag, data) in audio_data:
        print(f'#=====segment start, {round(len(data) / audio_sr, 3)}s======')
        length = int(np.ceil(len(data) / audio_sr * svc_model.target_sample))
        raw_path = io.BytesIO()
        soundfile.write(raw_path, data, audio_sr, format="wav")
        raw_path.seek(0)
        if slice_tag:
            print('jump empty segment')
            _audio = np.zeros(length)
        else:
            out_audio, out_sr = svc_model.infer(spk, tran, raw_path)
            _audio = out_audio.cpu().numpy()
        audio.extend(list(_audio))
    infer_tool.mkdir(["./vits_results"])
    res_path = f'./vits_results/{tran}key_{spk}_{str(uuid.uuid4())}.{wav_format}'
    soundfile.write(res_path, audio, svc_model.target_sample, format=wav_format)

    return res_path