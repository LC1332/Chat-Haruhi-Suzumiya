# 自定义修改下面字典的value值  标有**的文件夹，需要有对应文件。
video_config = {"video_lis_pth": "/mnt/sda/baidu_disk/凉宫春日/lg_video/video",  # **视频所在文件夹 **需要准备视
                }
audio_config = {
                "audio_model_pth":'/mnt/sda/huggingface_weight/voicemodel/',  # **模型权重路径 需要下载模型→ git clone https://huggingface.co/scixing/voicemodel
                "audio_roles_dir":'/mnt/sda/baidu_disk/lg/scixing/roles/voice', # **分类好的角色音频路径 需要手动分类
                "audio_feature_dir":'/mnt/sda/baidu_disk/lg/scixing/roles/feature', # **分类好的角色音频路径 需要手动分类
                "audio_out_dir": "/mnt/sda/baidu_disk/凉宫春日/lg_video/audio",  # 视频切割输出的音频路径
                }

srt_config = {
               "subtitle_dir":"/mnt/sda/baidu_disk/lg/zim/Subtitle_SC_SRT",  # **视频对应字幕，视频和字幕名称需要一致 需要准备 ,
                # 1.预测的角色类型输出路径 +
                # 2.预测输出文本之后→进行人工核之后，文件重命名，增加'annotate',举例 a.txt →a.annotate.txt,可以进行增量训练
                "srt_out_dir":"./srt_predict_out",

            }


