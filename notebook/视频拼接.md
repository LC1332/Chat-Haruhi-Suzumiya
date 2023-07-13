我有一段字幕

```
Dialogue: 0,0:22:01.79,0:22:03.09,zhengwen,NTP,0000,0000,0000,,喂  春日
Dialogue: 0,0:22:04.67,0:22:05.23,zhengwen,NTP,0000,0000,0000,,什么啊
Dialogue: 0,0:22:07.11,0:22:09.27,zhengwen,NTP,0000,0000,0000,,这电影我绝对会让它成功的
Dialogue: 0,0:22:19.90,0:22:20.70,zhengwen,NTP,0000,0000,0000,,当然啊
Dialogue: 0,0:22:22.47,0:22:24.27,zhengwen,NTP,0000,0000,0000,,因为是我导演的呢  
Dialogue: 0,0:22:24.68,0:22:28.94,zhengwen,NTP,0000,0000,0000,,自然是和成功约好的  用不着你说也是
```

并且根据字幕的最后一个字符串，定义了一个图片文件

如字幕第一行对应"/content/output/喂  春日.jpg"
字幕第二行对应"/content/output/什么啊.jpg"

我希望组织一段新的视频output.avi，根据字幕对应的时间，组织一段视频。对应图片的时间与字幕一致

比如我定义 start_time = 22 * 60

那么视频的1.79秒之前，是黑色的
1.79秒到3.09秒显示"/content/output/喂  春日.jpg"
以此类推。用python的opencv库为我实现

```python
import cv2

# 定义字幕文件路径和视频输出路径
subtitle_path = "/path/to/subtitle.srt"
output_path = "/path/to/output.avi"

# 定义视频尺寸和帧率
width, height = 1920, 1080
fps = 30

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 定义字幕开始时间偏移量（单位：秒）
start_time = 22 * 60

# 读取字幕文件并逐行处理
with open(subtitle_path, "r", encoding="utf-8") as subtitle_file:
    lines = subtitle_file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Dialogue:"):
            # 解析字幕时间
            components = line.split(",")
            start = components[1].split(":")
            end = components[2].split(":")
            start_seconds = float(start[0]) * 3600 + float(start[1]) * 60 + float(start[2])
            end_seconds = float(end[0]) * 3600 + float(end[1]) * 60 + float(end[2])
            
            # 计算相对于视频开始时间的偏移量
            start_seconds -= start_time
            end_seconds -= start_time
            
            # 前面为黑色帧
            for i in range(int(start_seconds * fps)):
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                out.write(frame)
            
            # 字幕期间显示对应的图片
            for i in range(int(start_seconds * fps), int(end_seconds * fps)):
                img_path = components[-1].strip().strip(",")
                img = cv2.imread(img_path)
                frame = cv2.resize(img, (width, height))
                out.write(frame)

# 关闭视频写入对象
out.release()
```