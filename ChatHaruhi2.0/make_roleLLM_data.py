import ChatHaruhi.ChatHaruhiTrain as ChatHaruhiTrain
import os
import collections
import tiktoken
import json
from transformers import AutoTokenizer, AutoModel
import torch
import math
from tqdm import tqdm

# 先用用tiktoken大致划分？
enc = tiktoken.get_encoding("cl100k_base")


def divide_data_into_chunk(file_path, ALLOW_SPLIT_TOKEN_LEN=300, ENFORCE_SPLIT_TOKEN_LEN=700):
    data = []
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    chunk_data = []
    last_act = -1
    last_diag = -1
    current_role_list = []
    current_chunk_list = []
    act_dialog_list = []
    len_current_chunk = 0
    data.append({"act_id": -1, "diag_id": -1, "content": "", "role": ""})
    for d in data:
        act_id = d['act_id']
        diag_id = d['diag_id']
        role = d['role']
        # 感觉句中\n断句好像基本都是旁白多个动作划分没啥意义?
        content = d['content'].replace("\n", " ")

        split_flag = False

        # 旁白special token验证
        if str.lower(role).startswith('narr'):
            current_content = role + ":" + content + '\n'
        else:
            current_content = role + ":「" + content + '」\n'

        len_current_content = len(enc.encode(current_content))

        if len_current_content > ENFORCE_SPLIT_TOKEN_LEN:
            n = len(content)
            while len(enc.encode(content[:n])) > ENFORCE_SPLIT_TOKEN_LEN:
                n -= 20
            current_content = role + ":「" + content + '」\n'

            len_current_content = len(enc.encode(current_content))

        if act_id != last_act:
            split_flag = True

        if act_id == last_act and diag_id != last_diag:
            if len_current_content + len_current_chunk > ALLOW_SPLIT_TOKEN_LEN:
                split_flag = True
            # 规则调整，防止dialog_id遗漏
            else:
                last_act = act_id
                last_diag = diag_id
                split_flag = False

        if len_current_content + len_current_chunk > ENFORCE_SPLIT_TOKEN_LEN:
            split_flag = True

        if split_flag == True:
            if len(current_chunk_list) != 0:
                dic = {"role_list": current_role_list,
                       "text_list": current_chunk_list,
                       "id_list": act_dialog_list}
                chunk_data.append(dic)
            last_act = act_id
            last_diag = diag_id
            current_role_list = [role]
            current_chunk_list = [current_content]
            act_dialog_list = [str(act_id) + "_" + str(diag_id)]
            len_current_chunk = len_current_content

        else:
            current_role_list.append(role)
            current_chunk_list.append(current_content)
            act_dialog_list.append(str(act_id) + "_" + str(diag_id))
            len_current_chunk += len_current_content

    return chunk_data


def output_chunks(role_name, chunk_data, root_dir):
    max_len = 0
    bad = 0
    for chunk in chunk_data:
        chunk_str = "".join(chunk["text_list"])
        max_len = max(max_len, len(enc.encode(chunk_str)))
        if role_name not in chunk_str:
            bad += 1

    print("role_name: {}, max_len: {}, n_chunk: {}, bad: {}".format(role_name, max_len, len(chunk_data), bad))

    # 创建角色名称的文件夹
    output_dir = f"{root_dir}/profile_chunks/{role_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将chunk写入文件
    for i, chunk in enumerate(chunk_data):
        file_path = f"{output_dir}/{i}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("".join(chunk["text_list"]))


def get_system_prompt(movie_names, desc, role_name):
    character = role_name
    series = movie_names[role_name]
    original_prompt = f'''I want you to act like {character} from {series}.
If others‘ questions are related with the novel, please try to reuse the original lines from the novel.
I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use.
You must know all of the knowledge of {character}.

'''
    # 修改角色prompt第一人称？
    original_prompt += desc[role_name]

    return original_prompt


def form_rolebench_database(root_dir):
    desc_path = f"{root_dir}/profiles-eng/desc.json"
    movie_name_path = f"{root_dir}/profiles-eng/scripts.json"

    with open(desc_path) as f:
        desc = json.load(f)

    with open(movie_name_path) as f:
        movie_names = json.load(f)

    # 这两个文件无数据
    remove_desc = ["Doctor Who", "Blair Waldorf"]

    role_database = []
    for role_name in desc:
        if role_name in remove_desc:
            continue

        script_path = f"{root_dir}/profiles-eng/profiles-eng-{role_name}.jsonl"
        chunk_data = divide_data_into_chunk(script_path)

        # # 输出拆分台本文本数据
        output_chunks(role_name, chunk_data, root_dir)

        # # 打印调整划分文本参数
        # for k in chunk_data:
        #     print(k)
        #     chunk_str = "".join(k["text_list"])
        #     print([len(enc.encode(a)) for a in k["text_list"]])
        #     print(len(enc.encode(chunk_str)))
        #     print()

        system_prompt = get_system_prompt(movie_names, desc, role_name)
        
        role_data = {"role_name": role_name,
                     "chunks": chunk_data,
                     "system_prompt": system_prompt
                     }
        role_database.append(role_data)

    return role_database


def extract_tuples_from_story(role_name, chunks):
    story_tuples = []
    for chunk in chunks:
        role_list = chunk["role_list"]
        text_list = chunk["text_list"]

        query, target = "", ""
        history = []
        for role, text in zip(role_list, text_list):
            if role == role_name and query != "":
                target = text
                story_tuples.append((query, target, history[:-1]))
            else:
                query = text

            history.append(text)

    return story_tuples


if __name__ == "__main__":
    root_dir = "/group/30106/warrensun/kg/new_data/sq_digit/RoleBench"
    role_database = form_rolebench_database(root_dir)

    for data in role_database:
        role_name = data['role_name']
        chunks = data['chunks']
        system_prompt = data['system_prompt']

        story_tuples = extract_tuples_from_story(role_name, chunks)

        story_text_folder = f"{root_dir}/profile_chunks/{role_name}"
        chatbot = ChatHaruhiTrain(system_prompt=system_prompt,
                                  story_text_folder=story_text_folder,
                                  llm="Llama2GPT",
                                  embedding="bge_en")

        for query, target, history in story_tuples:
            input_prompt = chatbot.generate_prompt(query, history, target)

            # 打印train示例
            print(input_prompt)