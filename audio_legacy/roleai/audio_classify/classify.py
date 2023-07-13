#coding: utf-8

import os
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import random
from scipy.spatial.distance import cosine
from audio_legacy.roleai.tool import get_first_subdir,get_subdir,get_filelist
from audio_legacy.roleai.tool import write_to_file
import shutil
"""
feature是一个N*D的numpy矩阵，每行存储了一个D维特征 labels是一个python的list of string，表示每行对应的数据的标签。

实现一个Python类My_Classifier, 这个类可以使用feature和labels初始化一个 sklearn的1-NN的最近邻分类器，使用cosine度量 这个类有一个predict方法，输出一个tuple，为(类别，距离)
"""


from sklearn.neighbors import NearestNeighbors
import numpy as np


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


class KNN_Classifier_One:
    def __init__(self, feature, labels,n_neighbors):
        self.feature = feature
        self.labels = labels
        self.classifier = NearestNeighbors(n_neighbors=1, metric='cosine')
        self.classifier.fit(self.feature)

    def predict(self, x):
        # Get the distances and indices of the nearest neighbors
        dists, indices = self.classifier.kneighbors(x.reshape(1, -1))
        # Get the label and distance of the nearest neighbor
        nearest_label = self.labels[indices[0][0]]
        nearest_dist = dists[0][0]

        return nearest_label, nearest_dist



