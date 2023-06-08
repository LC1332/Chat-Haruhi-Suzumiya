import requests
import inference_main

def set_model_path(path):
    inference_main.set_model_path(path)

def tts(text):
    res = requests.get(f"https://fanyi.baidu.com/gettts?lan=jp&text={text}&spd=5&source=web", headers={"Accept-Encoding": "gzip"})
    if res.status_code == 200:
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