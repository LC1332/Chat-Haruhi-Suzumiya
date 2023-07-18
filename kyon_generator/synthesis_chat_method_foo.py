# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个程序是一个synthesis_chat method的简单例子

def generate(input_file, output_file, additional_config=None):
    """
    核心函数，使用foo方法将input_file生成增广的jsonl文件保存到output_file
    """
    with open(input_file, 'r') as f:
        # 读取input_file的内容
        data = f.read()
    
    # 这里可以编写生成增广数据的函数逻辑
    
    with open(output_file, 'w') as f:
        # 将增广数据写入output_file
        f.write(data)