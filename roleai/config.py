# 自定义修改下面字典的value值  标有**的文件夹，需要有对应文件。
video_config = {"video_lis_pth": "/mnt/sda/baidu_disk/凉宫春日/lg_video/video",  # **视频所在文件夹 **需要准备视
                }
audio_config = {
                "audio_model_pth":'/mnt/sda/huggingface_weight/voicemodel/',  # **模型权重路径 需要下载模型→ git clone https://huggingface.co/scixing/voicemodel
                "audio_roles_dir":'/mnt/sda/baidu_disk/lg/scixing/roles', # **分类好的角色音频路径 需要手动分类
                "audio_out_dir": "/mnt/sda/baidu_disk/凉宫春日/lg_video/audio",  # 视频切割输出的音频路径
                }

srt_config = {
               "subtitle_dir":"/mnt/sda/baidu_disk/lg/zim/Subtitle_SC_SRT",  # **视频对应字幕，视频和字幕名称需要一致 需要准备 ,
                "srt_out_dir":"/mnt/sda/baidu_disk/lg/scixing/",  # 预测的角色类型路径
            }


