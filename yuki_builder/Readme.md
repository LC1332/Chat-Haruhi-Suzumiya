# 台本工具

## 介绍

## 环境安装

推荐使用anaconda创建虚拟环境，具体安装步骤请参考[anaconda](https://www.anaconda.com/)官网

- 安装pytorch  
推荐在官网([pytorch](https://pytorch.org/))选择适合自己的脚本安装，安装时注意选择合适的cuda版本
<!-- ，如果没有cuda则选择cpu版本。 -->
例如
```ps
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```
- 安装ffmpeg
前往[ffmpeg](https://ffmpeg.org/)官网下载安装包，需要添加环境变量


- 安装其他依赖
```ps
pip3 install -r requirements.txt
```

## 使用方法
本脚本提供4个功能，分别是
- 从视频中提取字幕(使用whisper)
- 将字幕转为csv文件
- 从手动标注的csv文件中提取特征
- 通过第三步得到特征文件，再通过视频与字幕文件，自动分类台词所属人物  
通常流程顺序使用即可，对于同一番剧。在特征足够的情况下，可以直接使用第四步进行分类。

### 从视频中提取字幕
支持从视频中提取字幕，输出为srt格式
```ps
python yuki_builder.py whisper -input_video <input_video> -srt_folder <srt_folder>
```
**input_video**: 输入视频文件路径
**srt_folder**: 输出字幕文件夹路径

### 将字幕转为csv文件
支持将srt文件或是ass文件转为csv文件, 用于后续使用，
这个步骤会输出一个csv文件，这个文件中包含了每一句台词的开始时间，结束时间，台词内容  
**台词所属人物需要人工进行标注，作为后期人物的特征数据**

```ps
python yuki_builder.py srt2csv -input_srt <input_srt>  -srt_folder <srt_folder>
```
**input_srt**: 输入srt文件路径  
**srt_folder**: 输出csv文件夹路径

### 从手动标注的csv文件中提取特征
此步会去下载声纹模型，若下载失败，可考虑从[这里](https://huggingface.co/scixing/voicemodel)进行下载放入`./yuki_builder/audio_feature_ext/models`文件夹中
这步将根据已经标注好的csv文件，去切割视频，提取特征，输出为wav, pkl等文件

```ps
python yuki_builder.py crop -annotate_map <annotate_map> -role_audios <role_audios>
```
**annotate_map**: 输入csv文件路径(此csv为手动标注的csv文件与视频文件的对应关系)  
示例: annotate_map.csv
```csv
标注文件,视频文件
Z:\ChatHaruhi\Chat-Haruhi-Suzumiya\yuki_builder\testWhisper\Oshi.no.Ko.S01E11.Idol.1080p.NF.WEB-DL.AAC2.0.H.264-ZigZag.cht&jp.csv,D:\推子\桜都字幕组（简日双语）\[Sakurato] Oshi no Ko [11][AVC-8bit 1080p AAC][CHS&JPN].mp4
```
**role_audios**: 输出特征，声音文件夹路径，将在下一步用到

## 通过第三步得到特征文件，再通过视频与字幕文件，自动分类台词所属人物
此步将根据第三步得到的特征文件，自动分类视频台词所属人物，输出为csv，txt文件
```ps
python yuki_builder.py recognize -input_video <input_video> -input_srt <input_srt> -role_audios <role_audios> -output_folder <output_folder>
``` 

**input_video:** 输入视频文件路径
**input_srt**: 视频srt文件路径
**role_audios**: 特征文件夹路径(第三步得到)
**output_folder**: 结果输出文件夹路径






