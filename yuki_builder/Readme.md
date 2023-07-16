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
- 将csv文件转为字幕
- 分类人物

### 从视频中提取字幕
支持从视频中提取字幕，输出为srt格式
```ps
python yuki_builder.py whisper <input_video> -srt_folder <srt_folder>
```
input_video: 输入视频文件路径
srt_folder: 输出字幕文件夹路径

### 将字幕转为csv文件
支持将srt文件或是ass文件转为csv文件, 用于后续使用

```ps
python yuki_builder.py srt2csv -input_srt <input_srt>  -srt_folder <srt_folder>
```
input_srt: 输入srt文件路径
srt_folder: 输出csv文件夹路径






