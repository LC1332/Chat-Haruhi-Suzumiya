import os

def checkCharacter(configuration):
    pass
    if os.path.isdir(configuration['character_folder']):
        print("已找到角色文件夹")
    else:
        print("未找到角色文件夹")
        return False, 0, "未找到角色文件夹"
    elements = os.listdir(configuration['character_folder'])
    if "system_prompt.txt" not in elements:
        # print("未找到系统提示词，请添加")
        return False, 1, "未找到系统提示词, 请添加"
    # print(os.listdir(configuration['character_folder']))
    if "pkl" not in elements:
        return False, 2, "未找到pkl文件, 请添加"
    else:
        pkl_path = os.path.join(configuration["character_folder"], "pkl")
        print(pkl_path)
        pkl_elements = os.listdir(pkl_path)
        print(pkl_elements)
        
    return True, -1, "角色检查完毕"