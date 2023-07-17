# coding: utf-8

import argparse
import os,re
import pickle
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from audio_feature_ext.tool import get_subdir, get_filelist,save_lis2txt
from audio_feature_ext.audio_fea_ext import AudioFeatureExtraction
from crop import video_Segmentation
import csv
import shutil

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
            # role = role_dir.split('/')[-1]
            role = os.path.basename(os.path.normpath(role_dir))
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
        print(f'识别结果保存到csv, {filename}')

    def correct_timestamp_format(self, s):
        # 使用正则表达式查找匹配的时间戳，并将第3个冒号替换为点
        corrected_s = re.sub(r'(\d{2}).(\d{2}).(\d{2}).(\d{3})', r'\1:\2:\3.\4', s)
        return corrected_s

    def save_lis2txt(self,filename, lines):
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(str(line) + '\n')
        print(f'识别结果保存到txt, {filename}')
    def get_pridict(self,role_audios,output_folder,temp_folder,n_neighbors=3):

        # read the local pkl pth to get features and labels
        self.feat_sel, self.label_sel = self.get_feature(role_audios)
        self.my_classifier = KNN_Classifier(self.feat_sel, self.label_sel,n_neighbors)

        # multiple classifiers
        # self.my_classifier = self.create_classifier(class_name,self.feat_sel, self.label_sel,n_neighbors)

        threshold_certain = 0.4
        threshold_doubt = 0.6 # 遍历视频切割的目录
        sub_dir = get_subdir(temp_folder)[0]
        # name = sub_dir.split('/')[-1]

        name = os.path.basename(os.path.normpath(sub_dir))

        csv_save_name = os.path.join(output_folder, f'{name}_output.csv')
        txt_save_name = os.path.join(output_folder, f'{name}_output.txt')
        feature_folder = os.path.join(sub_dir,"feature")  # 遍历特征文件


        file_list = get_filelist(feature_folder)
        res_lis = [['人物','人物台词','开始时间','结束时间']]
        txt_lis = []
        for file in file_list[:]:
            try:
                file = os.path.basename(file)
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

                start_time = self.correct_timestamp_format(start_time)
                end_time = self.correct_timestamp_format(end_time)
                res_lis.append([role_name, text, start_time, end_time])

                text_content = role_name + ':「' + text + '」'
                txt_lis.append(text_content)
            except:
                continue
        self.save_to_csv(csv_save_name,res_lis)
        self.save_lis2txt(txt_save_name,txt_lis)


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
    if not os.path.isdir(args.output_folder):
        print('warning output_folder is not exist')
        # create output_folder
        os.mkdir(args.output_folder)
        print('create folder', args.output_folder)

    # create temp folder under the args.role_audios
    temp_dir = os.path.dirname(args.role_audios)
    temp_folder = f'{temp_dir}/temp_folder'
    os.makedirs(temp_folder, exist_ok=True)

    # clip audio segement according to the subtile file timestamp ; output: *.wav
    # subtitle files that are not labeled by role
    video_pth_segmentor = video_Segmentation()
    video_pth_segmentor.clip_video_bysrt(args.input_video,args.input_srt,temp_folder)


    # audio features extract wav→pkl
    audio_feature_extractor = AudioFeatureExtraction()
    video_pth_segmentor.extract_new_pkl_feat(audio_feature_extractor, args.input_video,temp_folder)

    # role classify
    audio_classification = AudioClassification()
    audio_classification.get_pridict(args.role_audios,args.output_folder,temp_folder)

    # delete the temp folder
    # shutil.rmtree(temp_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract audio by subtitle time stamp',
        epilog='author:fengyunzaidushi(https://github.com/fengyunzaidushi)'
    )
    # video_pth, role_audios, annotate_csv
    parser.add_argument("verbose", type=bool, action="store")
    parser.add_argument('--input_video', default='input_file', type=str, required=True, help="video path")
    parser.add_argument('--input_srt', default='input_srt', type=str, required=True,help="path of input .srt/.ass file")
    parser.add_argument('--role_audios', default='./input_folder/role_audios', type=str, required=True, help= "audio directories and feature folder categorized by role") # Better to change the default folder
    parser.add_argument('--output_folder', default='./output_folder', type=str, required=False,
                        help="the output_folder role recoginize csv file")

    args = parser.parse_args()
    parser.print_help()
    recognize(args)

"""
cd yuki_builder/
python verbose=True 
        --input_video Haruhi_16.mkv
        --input_srt Haruhi_16.srt
        --role_audios ./input_folder/role_audios  # Better change it to your own path
        --output_folder ./data_crop  # You can change it to your own path
"""
