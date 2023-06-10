import requests
import inference_main
import time
import uuid

def set_model_path(path):
    inference_main.set_model_path(path)

def tts(text, spd):
    url = f"https://fanyi.baidu.com/gettts?lan=jp&text={text}&spd={spd}&source=web"

    payload = {}
    headers = {
    'Cookie': 'BAIDUID=543CBD0E4FB46C2FD5F44F7D81911F15:FG=1'
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    while res.content == b'':
        res = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(0.1)
   

    if res.status_code == 200:
        return res.content
    else:
        return None

def vits_haruhi(text, tran, spd=3):
    voice = tts(text, spd)
    
    if voice is None:
        print("TTS failed")
        return None
    filename = f"tts_results/{str(uuid.uuid4())}.mp3";
    with open(filename, "wb") as f:
        f.write(voice)
    return inference_main.infer_to("haruhi", tran, filename)


if __name__ == "__main__":
    inference_main.infer_tool.mkdir(["./tts_results"])
    # 设置模型路径
    set_model_path("vits_models/Haruhi_54000.pth")
    # 生成语音
    print( vits_haruhi("真実はいつもひとつ", 8))
    print( vits_haruhi("私の青春は後悔していない", 8))
    # vits_haruhi("またみんなで笑いたいのに君が死んだら意味が無いじゃないか！", 8)
    # vits_haruhi("あきらめたらそこで試合終了だよ", 8)
    # vits_haruhi("別れの味は分かりません。さようならという言葉がこんなに強いとは知りませんでした", 8)
    # vits_haruhi("命には限りがあるからこそ、もっと大切に見える。命に限りがあるからこそ、たゆまぬ努力が必要だ", 8)
    # vits_haruhi("なんとかなるよ！絶対大丈夫だよ", 8)