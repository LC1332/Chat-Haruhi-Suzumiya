import requests
import inference_main
import time
import uuid

def set_model_path(path):
    inference_main.set_model_path(path)

def tts(text):
    url = "https://fanyi.baidu.com/gettts?lan=jp&text=%E7%A7%81%E3%81%AE%E9%9D%92%E6%98%A5&spd=3&source=web"

    payload = {}
    headers = {
    'Cookie': 'BAIDUID=543CBD0E4FB46C2FD5F44F7D81911F15:FG=1'
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    while res.content == b'':
        res = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(0.1)
    # print(len(res.content))
    # print(res.text)
    if res.status_code == 200:
        # with open("temp.mp3", "wb") as f:
        #     f.write(res.content)
        return res.content
    else:
        return None

def vits_haruhi(text, tran):
    voice = tts(text)
    if voice is None:
        print("TTS failed")
        return None
    return inference_main.infer_to("haruhi", tran, voice)


if __name__ == "__main__":
    # 设置模型路径
    set_model_path("vits_models/Haruhi_54000.pth")
    # 生成语音
    vits_haruhi("真実はいつもひとつ", 8)
    vits_haruhi("私の青春は後悔していない", 8)
    vits_haruhi("またみんなで笑いたいのに君が死んだら意味が無いじゃないか！", 8)
    vits_haruhi("あきらめたらそこで試合終了だよ", 8)
    vits_haruhi("別れの味は分かりません。さようならという言葉がこんなに強いとは知りませんでした", 8)
    vits_haruhi("命には限りがあるからこそ、もっと大切に見える。命に限りがあるからこそ、たゆまぬ努力が必要だ", 8)
    vits_haruhi("なんとかなるよ！絶対大丈夫だよ", 8)