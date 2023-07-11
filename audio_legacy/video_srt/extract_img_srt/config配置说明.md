1. 原始字幕和视频所在路径 ，必修改

"srt_dir_origin": "./data/ASS",
"video_origin": "./data/video",

修改后如下：

![](img/文件路径配置.png)



2. 目前仅支持ASS字幕，ASS字幕style

   2.1 ASS字幕格式如下：

   Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text

   2.2 选择选择第5列 **style** 的值，如下图所示：

   style有很多值：jinggao,OP,**zhengwen,**  其中**zhengwen**是真正剧情人物对话的字幕。 jinggao,OP是说明注释，或者一些歌词之类的，或者字幕制作者对字幕的补充。

   ![](img/srt_style.png)

   ![](img/srt_style_zw.png)



3. 视频格式

   3.1 "video_format": ".mkv",  # 原始视频格式

   就是视频的格式后缀

   3.2   "srt_video_format": '_srt.mkv',

    就是把字幕压制进了字幕后，视频的命名，主要是为了和原视频进行区分。在视频格式“.mkv”前面加上任意字符。，如 "_srt"

   *注释：字幕压制，就是字幕嵌入到视频里之后，单独打开视频就有字幕，不需要单独的字幕文件了。

