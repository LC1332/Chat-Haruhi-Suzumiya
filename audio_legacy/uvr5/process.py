from MDXNet import MDXNetDereverb
from infer_uvr5 import _audio_pre_, _audio_pre_new
from config import Config
from tqdm import tqdm
import os
import traceback, pdb
import ffmpeg
import torch
import shutil
import sys

now_dir = os.getcwd()
sys.path.append(now_dir)
torch.manual_seed(114514)
tmp = os.path.join(now_dir, "TEMP")

shutil.rmtree(tmp, ignore_errors=True)
os.makedirs(tmp, exist_ok=True)


config = Config()
weight_uvr5_root = "uvr5_weights"
uvr5_names = []
for name in os.listdir(weight_uvr5_root):
    if name.endswith(".pth") or "onnx" in name:
        uvr5_names.append(name.replace(".pth", ""))


os.environ['OPENBLAS_NUM_THREADS'] = '1'


# 获取子目录
def get_subdir(folder_path):
    subdirectories = [os.path.abspath(os.path.join(folder_path, name)) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    return subdirectories


def get_filename(directory,format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.startswith('.') and os.path.isfile(file_path):
                if format:
                    if file.endswith(format):
                        file_list.append([file,file_path])
                else:
                    file_list.append([file, file_path])
    file_list.sort()
    return file_list


def uvr(model_name, inp_root, save_root_vocal, save_root_ins, agg, format0):
    infos = []
    try:
        inp_root = inp_root.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        save_root_vocal = (
            save_root_vocal.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        save_root_ins = (
            save_root_ins.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        if model_name == "onnx_dereverb_By_FoxJoy":
            pre_fun = MDXNetDereverb(onnx=f"{weight_uvr5_root}/onnx_dereverb_By_FoxJoy", chunks=15)
        else:
            func = _audio_pre_ if "DeEcho" not in model_name else _audio_pre_new
            pre_fun = func(
                agg=int(agg),
                model_path=os.path.join(weight_uvr5_root, model_name + ".pth"),
                device=config.device,
                is_half=config.is_half,
            )
        sub_dirs = get_subdir(f'{inp_root}')
        for dir in sub_dirs[:]:
            voice_files = get_filename(dir)
            name = os.path.basename(os.path.normpath(dir))
            save_ins_path = f'{save_root_ins}/instrument/{name}'

            save_vocal_path = f'{save_root_vocal}/voice/{name}'
            for file, inp_path in tqdm(voice_files, f'extract {name} uvr ,convert .wav to .wav'):
                need_reformat = 1
                done = 0
                try:
                    info = ffmpeg.probe(inp_path, cmd="ffprobe")
                    if (
                            info["streams"][0]["channels"] == 2
                            and info["streams"][0]["sample_rate"] == "44100"
                    ):
                        need_reformat = 0
                        pre_fun._path_audio_(
                            inp_path, save_ins_path, save_vocal_path, format0
                        )
                        done = 1
                except:
                    need_reformat = 1
                    traceback.print_exc()
                if need_reformat == 1:
                    tmp_path = "%s/%s.reformatted.wav" % (tmp, os.path.basename(inp_path))
                    os.system(
                        "ffmpeg -i %s -vn -acodec pcm_s16le -ac 2 -ar 44100 %s -y -loglevel error"
                        % (inp_path, tmp_path)
                    )
                    inp_path = tmp_path
                try:
                    if done == 0:
                        pre_fun._path_audio_(
                            inp_path, save_ins_path, save_vocal_path, format0
                        )
                    infos.append("%s->Success" % (os.path.basename(inp_path)))
                    yield "\n".join(infos)
                except:
                    infos.append(
                        "%s->%s" % (os.path.basename(inp_path), traceback.format_exc())
                    )
                    yield "\n".join(infos)

    except:
        infos.append(traceback.format_exc())
        yield "\n".join(infos)
    finally:
        try:
            if model_name == "onnx_dereverb_By_FoxJoy":
                del pre_fun.pred.model
                del pre_fun.pred.model_
            else:
                del pre_fun.model
                del pre_fun
        except:
            traceback.print_exc()
        print("clean_empty_cache")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    yield "\n".join(infos)

