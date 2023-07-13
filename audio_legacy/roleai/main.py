from clip_tool import VideoSegmentation
from audio_legacy.roleai.audio_feature_ext.audio_fea_ext import AudioFeatureExtraction
from config import audio_config, srt_config, video_config
from audio_legacy.roleai.audio_classify.classify import AudioClassification
from incredata import IncrementData


def main():
    # 01 使用前 先修改 config.py对应参数
    # video segement by subtitle 视频切割出分段音频
    video_segmentor = VideoSegmentation(video_config['video_lis_pth'],
                                        audio_config['audio_out_dir'],
                                        srt_config['subtitle_dir'])
    # video_segmentor.process()

    # 02 Audio Feature Extraction  音频特征提取
    audio_feature_extractor = AudioFeatureExtraction(audio_config['audio_model_pth'])
    # audio_feature_extractor.extract_features(audio_config['audio_out_dir'])

    # 03 audio calssify and predict 根据音频特征 识别台本角色
    audio_classification = AudioClassification(audio_config['audio_feature_dir'],
                                               audio_config['audio_roles_dir'],
                                               srt_config['srt_out_dir'],
                                               audio_config['audio_out_dir'])

    class_name = ['KNN_Classifier_One', 'KNN_Classifier']
    n_neighbors = 3  # 表示knn n_neighbors的取值
    mark = ''  # 在默认输出文件后拼接一个字符,a.txt → a_mark.txt; mark 可自定义为01，02...,区分更新数据集后新的结果
    audio_classification.get_pridict(class_name[1], n_neighbors, mark)


    # 04 数据增强
    audio_increment = IncrementData(audio_config['audio_out_dir'],
                                    audio_config['audio_roles_dir'],
                                    srt_config['srt_out_dir'])
    # audio_increment.process()

    # 再预测
    # audio_classification.get_pridict(class_name[0], n_neighbors, mark='retrain')

if __name__ == '__main__':
    main()

