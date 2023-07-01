from clip_tool import VideoSegmentation
from roleai.audio_feature_ext.audio_fea_ext import AudioFeatureExtraction
from config import audio_config,srt_config,video_config
from roleai.audio_classify.classify import AudioClassification

def main():


    # video segement by subtitle
    video_segmentor = VideoSegmentation(video_config['video_lis_pth'],
                                        audio_config['audio_out_dir'],
                                        srt_config['subtitle_dir'])
    video_segmentor.process()

    # Audio Feature Extraction
    audio_feature_extractor = AudioFeatureExtraction(audio_config['audio_model_pth'])
    audio_feature_extractor.extract_features(audio_config['audio_out_dir'])

    # audio calssify and predict
    audio_classification = AudioClassification(audio_config['audio_roles_dir'],
                                               srt_config['srt_out_dir'],
                                               audio_config['audio_out_dir'])

    audio_classification.get_pridict()


if __name__ == '__main__':
    main()

