SRT_CONFIG = {
    # 原始字幕和视频所在路径  必准备
    "srt_dir_origin": "./data/ASS",
    "video_origin": "./data/video",

    # 如果和默认值不同必须填写
    "srt_style": "zhengwen", # 目前仅支持ASS格式字幕，ASS字幕中 style一列的值，一般都是DeFault,zhengwen 等
    "video_format": ".mkv",  # 原始视频格式
    "srt_video_format": '_srt.mkv',  # 压制了字幕后 视频的命名，前面加上任意字符，如 "_srt"，和原视频能区分就可以

    # 默认 可以不用修改
    "srt_dir_utf8": "./data/ASS_utf8", # 转化为utf-8编码格式后，字幕输出的文件夹
    "srt_dic_file": "./data/srt_all_dic.txt", # 所有字幕，选择字幕时间的中间值(单位s)作为key,文本为value,制作成一个字典，方便后期和图片进行匹配
    "img_out_dir": './data/imgout',  # 切割出的图片的总目录
    "rename_img_dir": "./data/rename",  # 根据字幕 重命名的图片的总目录，可以和img_out_dir相同
}

