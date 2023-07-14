# coding: utf-8

import argparse
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from audio_feature_ext.tool import get_subdir, get_filelist
from audio_feature_ext.audio_fea_ext import AudioFeatureExtraction
from crop import video_Segmentation
import csv

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
    def save_to_csv(self,filename,data):

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print('识别结果保存到csv')
    def get_pridict(self,role_audios,audio_pkl_out,recog_csv_out,n_neighbors=3):

        # read the local pkl pth to get features and labels
        self.feat_sel, self.label_sel = self.get_feature(role_audios)
        self.my_classifier = KNN_Classifier(self.feat_sel, self.label_sel,n_neighbors)

        # multiple classifiers
        # self.my_classifier = self.create_classifier(class_name,self.feat_sel, self.label_sel,n_neighbors)

        threshold_certain = 0.4
        threshold_doubt = 0.6 # 遍历视频切割的目录
        sub_dir = get_subdir(audio_pkl_out)[0]
        name = sub_dir.split('/')[-1]

        save_name = os.path.join(recog_csv_out, f'{name}_recognize.csv')
        feature_folder = os.path.join(sub_dir,"feature")  # 遍历特征文件

        file_list = os.listdir(feature_folder)

        file_list.sort(key = lambda x: int(x.split('_')[0]))
        res_lis = [['人物','人物台词','开始时间','结束时间']]

        for file in file_list[:]:
            try:
                id_str = file[:-8]
                index,start_time, end_time , text= id_str.split('_')
                full_file_name = os.path.join(feature_folder, file)

                with open(full_file_name, 'rb') as f:
                    feature = pickle.load(f)

                predicted_label, distance = self.my_classifier.predict(feature)
                role_name = ''

                if distance < threshold_certain:
                    role_name = predicted_label
                elif distance < threshold_doubt:
                    role_name = '(可能)' + predicted_label

                start_time = start_time.replace('.', ':')
                end_time = end_time.replace('.', ':')
                res_lis.append([role_name, text, start_time, end_time])
            except:
                continue
        self.save_to_csv(save_name,res_lis)
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
    
    # checking if audio_pkl_out is a folder
    if not os.path.isdir(args.audio_pkl_out):
        print('warning audio_pkl_out is not exist')
        # create audio_pkl_out
        os.mkdir(args.audio_pkl_out)
        print('create folder', args.audio_pkl_out)

    # clip audio segement according to the subtile file timestamp ; output: *.wav
    # subtitle files that are not labeled by role
    video_pth_segmentor = video_Segmentation()
    # video_pth_segmentor.clip_video_bysrt(args.input_video,args.input_srt,args.audio_pkl_out)

    # 音频提取特征 wav→pkl
    model_pth = '/mnt/sda/huggingface_weight/voicemodel/'
    audio_feature_extractor = AudioFeatureExtraction(model_pth)
    # video_pth_segmentor.extract_new_pkl_feat(audio_feature_extractor, args.audio_pkl_out)

    # 角色识别
    audio_classification = AudioClassification()
    audio_classification.get_pridict(args.role_audios,args.audio_pkl_out,args.recog_csv_out)


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
    parser.add_argument('--audio_pkl_out', default='./data_crop/audio_pkl_out', type=str, required=True, help="directory of the  audios and pkl files  to save") # It is best to change the default directory
    parser.add_argument('--role_audios', default='./data_crop/role_audios', type=str, required=True, help= "audio directories and feature directories categorized by role") # It is best to change the default directory
    parser.add_argument('--recog_csv_out', default='./data_crop', type=str, required=False,
                        help="the role recoginize csv file")

    args = parser.parse_args()
    parser.print_help()
    # print(args.recog_csv_out)
    recognize(args)
"""
cd yuki_builder/
python verbose=True 
        --input_video Haruhi_16.mkv
        --input_srt Haruhi_16.srt
        --role_audios ./data_crop/role_audios  # Better change it to your own path
        --audio_pkl_out ./data_crop/audio_pkl_out  # Better change it to your own path
        --recog_csv_out ./data_crop  # You can change it to youw own path
"""
