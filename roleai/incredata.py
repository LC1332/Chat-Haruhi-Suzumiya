import os
import shutil

from tool import get_filename, read_tolist, get_first_subdir


class IncrementData():
    def __init__(self, audio_out_dir, audio_roles_dir, srt_out_dir):
        self.audio_out_dir = audio_out_dir
        self.audio_roles_dir = audio_roles_dir
        self.srt_out_dir = srt_out_dir

    def static_origin(self):
        # 统计原始数据
        stattics_dic = {}
        role_lis = get_first_subdir(self.audio_roles_dir)
        for sub_dir in role_lis:
            role = sub_dir.split('/')[-1]
            # if role == '朝仓':
            lis = get_filename(sub_dir)
            stattics_dic[role] = [item[0] for item in get_filename(sub_dir)]

        origin_lis = [item for sub_lis in list(stattics_dic.values()) for item in sub_lis]
        return origin_lis

    def process(self):
        golden_res = get_filename(self.srt_out_dir, 'annotate.txt')
        same_lis = []
        i = 0
        j = 0
        for file, pth in golden_res[:]:
            srt_lis = read_tolist(pth)
            file_name = '_'.join(file.split('_')[:2])
            # 字典- 文本：role
            annote_dic = {}
            for line in srt_lis:
                role, text = line.split(":「")
                text = text[:-1]
                if text not in annote_dic:
                    annote_dic[text] = [role]
                else:
                    annote_dic[text].append(role)
            # 去掉重复的话语，因为字幕和音频数量不对等，要找到对应的音频是那句话→比较复杂
            real_dic = {k: v[0] for k, v in annote_dic.items() if len(v) == 1}
            corres_dir = os.path.join(self.audio_out_dir, f'{file_name}/voice')
            audio_lis = get_filename(corres_dir)

            # 遍历每一条音频

            audio_dic = {}
            for aud_name, aud_pth in audio_lis:
                file_text = os.path.splitext(aud_name)[0]
                audio_text = ''.join(file_text.split('_')[1:])

                if audio_text not in audio_dic:
                    audio_dic[audio_text] = [[aud_name, aud_pth]]
                else:
                    audio_dic[audio_text].append([aud_name, aud_pth])
            # 同样也是去掉重复的音频，因为字幕和音频数量不是一一对应，要找到对应的音频是那句话→比较复杂
            new_audio_dic = {k: v[0] for k, v in audio_dic.items() if len(v) == 1}
            # print(f'len(real_dic)  {len(real_dic)}')
            # print(f'len(new_audio_dic) {len(new_audio_dic)}')
            for audio_text, value in new_audio_dic.items():
                aud_name, aud_pth = value

                if audio_text in real_dic:
                    role = real_dic[audio_text]
                    new_aud_dir = os.path.join(self.audio_roles_dir, role)
                    os.makedirs(new_aud_dir, exist_ok=True)
                    new_aud_pth = os.path.join(new_aud_dir, aud_name)

                    # new_aud_dir1 = os.path.join(audio_roles_dir, f'new')
                    # os.makedirs(new_aud_dir1, exist_ok=True)
                    # new_aud_pth1 = os.path.join(new_aud_dir1, f'{aud_name}')

                    if not os.path.exists(new_aud_pth):
                        shutil.copy(aud_pth, new_aud_pth)
                        # shutil.copy(aud_pth, new_aud_pth1)
                        i += 1
                        print(f'{role} + 1 {aud_name},{i}')
                        pass
                    elif os.path.exists(new_aud_pth):
                        # j += 1
                        # print(aud_name,j)
                        # same_lis.append(aud_name)
                        pass

        # chaji_lis = [item for item in self.origin_lis if item not in same_lis]
        # print(chaji_lis)