class KNN_Classifier_Custom:
    def __init__(self, feature, labels,n_neighbors):
        self.feature = feature
        self.labels = labels

    def predict(self, x):
        min_dist = float('inf')
        predicted_label = None

        for i, f in enumerate(self.feature):
            dist = cosine(x, f)
            if dist < min_dist:
                min_dist = dist
                predicted_label = self.labels[i]

        return predicted_label, min_dist


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
    def __init__(self,audio_feature_dir, audio_roles_dir,srt_out_dir,audio_out_dir):
        self.audio_feature_dir = audio_feature_dir
        self.audio_roles_dir = audio_roles_dir
        self.srt_out_dir = srt_out_dir

        self.audio_first_dir = get_first_subdir(audio_out_dir)

        self.candidate_path = self.audio_first_dir[:]
        # self.roles, self.roles_list = self.get_roles_list()
        # self.features, self.labels = self.get_features()

    def get_roles_list(self):
        roles = os.listdir(self.audio_roles_dir)

        """
        roles
            春日 谷口 长门 新川先生 多丸裕 朝比奈 朝仓 ...
        roles_list
            ['209_或者这座岛有没有被当地人称为「什么什么岛」的传闻？.wav', 
            '106_我要喝100%果汁.wav', '121_你睡什么觉啊  笨蛋.wav',
        """
        roles_list = []
        roles_list_full = []
        for role in roles:

            sub_list = os.listdir(os.path.join(self.audio_roles_dir,role))
            roles_list.append(sub_list)

            full_name_list = [self.audio_roles_dir+role+'/'+file for file in sub_list]
            roles_list_full.append(full_name_list)

        return roles, roles_list



    def get_features(self):
        features = []
        labels = []
        dim = 0
        count = 0

        for role in self.roles:
            print(role,end='')
            for file in self.roles_list[self.roles.index(role)]:
                deal_flag = False
                for candidate in self.candidate_path: #'/mnt/sda/baidu_disk/lg/scixing/Haruhi ep1'
                    candidate_fname = os.path.join(candidate, 'voice')
                    if os.path.exists(candidate_fname):
                        deal_flag = True
                        feature_fname = os.path.join(candidate,'feature',file) +'.pkl'
                        break

                if deal_flag == False:
                    # print('warning!', file, 'not found')
                    continue

                if not os.path.exists(feature_fname):
                    # print('warning!', feature_fname, 'not found')
                    continue

                    # pinkle load feature_fname
                with open(feature_fname, 'rb') as f:
                    feature = pickle.load(f)

                count += 1

                # append numpy array feature into numpy matrix features
                if dim == 0:
                    features = feature
                    dim = feature.shape[0]
                    # print(dim)
                else:
                    features = np.vstack((features, feature))

                labels.append(role)

                # print(feature_fname,'found')

            # break
        return features, labels

    def knn_test(self):
        """
        feature是一个N*D的numpy矩阵，每行存储了一个D维特征 labels是一个python的list of string，表示每行对应的数据的标签。
        我想验证这批数据使用K近邻分类，在10折交叉时的准确率，请用python为我实现。
        """
        k = 1
        knn = KNeighborsClassifier(n_neighbors=k, metric='cosine')

        features = np.array(self.features)

        labels = np.array(self.labels)

        cv_accuracy = cross_val_score(knn, features, labels, cv=5)

        for fold, accuracy in enumerate(cv_accuracy,1):
            print(f"Fold {fold}: {accuracy}")

        # 打印平均准确率
        mean_accuracy = np.mean(cv_accuracy)
        print(f"Average Accuracy: {mean_accuracy}")

    def gather_feature_label(self,roles, roles_list):
        features = []
        labels = []
        dim = 0

        count = 0

        for role in roles:
            print(role,end=' ')

            for file in roles_list[roles.index(role)]:
                # print(file)

                deal_flag = False
                # 从切分的视频中找到对应的pkl文件
                for candidate in self.candidate_path:

                    candidate_fname = os.path.join(candidate,'voice',file)

                    if os.path.exists(candidate_fname):
                        # print(candidate_fname,'found')
                        deal_flag = True
                        feature_fname = os.path.join(candidate,'feature',file) + '.pkl'
                        out_pkl_dir= f'/mnt/sda/baidu_disk/lg/scixing/roles/feature/{role}'
                        os.makedirs(out_pkl_dir, exist_ok=True)
                        new_pkl_pth = f'{out_pkl_dir}/{file}.pkl'
                        if not os.path.exists(new_pkl_pth):
                            shutil.copy(feature_fname,new_pkl_pth)
                        break

                if deal_flag == False:
                    print('warning!',file,'not found')
                    continue

                if not os.path.exists(feature_fname):
                    print('warning!',feature_fname,'not found')
                    continue

                # pinkle load feature_fname
                with open(feature_fname,'rb') as f:
                    feature = pickle.load(f)

                count += 1

                # append numpy array feature into numpy matrix features
                if dim == 0:
                    features = feature
                    dim = feature.shape[0]
                    # print(dim)
                else:
                    features = np.vstack((features,feature))

                labels.append(role)

        return features, labels


    def get_feat_sel(self,roles,roles_list):
        roles_sel = []
        roles_list_sel = []
        for role in roles[:]:
            wav_list = roles_list[roles.index(role)]

            # random pick 5 element from wav_list
            random.shuffle(wav_list)
            # wav_list = wav_list[:]

            roles_sel.append(role)
            roles_list_sel.append(wav_list)

        feat_sel, label_sel = self.gather_feature_label(roles_sel,roles_list_sel)
        return feat_sel, label_sel

    def get_sel_predict(self):


        corrent_dists = []
        wrong_dists = []

        for i in range(len(self.labels)):
            # read i-th row from features, save as feat
            feat = self.features[i, :]
            # read i-th row from labels, save as label
            label = self.labels[i]

            # predict label of i-th row
            predicted_label, distance = self.my_classifier.predict(feat)
            if label == predicted_label:
                corrent_dists.append(distance)
            else:
                wrong_dists.append(distance)

    def create_classifier(self,class_name, features, labels, n_neighbors=None):
        classifier_class = globals()[class_name](features, labels, n_neighbors)
        return classifier_class

    def get_feature(self,audio_feature_dir):
        # pinkle load feature_fname
        features = []
        labels = []
        dim = 0

        role_dirs = get_subdir(audio_feature_dir)
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
                    # print(dim)
                else:
                    features = np.vstack((features, feature))

                labels.append(role)

        return features,labels
    def get_pridict(self,class_name,n_neighbors=3,mark=''):

        # self.roles, self.roles_list = self.get_roles_list()
        # self.feat_sel, self.label_sel = self.get_feat_sel(self.roles, self.roles_list)
        self.feat_sel, self.label_sel = self.get_feature(self.audio_feature_dir)

        self.my_classifier = self.create_classifier(class_name,self.feat_sel, self.label_sel,n_neighbors)



        threshold_certain = 0.4
        threshold_doubt = 0.6 # 遍历视频切割的目录
        for idx,feature_folder in enumerate(self.candidate_path[:]):
            name = feature_folder.split('/')[-1]
            if mark:
                save_name = os.path.join(self.srt_out_dir,f'{name}_{mark}.txt')
            else:
                save_name = os.path.join(self.srt_out_dir, f'{name}.txt')
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


                # label = 1
                # if distance[0][1] >0.4:
                #     label = 'dis0'
                # label_lis = len(set([item[0] for item in distance]))
                # label1 = 1
                # if label_lis>1:
                #     label1 = 'dif2'
                # print(predicted_label,distance,label,label1,"\n")


