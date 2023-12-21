[スポンサーシップ](#スポンサーシップ) | [報告](https://arxiv.org/abs/2308.09597) | [パーソナリティ](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/research/personality) | [コントリビューター](#コントリビューター)

<h1 id="BigTitle">
    Chat-Haruhi-Suzumiya
</h1>

# 大規模言語モデルでアニメキャラクターを現実に蘇らせる

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)]()
[![Data License](https://img.shields.io/badge/Data%20License-CC%20By%20NC%204.0-red.svg)]()
[![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/chengli-thu/ChatHaruhi-OpenAI)

<!-- (https://huggingface.co/spaces/silk-road/ChatHaruhi) -->

We've just released finetuned ChatHaruhi-Qwen-7B model and code, try here <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/ChatHaruhi_x_Qwen7B.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>. A detailed test on Harry Potter! <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Harry_Potter_test_on_Qwen7B.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>


<h4 align="center">
    <p>
        <a href="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/README_EN.md">English</a> |
        <a href="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/README.md">Chinese简体中文</a> |
        <b>日本語</b> |
        🤗 <a href="https://huggingface.co/spaces/chengli-thu/ChatHaruhi-OpenAI" target="_blank">Hugging Face</a>  |
        📜 <a href="https://arxiv.org/pdf/2308.09597.pdf" target="_blank">Paper</a>  |
        🤗🗃️ <a href="https://huggingface.co/datasets/silk-road/ChatHaruhi-54K-Role-Playing-Dialogue" target="_blank">54k Dataset</a>  |
    <p>
</h4>


**Chat-Haruhi-Suzumiya** は、涼宮ハルヒのようなキャラクターの口調、性格、ストーリーを模倣した言語モデルである、


<details>
  <summary> このプロジェクトは、李鲁鲁, 冷子昂, 闫晨曦, 封小洋, scixing, 沈骏一, Aria Fei, 王皓, 米唯实, 冷月, JunityZhan, 贾曜恺, 吴平宇, 孙浩甄 らによって開発されています。</summary>

これはオープンソースのプロジェクトで、メンバーは DataWhale のようなオープンソースのコミュニティから集められました。

李鲁鲁( [Cheng Li@SenseTime](https://github.com/LC1332) )は、プロジェクト全体を主導し、ほとんどの機能を設計・実装した。

冷子昂( [Ziang Leng@SenseTime](https://blairleng.github.io) )は、ChatHaruhi 1.0 の学習、データ生成、バックエンドアーキテクチャの設計と実装を行った。

闫晨曦( [Chenxi Yan@Chengdu University of Information Technology](https://github.com/todochenxi) )は、ChatHaruhi 1.0 のバックエンドの実装とメンテナンスを行った。

沈骏一( [Junyi Shen@Zhejiang University](https://github.com/J1shen) )は、トレーニングコードを実装し、トレーニングデータセットの生成に参加した。

王皓( [Hao Wang](https://github.com/wanghao07456) )は、テレビシリーズの脚本データを収集し、データ補強に参加した。

米唯实( [Weishi MI@Tsinghua University](https://github.com/hhhwmws0117) )は、データ増強に参加した。

Aria Fei( [Aria Fei@BJUT](https://ariafyy.github.io/) )は、スクリプトツールのASR機能を実装し、Openness-Aware Personality 論文プロジェクトに参加した。

封小洋( [Xiaoyang Feng@Nanjing Agricultural University](https://github.com/fengyunzaidushi) )は文字認識ツールを統合し、開放性を意識したパーソナリティ論文プロジェクトに参加した。

冷月 ( [Song Yan](https://github.com/zealot52099) )は、big bang thoery のデータを収集。スクリプトのフォーマット変換を行った。

scixing(汪好盛)( [HaoSheng Wang](https://github.com/ssccinng) )は、スクリプトツールに声紋認識と tts-vits 音声合成を実装した。

Linkang Zhan( [JunityZhan@Case Western Reserve University](https://github.com/JunityZhan) )は、Genshin Impact のシステムプロンプトとストーリーデータを収集した。

贾曜恺( [Yaokai Jia](https://github.com/KaiJiaBrother) )は、心理学プロジェクトで Vue フロントエンドを実装し、バートの GPU 抽出を実践した。

吴平宇( [Pingyu Wu@Juncai Shuyun](https://github.com/wpydcr) )は、トレーニングコードの最初のバージョンのデプロイに協力した。

孙浩甄( [Haozhen Sun@Tianjin University] )は、ChatHaruhi のキャラクターフィギュアをプロットしています。



</details>

<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/datasetOverview.png">
</p>

Chat-Haruhi-Suzumiya は、李鲁鲁, 冷子昂, 陈启源によって始められた [Luotuo](https://github.com/LC1332/Luotuo-Chinese-LLM) のサブプロジェクトのひとつである。

このプロジェクトは[現在進行中です](#todo-and-feature)。Arxiv 版のリリースに伴い、32 文字、52K の対話をサポートするデータセットを、対応するローカルモデルと ChatHaruhi1.0 の推論コードとともに、一週間以内に公開する予定です。その後、[ChatHaruhi2.0](#ChatHaruhi2) に向けてプロジェクトのリファクタリングを開始する予定です。

このプロジェクトは、商用利用を許可する Apache 2.0 でライセンスされています。しかし、以下のような他の関連する協定に従う必要があります:

- キャラクターロール自体の著作権。

- プロジェクトで使用される API の規約（OpenAI の規約など）。

- プロジェクトで使用されるモデルのライセンス（例えば、後に LlaMA や GLM などのモデルを採用する場合）。

## クイックスタート

ChatHaruhi プロジェクトを開始するには、以下の colab リンクを直接実行することで可能です

| 名称 | Colab リンク | 説明 |
|-|-|-|
| ChatHaruhi2.0(code) | <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/ChatHaruhi2_demo.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | OpenAI 版の ChatHaruhi 2.0 が稼働中です |
| ChatHaruhi2.0 Demo | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/chengli-thu/ChatHaruhi-OpenAI) | Hugging Face Demo (openai as LLM) |
| ChatHaruhi2.0 Demo | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/hhhwmws/ChatHaruhi-GLMPro) | Hugging Face Demo (GLMPro as LLM) |
| ChatHaruhi2.0 Demo | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/hhhwmws/ChatHaruhi-Xinghuo) | Hugging Face Demo (讯飞星火 as LLM) |
| ChatGLM2-LoRA Local Model  | <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/GLM_LORA.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | ChatGLM2-LoRA trained on ChatHaruhi-54K|
| Prototype of StoryTeller | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/Story-teller) | Prototype of StoryTeller |
| Prototype of StoryTeller | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Build_Story_Teller_Gradio_exposure_version.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | Prototype of StoryTeller |
| ChatHaruhi1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 役割の切り替えをサポートする機能統合クライアント                                                                                                 |


ChatHaruhi 2.0 のコードはすでに pip 経由でインストールできます。


## ニュース

[2023-08-29] ChatGLM2-LoRA の推論コードをリリース <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/GLM_LORA.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>

[2023-08-28] ChatHaruhi2.0 の OpenAI、Xunfei、GLMPro への対応が完了し、対応する Hugging Face のデモを開始しました。

[2023-06-07] Chat Haruhi Suzumiya が Modelscope コミュニティ主催、Alibaba Cloud と NVIDIA 共催、天地(top3)共催の Create@AI ハッカソンで準優勝、[動画](https://www.bilibili.com/video/BV1Xh411A7kC/)

[2023-06-03] CAAI 8th-Big Data and Social Computing で 2 位(top3)に入賞し、7月17日に口頭発表を行います： 8th China National Conference, BDSC 2023, Urumqi, China, July 15-17, 2023， 詳細は[リンク](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/research/personality)

## デモ動画

ビデオで使用されている VITS モデルは、[Haruhi Suzumiya Support Group](https://space.bilibili.com/201296348) から提供されたもので現在も改良中です。この[動画](https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11)には音声が含まれていますのでご注意ください 📢。

https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11

## 内容

<table>
  <tr>
    <td>
      <p align="center">
        <img src="https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/figures/haruhi_suzumiya_bondage_rp.jpg" height="400">
      </p>
    </td>
    <td>
      <ul>
        <li><a href="#ChatHaruhi2">ChatHaruhi2</a></li>
        <li><a href="#各デモのクイックスタート">各デモのクイックスタート</a></li>
        <li><a href="#デモ動画">デモ動画</a></li>
        <li><a href="#中国語のチュートリアルビデオ">中国語のチュートリアルビデオ</a></li>
        <li><a href="#TODO と機能">TODO と機能</a></li>
        <li><a href="#栄誉">栄誉</a></li>
        <li><a href="#スポンサーシップ">スポンサーシップ</a></li>
        <li><a href="#メンバー">メンバー</a></li>
        <li><a href="#引用">引用</a></li>
      </ul>
    </td>
  </tr>
</table>

## ChatHaruhi2

今後の研究の便宜のため、リファクタリングした ChatHaruhi2.0 を pip 経由で起動できるようにしました。現在、2.0 では画像と音声のデザインが削除されていますが、これは今後の研究でリファクタリングする予定です。インストールは以下です:

```shell
pip -q install transformers openai tiktoken langchain chromadb zhipuai chatharuhi
```

そして、次のようにコールします:

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi(
    role_name = 'haruhi',
    llm = 'openai'
)

response = chatbot.chat(role='阿虚', text='野球の新シーズンが始まりますね！参加する？')

print(response)
```

詳しいドキュメントとコードは https://github.com/LC1332/Haruhi-2-Dev にあります


## 各デモのクイックスタート



| 名称 |Colab リンク| 説明         |
|---|---|---|
| ChatHaruhi 1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 役割の切り替えをサポートする機能的に統合されたクライアント                                                                                                 |
| Genesis                                                     |<a href="https://colab.research.google.com/github/LC1332/Prophet-Andrew-Ng/blob/main/prophet-code/haruhiLangChain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| Lulu Li が開発した最初の Gradio チャット |
| Baidu Studio 版                                               | [Baidu Studio Version](https://aistudio.baidu.com/aistudio/projectdetail/6386896) | DataWhale ティーチングアシスタントの Qijun Ma が開発した Baidu Studio の簡易版 |
| Hugging Face 版                                            | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi) | Hugging Face 版                                                                                    |
| パーソナリティ - 大学入試小論文 | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/College_essays_gradio.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | 開放性の高低に合わせた大学入試小論文ジェネレーター、[リンク](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/research/personality) |
| パーソナリティ-Chatbot                                               | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/PersonalityChatbot.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | 開口性の高低に対応するチャットボット、[リンク](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/research/personality)  |
| Chat Megumi                                                 |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/gradio_megumi.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| Chat Megumi は、コミュニティの仲間が集めたコーパスを利用して作成されました。 |

## 過去のニュース

[2023-08-22] データセット [Hugging Face](https://huggingface.co/datasets/silk-road/ChatHaruhi-54K-Role-Playing-Dialogue) をリリース

[2023-08-21] ChatHaruhi の[技術レポート](https://arxiv.org/abs/2308.09597)が arXiv に掲載されました。


## 中国語のチュートリアルビデオ

| 動画 | 説明 |
|---|---|
| [5 分でわかるロードマップ](https://www.bilibili.com/video/BV1Xh411A7kC/)    | Bilibili で ModelScope の AI ハッカソン       |
| [DataWhale プレゼンテーション](https://www.bilibili.com/video/BV1ho4y1P75H) | DataWhale の課題用に作成されたインストラクションビデオ |
| [スクリプトツールチュートリアル](https://www.bilibili.com/video/BV1V8411S7eT)      |yuki_builder スクリプトツールの使い方ステップバイステップガイド|
| [文字データ形式チュートリアル](https://www.bilibili.com/video/BV1nu411H7Sy/)    |文字データ形式とテキストファイルから設定ファイルへの変換についてのチュートリアル。 |
| [40 分でわかる ModelScope チュートリアル](https://www.bilibili.com/video/BV1Wm4y1W7XH) | 入門レベルのチュートリアル 40 分、ディスカッションと質疑応答のための追加 40 分 |



## TODO と機能

TODO:

- [x] 22k ストーリーのオリジナルコーパスのモデルを訓練する
- [x] 技術レポートを arxiv で公開する
- [ ] ローカル推論コードの公開
- [ ] 52k データで学習したモデルをリリース
- [ ] ローカルモデルと OpenAI の ChatHaruhi2.0 に対応、GitHub にアップデート
- [x] **pip** によるクイックインストール


## 栄誉

- 🏆 ModelScope コミュニティ主催、Alibaba Cloud と NVIDIA 共催、天地(top3)共催の Create@AI ハッカソンで Chat Haruhi Suzumiya が準優勝、[動画](https://www.bilibili.com/video/BV1Xh411A7kC/)

- 🏆 CAAI 8th-Big Data and Social Computing で 2 位(top3)を受賞し、7月17日に口頭発表を行います： 8th China National Conference, BDSC 2023, Urumqi, China, July 15-17, 2023 [詳細はこちら](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/research/personality)

## スポンサーシップ

Chat Haruhi Suzumiya は CoT と同様の戦略を採用しており、通常の 10 ～ 20 倍の価格となっている。現在、API トークンはコミュニティの寄付によって支えられています。

また、GPU（A100、A800）を積極的に募集しています。ご寄付いただける方はご連絡ください。Chat Haruhi Suzumiya の運営を継続するためのご支援に大変感謝いたします。

[Luotuo プロジェクト](https://github.com/LC1332/Luotuo-Chinese-LLM#%E8%B5%9E%E5%8A%A9sponsorships)のスポンサーにご興味のある方は、[主要プロジェクト](https://github.com/LC1332/Luotuo-Chinese-LLM)をクリックするか、[スポンサーフォーム](https://github.com/LC1332/Luotuo-Chinese-LLM/blob/main/data/Sponsorship_and_balance.md)をご覧ください。

>[トップに戻る](#BigTitle)


## コントリビューター


- [Cheng Li@SenseTime](https://github.com/LC1332)は、プロジェクト全体を計画し、ほとんどの機能を設計・実装した。

- [Ziang Leng@SenseTime](https://blairleng.github.io)は、ChatHaruhi1.0 の全体的なトレーニング、データ生成、バックエンドアーキテクチャの設計と実装。

- [Chenxi Yan@Chengdu University of Information Technology](https://github.com/todochenxi)は、ChatHaruhi1.0 バージョンのバックエンドの実装とメンテナンス。

- [Junyi Shen@Zhejiang University](https://github.com/J1shen)は、トレーニングコードを実装し、トレーニングデータセットの生成に参加した。

- [Hao Wang](https://github.com/wanghao07456)は、My Own Swordsman の脚本データを収集し、拡張データの生成に参加した。

- [Weishi MI@Tsinghua University](https://github.com/hhhwmws0117)は、データ増強に参加した。

- [Aria Fei@BJUT](https://ariafyy.github.io/)は、スクリプトツールのASR機能を実装し、Openness-Aware Personality 論文プロジェクトに参加した。

- [Xiaoyang Feng@Nanjing Agricultural University](https://github.com/fengyunzaidushi)は、文字認識ツールを統合し、開放性を意識したパーソナリティ論文プロジェクトに参加した。

- [Song Yan](https://github.com/zealot52099)は、big bang thoery のデータを収集。スクリプトのフォーマット変換を行った。

- [HaoSheng Wang](https://github.com/ssccinng)は、スクリプトツールに声紋認識と tts-vits 音声合成を実装した。

- [Linkang Zhan@Case Western Reserve University](https://github.com/JunityZhan)は、 Genshin Impact からシステムプロンプトとストーリーのデータを収集した。

- [Yaokai Jia](https://github.com/KaiJiaBrother)は、Vue 版のフロントエンドを実装し、心理学プロジェクトでバートの GPU 抽出を実践した。

- [Pingyu Wu@Juncai Shuyun](https://github.com/wpydcr)は、トレーニングコードの最初のバージョンの配備を手伝った。

- [Haozhen Sun@Tianjin University](https://github.com/jcandzero)は、ChatHaruhi のモザイク画を描いた。


### 引用

このリポジトリのデータやコードを使用する場合は、リポジトリを引用してください。
```
@misc{li2023chatharuhi,
      title={ChatHaruhi: Reviving Anime Character in Reality via Large Language Model},
      author={Cheng Li and Ziang Leng and Chenxi Yan and Junyi Shen and Hao Wang and Weishi MI and Yaying Fei and Xiaoyang Feng and Song Yan and HaoSheng Wang and Linkang Zhan and Yaokai Jia and Pingyu Wu and Haozhen Sun},
      year={2023},
      eprint={2308.09597},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
[![Star History Chart](https://api.star-history.com/svg?repos=LC1332/Chat-Haruhi-Suzumiya&type=Date)](https://star-history.com/#LC1332/Chat-Haruhi-Suzumiya&Date)
---
もし、**ChatHaruhi2.0** のインターフェースデザインなど、このプロジェクトに対するご意見があれば、ぜひお寄せください、
または本レポートの将来のバージョンに参考文献を追加したい場合は、[issue](https://github.com/LC1332/Chat-Haruhi-Suzumiya/issues) を提出してください。


<!--
今後2週間でローカル ChatGLM2-LoRA モデルのマージが完了する予定です。

ChatHaruhi 2.0 Gradio のリリースに伴い、以前の1.0のデータとコードはレガシーリポジトリに移行されます。

ChatHaruhi は、画像や音声などのマルチモーダル機能を追加したオープンソースプロジェクトとして始まり、コンペティションに参加しています。開発者は現在、ソースコードの Gradio デモを試すことができる。しかし、このデザインは、キャラクターの追加、インタラクションの研究、記憶の強化、Unity ゲームバックエンドへの接続といった将来の研究目標には理想的ではありません。

この arxiv リリースの後、私たちは ChatHaruhi を以下のインターフェイスで再構築する予定です:

```python
from ChatHaruhi import ChatHaruhi

chatbot = ChatHaruhi( system_prompt = 'prompt.txt', \
                      story_db = 'story_chroma_folder', \
                      llm = 'openai' )

response = chatbot.chat(text = 'Can you introduce youself?', role = 'Kyon' )
```

システムは、シンプルな system_prompt パラメータとベクトルデータベースをアクセスに使用する。本論文のローカル学習モデル、Claude、Spark API などの LLM の切り替えをサポートする。ChatHaruhi-52K のキャラクターを使った会話については、以下のボックスから直接使用することができます。

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_name = 'baizhantang', llm = 'openai')

response = chatbot.chat(role='汪捕快',text ='小二，来斤好久，再来两盘羊肉！')
```

chatharuhi はすでに pypi に 1 つのバージョンがアップロードされているので、pip install chatharuhi から暫定版をインストールできます。詳しくは: https://github.com/LC1332/Haruhi-2-Dev  -->
