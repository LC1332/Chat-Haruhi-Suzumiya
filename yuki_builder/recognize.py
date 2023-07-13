# coding: utf-8

import argparse
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import random
from scipy.spatial.distance import cosine
from audio_feature_ext.tool import get_first_subdir,write_to_file, get_subdir, get_filelist
from audio_feature_ext import AudioFeatureExtraction
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import cross_val_score
from crop import video_Segmentation

class KNN_Classifier_lis:
    def __init__(self, feature, labels,n_neighbors=3):
        self.feature = feature
        self.labels = labels
        self.classifier = KNeighborsClassifier(n_neighbors=n_neighbors, metric='cosine')
        self.classifier.fit(self.feature, self.labels)

    def predict(self, x):
        # Predict the class label
        predicted_label = self.classifier.predict(x.reshape(1, -1))

        # Get the distances and indices of the nearest neighbors
        dists, indices = self.classifier.kneighbors(x.reshape(1, -1))

        # Get the labels of the nearest neighbors
        nearest_labels = [self.labels[i] for i in indices[0]]

        # Return the predicted label, nearest labels and distances
        return predicted_label[0], list(zip(nearest_labels, dists[0]))


class KNN_Classifier:
    def __init__(self, feature, labels,n_neighbors=3):
        self.feature = feature
        self.labels = labels
        self.classifier = KNeighborsClassifier(n_neighbors=n_neighbors, metric='cosine')
        self.classifier.fit(self.feature, self.labels)

    def predict(self, x):
        # Predict the class label
        predicted_label = self.classifier.predict(x.reshape(1, -1))

        # Get the distances to the nearest neighbors
        dist, _ = self.classifier.kneighbors(x.reshape(1, -1))

        # Return the label of the most common class and the smallest distance
        return predicted_label[0], dist[0].min()


class AudioClassification:
    def __init__(self):
        pass

    def create_classifier(self,class_name, features, labels, n_neighbors=None):
        classifier_class = globals()[class_name](features, labels, n_neighbors)
        return classifier_class

    def get_feature(self,audio_feature_dir):


        # pinkle load feature_fname
        features = []
        labels = []
        dim = 0
        role_dirs = get_subdir(audio_feature_dir+'/feature')
        for role_dir in role_dirs:
            role = role_dir.split('/')[-1]
            file_list = get_filelist(role_dir)
            for feature_fname in file_list:
                with open(feature_fname, 'rb') as f:
                    feature = pickle.load(f)
                # append numpy array feature into numpy matrix features
                if dim == 0:
                    features = feature
                    dim = feature.shape[0]
                else:
                    features = np.vstack((features, feature))

                labels.append(role)

        return features,labels
    def get_pridict(self,role_audios,recog_csv_out,n_neighbors=3,mark=''):

        # read the local pkl pth to get features and labels
        self.feat_sel, self.label_sel = self.get_feature(role_audios)
        self.my_classifier = KNN_Classifier(self.feat_sel, self.label_sel,n_neighbors)

        # multiple classifiers
        # self.my_classifier = self.create_classifier(class_name,self.feat_sel, self.label_sel,n_neighbors)

        threshold_certain = 0.4
        threshold_doubt = 0.6 # 遍历视频切割的目录
        for idx,feature_folder in enumerate(self.candidate_path[:]):
            name = feature_folder.split('/')[-1]
            if mark:
                save_name = os.path.join(recog_csv_out,f'{name}_{mark}.txt')
            else:
                save_name = os.path.join(recog_csv_out, f'{name}.txt')
            feature_folder = os.path.join(feature_folder,"feature")  # 遍历特征文件

            file_list = os.listdir(feature_folder)

            file_list.sort(key = lambda x: int(x.split('_')[0]))
            with open(save_name, "w", encoding="utf-8") as f_out:  # 把knn结果写入srt文件
                for file in file_list:
                    try:
                        id_str = ''.join(file.split('_')[1:])
                        full_file_name = os.path.join(feature_folder, file)

                        with open(full_file_name, 'rb') as f:
                            feature = pickle.load(f)

                        predicted_label, distance = self.my_classifier.predict(feature)

                        role_name = ''

                        if distance < threshold_certain:
                            role_name = predicted_label
                        elif distance < threshold_doubt:
                            role_name = '(可能)' + predicted_label

                        output_str = role_name + ':「' + id_str[:-8] + '」'
                        f_out.write(output_str + "\n")
                    except:
                        continue

def recognize(args):

    if args.verbose:
        print('runing recognize')

    # checking if input_video is a file
    if not os.path.isfile(args.input_video):
        print('input_video is not exist')
        return
    
    # checking if input_srt is a file
    if not os.path.isfile(args.input_srt):
        print('input_srt is not exist')
        return
    
    # checking if role_audios is a folder
    if not os.path.isdir(args.role_audios):
        print('role_audios is not exist')
        return
    
    # checking if output_folder is a folder
    if not os.path.isdir(args.audio_pkl_out):
        print('warning output_folder is not exist')
        # create output_folder
        os.mkdir(args.audio_pkl_out)
        print('create folder', args.audio_pkl_out)

    # 视频切割
    video_pth_segmentor = video_Segmentation()
    # video_pth_segmentor.clip_video_bysrt(args.input_video,args.input_srt,args.audio_pkl_out)

    # 音频提取特征 wav→pkl
    model_pth = '/mnt/sda/huggingface_weight/voicemodel/'
    audio_feature_extractor = AudioFeatureExtraction(model_pth)
    # video_pth_segmentor.extract_new_pkl_feat(audio_feature_extractor, args.audio_pkl_out)

    # 角色识别
    audio_classification = AudioClassification()

    # audio_classification.get_pridict(args.role_audios,args.recog_csv_out)


    pass
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract audio by subtitle time stamp',
        epilog='author:fengyunzaidushi(https://github.com/fengyunzaidushi)'
    )
    # video_pth, role_audios, annotate_csv
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--input_video', default='input_file', type=str, required=True, help="video path")
    parser.add_argument('--input_srt', default='input_srt', type=str, required=True,help="path of input .srt/.ass file")
    parser.add_argument('--audio_pkl_out', default='/mnt/sda/baidu_disk/lg/scixing/audio_pkl_out', type=str, required=True, help="directory of the  audios and pkl files  to save")
    parser.add_argument('--recog_csv_out', default='/mnt/sda/baidu_disk/lg/scixing/recog_csv_out', type=str, required=True, help="the role recoginize csv file")
    parser.add_argument('--role_audios', default='/mnt/sda/baidu_disk/lg/scixing/roles', type=str, required=True, help= "directory of the role audio to save")

    args = parser.parse_args()
    parser.print_help()
    recognize(args)
"""
python verbose=True --input_video /mnt/sda/baidu_disk/凉宫春日/lg_video/video/Haruhi_16.mkv  
        --input_srt /mnt/sda/baidu_disk/lg/zim/Subtitle_SC_SRT/Haruhi_16.srt
        --audio_pkl_out /mnt/sda/baidu_disk/lg/scixing/audio_pkl_out
        --recog_csv_out /mnt/sda/baidu_disk/lg/scixing/recog_csv_out
        --role_audios /mnt/sda/baidu_disk/lg/scixing/roles
"""
