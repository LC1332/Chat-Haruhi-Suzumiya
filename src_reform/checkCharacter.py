import os


def checkCharacter(configuration):
    pass
    character_folder = configuration['character_folder']
    if os.path.isdir(character_folder):
        print("已找到角色文件夹")
    else:
        os.makedirs(character_folder)
        print("已创建角色文件夹")
        # return False, 0, "未找到角色文件夹"
    elements = os.listdir(character_folder)
    if "system_prompt.txt" not in elements:
        # print("未找到系统提示词，请添加")
        print(f"未找到系统提示词, 请在{character_folder}中手动创建 'system_prompt.txt'文件，并设置你的prompt")
    # print(os.listdir(configuration['character_folder']))
    if "texts" not in elements:
        os.makedirs(configuration["texts_folder"])
        print("texts文件夹创建成功")
    if "jsonl" not in elements:
        os.makedirs(configuration["jsonl_folder"])
        print("jsonl文件夹创建成功")
        # return False, 2, "未找到jsonl文件, 请添加"
    # else:
    #     jsonl_path = os.path.join(character_folder, "jsonl")
    #     # print(jsonl_path)
    #     jsonl_elements = os.listdir(jsonl_path)
    #     # print(jsonl_elements)
    if 'dialogues' not in elements:
        os.makedirs(configuration["dialogue_path"])
        print("dialogues文件夹创建成功")
        # return False, 3, "未找到dialogues，请添加"
    if "images" not in elements:
        os.makedirs(configuration["images_folder"])
        print("iamges文件夹创建成功")
    return True, -1, "角色检查完毕"
