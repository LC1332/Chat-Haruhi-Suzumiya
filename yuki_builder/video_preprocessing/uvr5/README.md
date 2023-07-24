### 人声伴奏分离批量处理， 使用UVR5模型。

### 代码来源
```text
https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI

```


>UVR5模型文件 https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/uvr5_weights

### 模型说明
```text
模型分为三类：
1、保留人声：不带和声的音频选这个，对主人声保留比HP5更好。内置HP2和HP3两个模型，HP3可能轻微漏伴奏但对主人声保留比HP2稍微好一丁点；
2、仅保留主人声：带和声的音频选这个，对主人声可能有削弱。内置HP5一个模型；
3、去混响、去延迟模型（by FoxJoy）： 
 (1)MDX-Net(onnx_dereverb):对于双通道混响是最好的选择，不能去除单通道混响；
 (234)DeEcho:去除延迟效果。Aggressive比Normal去除得更彻底，DeReverb额外去除混响，可去除单声道混响，但是对高频重的板式混响去不干净。
去混响/去延迟，附：
1、DeEcho-DeReverb模型的耗时是另外2个DeEcho模型的接近2倍；
2、MDX-Net-Dereverb模型挺慢的；
3、个人推荐的最干净的配置是先MDX-Net再DeEcho-Aggressive。

```

### 使用
- 下载模型至 uvr5_weights
- import process.py
```python
from process import uvr
```
- 整理入参
```python
from process import uvr_prediction, uvr5_names
import os
import traceback, pdb
import ffmpeg
import torch
import shutil
import sys
# python yuki_builder.py crop的-role_audios输出文件夹 带上voice
dir_wav_input = '/media/checkpoint/speech_data/video/audio/test/voice/'
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

```

- 调用函数运行
```python

wav_input = '/media/checkpoint/speech_data/video/audio/test/voice/0003_0.00.56.1800_00.00.58.980_为了逃避狼群.wav'
vocal_path, others_path = uvr_prediction(uvr5_names[5], wav_input,
                                         opt_vocal_root,
                                         opt_ins_root,
                                         agg,
                                         format0[0]
                                         )
print(vocal_path)
print(others_path)
```
