# Chat凉宫春日 project (https://github.com/LC1332/Chat-Haruhi-Suzumiya)
# Chat凉宫春日是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，
# 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。
#
# 这个python程序用于处理Chat凉宫春日项目中的聊天记录，将dialogue转换为jsonl文件
# 用法：python chatlog2dialogue.py -input <input_file> -output <output_file>
import argparse
import json
import os


def generage_jsonl(input_folder, output_file):
    fw = open(output_file, 'w+', encoding='utf-8')
    for file in os.listdir(input_folder):
        with open(os.path.join('Haruhi-ContinuousGenerate', file), encoding='utf-8') as fr:
            """
            春日:「目前还没有，不过我们要时刻准备着，随时待命。SOS团的任务非常多样化，有时候会涉及到神秘事件的调查，有时候会需要我们去解决问题和争端。无论何时，我们都要保持警觉，时刻准备着，做好准备。」
            加藤惠:「好无聊啊，我想去玩儿游戏」
            春日:「惠，我们不能只顾自己的娱乐，忘记了我们的SOS团的使命和任务。如果你真的很无聊，不如和我们一起探索周围的环境，一起发现那些奇妙的事情。或者，我们可以一起思考创意，为SOS团的下一个任务做出更好的准备。只要我们团结一心，努力拼搏，相信我们一定可以收获更多的成果和收获。」
            朝比奈实玖瑠:「我想要拍摄一部影片」
            ||
            {"dialogue": [
              {"role": "阿虚", "text": "你们相信外星人吗？我听说有五个人见过外星人"},
              {"role": "小明", "text": "我不太确定，但是我觉得宇宙是非常广阔的，应该存在其他生命形式"},
              {"role": "阿虚", "text": "是的，我也有同样的观点。但是到目前为止，还没有确凿的证据表明外星人存在"}
            ], "source": "synthesized" }
            """
            dialgoue = {}
            texts = []
            for line in fr.readlines():
                print(file, '\n', line)
                line = line.strip()
                if line:
                    if ":" in line:
                        res = line.split(':')
                    elif '：' in line:
                        res = line.split('：')
                    if res[1] != '':
                        texts.append({"role": res[0], "text": res[1][1:-1]})
            dialgoue["dialogue"] = texts
            dialgoue["source"] = "synthesized"
            json.dump(dialgoue, fw, ensure_ascii=False)
            fw.write("\n")

    fw.close()


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Process dialogue data for Chat Haruhi Suzumiya project')
    parser.add_argument('-input', required=True, help='Input folder path')
    parser.add_argument('-output', help='Output file path')
    args = parser.parse_args()

    # 处理参数
    input_folder = args.input
    output_file = args.output if args.output else input_folder.replace('.jsonl', '_one_line_chat.jsonl')

    # 调用核心函数进行处理
    generage_jsonl(input_folder=input_folder, output_file=output_file)
