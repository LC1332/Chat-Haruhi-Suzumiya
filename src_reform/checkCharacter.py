import os

def checkCharacter(configuration):
    pass
    if os.path.isdir(configuration['character_folder']):
        print("已找到角色文件夹")
    else:
        print("未找到角色文件夹")
        return False
    