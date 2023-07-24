from .MDXNet import MDXNetDereverb
from .infer_uvr5 import _audio_pre_, _audio_pre_new
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

config = dict({
    'device': torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    # 16系/10系显卡和P40强制单精度 需要修改为False
    'is_half': True
})
weight_uvr5_root = os.path.dirname(os.path.realpath(__file__))+"/uvr5_weights"
uvr5_names = []
for name in os.listdir(weight_uvr5_root):
    if name.endswith(".pth") or "onnx" in name:
        uvr5_names.append(name.replace(".pth", ""))

os.environ['OPENBLAS_NUM_THREADS'] = '1'


# 获取子目录
def get_subdir(folder_path):
    subdirectories = [os.path.abspath(os.path.join(folder_path, name)) for name in os.listdir(folder_path) if
                      os.path.isdir(os.path.join(folder_path, name))]
    return subdirectories


def get_filename(directory, format=None):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.startswith('.') and os.path.isfile(file_path):
                if format:
                    if file.endswith(format):
                        file_list.append([file, file_path])
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
                device=config['device'],
                is_half=config['is_half'],
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


def uvr_prediction(model_name, inp_path, save_root_vocal, save_root_ins, agg, format0):
    """
    分离音频
    :param model_name: 模型名称
    :param inp_path: 输入文件
    :param save_root_vocal: 说话人保存位置
    :param save_root_ins: 伴奏保存位置
    :param agg:
    :param format0: 文件格式
    :return:
    """
    try:
        # 路径格式化
        save_root_vocal = (
            save_root_vocal.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        save_root_ins = (
            save_root_ins.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )

        # 模型加载
        if model_name == "onnx_dereverb_By_FoxJoy":
            pre_fun = MDXNetDereverb(onnx=f"{weight_uvr5_root}/onnx_dereverb_By_FoxJoy", chunks=15)
        else:
            func = _audio_pre_ if "DeEcho" not in model_name else _audio_pre_new
            pre_fun = func(
                agg=int(agg),
                model_path=os.path.join(weight_uvr5_root, model_name + ".pth"),
                device=config['device'],
                is_half=config['is_half'],
            )
        # 判断音频文件是否符合要求
        need_reformat = 1
        info = ffmpeg.probe(inp_path, cmd="ffprobe")

        if (
                'mov' in info["format"]['format_name'] or (
                    info["streams"][0]["channels"] == 2
                    and info["streams"][0]["sample_rate"] == "44100")
        ):
            need_reformat = 0

        if need_reformat == 1:
            tmp_path = "%s/%s.reformatted.wav" % (tmp, os.path.basename(inp_path))
            os.system(
                "ffmpeg -i %s -vn -acodec pcm_s16le -ac 2 -ar 44100 %s -y -loglevel error"
                % (inp_path, tmp_path)
            )
            inp_path = tmp_path

        # 处理音频
        vocal_path, others_path = pre_fun._path_audio_(
            inp_path, save_root_vocal, save_root_ins, format0
        )
        return vocal_path, others_path
    except:
        traceback.print_exc()
        return None, None
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


if __name__ == '__main__':
    # 音频说话人的输出文件
    opt_vocal_root = '/media/checkpoint/speech_data/video/audio/test/output/'
    # 音频伴奏的输出文件
    opt_ins_root = '/media/checkpoint/speech_data/video/audio/test/output/'

    shutil.rmtree(opt_vocal_root, ignore_errors=True)
    os.makedirs(opt_vocal_root, exist_ok=True)

    shutil.rmtree(opt_ins_root, ignore_errors=True)
    os.makedirs(opt_ins_root, exist_ok=True)
    # 人声提取激进程度
    agg = 10
    # 输出音频格式
    format0 = ["wav", "flac", "mp3", "m4a"]

    # uvr5_weights文件夹下发的模型，uvr5_names变量中存储
    uvr5_names
    """
    ['onnx_dereverb_By_FoxJoy',
     'HP2_all_vocals',
     'HP2-人声vocals+非人声instrumentals',
     'HP3_all_vocals',
     'HP5_only_main_vocal',
     'HP5-主旋律人声vocals+其他instrumentals',
     'VR-DeEchoAggressive',
     'VR-DeEchoDeReverb',
     'VR-DeEchoNormal']
    """
    wav_input = '/media/checkpoint/speech_data/video/PleasantGoatandBigBigMovie_23mi.mp4'
    vocal_path, others_path = uvr_prediction(uvr5_names[5], wav_input,
                                             opt_vocal_root,
                                             opt_ins_root,
                                             agg,
                                             format0[0]
                                             )
    print(vocal_path)
    print(others_path)
