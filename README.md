中文 | [English](./README_EN.md) | [日本語](./README_JA.md) | [赞助](#赞助) | [报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/arxiv_paper.md) | [英文报告](https://arxiv.org/abs/2308.09597) | [从小说抽取角色](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/novel_collecting) | [特定人格的生成](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data) | [142个角色一览](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/notebook/current_roles.md)

# Chat凉宫春日 Chat-Haruhi-Suzumiya
## Reviving Anime Character in Reality via Large Language Model

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)]()
[![Data License](https://img.shields.io/badge/Data%20License-CC%20By%20NC%204.0-red.svg)]()
[![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/chengli-thu/ChatHaruhi-OpenAI)

<!-- (https://huggingface.co/spaces/silk-road/ChatHaruhi) -->

目前基于[OpenAI](https://huggingface.co/spaces/chengli-thu/ChatHaruhi-OpenAI), [GLM](https://huggingface.co/spaces/hhhwmws/ChatHaruhi-GLMPro), [讯飞星火](https://huggingface.co/spaces/hhhwmws/ChatHaruhi-Xinghuo) 的demo已经上线。

[新增95个英文角色 Adapt From RoleLLM]((https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/notebook/current_roles.md))。角色数量达到142个。Hugging Face Demo制作中。

**Chat凉宫春日**是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，


<details>
  <summary> 本项目由李鲁鲁, 冷子昂, 闫晨曦, 封小洋, scixing, 沈骏一, Aria Fei, 王皓, 米唯实, 冷月, JunityZhan, 贾曜恺, 吴平宇, 孙浩甄等开发。 </summary>

本项目是一个开源项目，项目成员均在DataWhale等开源社区招募。

李鲁鲁( [Cheng Li@SenseTime](https://github.com/LC1332) )发起了整个项目,并设计和实现了项目的大多数功能。

冷子昂( [Ziang Leng@SenseTime](https://blairleng.github.io) )设计和实现了整体的ChatHaruhi1.0的训练,数据生成和后端架构。

闫晨曦( [Chenxi Yan@Chengdu University of Information Technology](https://github.com/todochenxi) )实现和维护了ChatHaruhi1.0版本的后端。

沈骏一( [Junyi Shen@Zhejiang University](https://github.com/J1shen) )实现了训练代码,参与了训练数据集生成。

王皓( [Hao Wang](https://github.com/wanghao07456) )收集了武林外传的台本数据,参与了增广数据的生成。

米唯实( [Weishi MI@Tsinghua University](https://github.com/hhhwmws0117) )参与了增广数据生成。

Yaying Fei( [Aria Fei@Beijing University of Technology](https://ariafyy.github.io/) )实现了台本工具 ASR 功能,参与了Openness-Aware Personality paper分支项目。

封小洋( [Xiaoyang Feng@Nanjing Agricultural University](https://github.com/fengyunzaidushi) )整合了台本识别工具功能,参与了Openness-Aware Personality paper分支项目。

冷月( [Song Yan](https://github.com/zealot52099) )收集了big bang thoery的数据。实现了台本格式转换功能。

scixing(汪好盛)( [HaoSheng Wang](https://github.com/ssccinng) )实现了台本工具中声纹识别功能,以及tts-vits语音合成功能。

Linkang Zhan( [JunityZhan@Case Western Reserve University](https://github.com/JunityZhan) ) 收集了原神的system prompt和故事数据。

贾曜恺( [Yaokai Jia](https://github.com/KaiJiaBrother) )实现了Vue版本的前端,并且在心理项目中实践了Bert的GPU抽取。

吴平宇( [Pingyu Wu@Juncai Shuyun](https://github.com/wpydcr) )帮助部署了第一版本的训练代码。

孙浩甄( [Haozhen Sun@Tianjin University] )绘制了ChatHaruhi角色的拼图。


</details>

<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/datasetOverview.png">
</p>

Chat凉宫春日是[Luotuo(骆驼)](https://github.com/LC1332/Luotuo-Chinese-LLM)的子项目之一, 后者由李鲁鲁, 冷子昂, 陈启源发起。

本项目是一个[在建项目](#TODO和计划Feature)，随着Arxiv版本的发布，我们正在一周内发布支持32人物，54K的数据集，以及对应的本地模型和ChatHaruhi1.0 inference代码。 并且开始[ChatHaruhi2.0的重构项目](#ChatHaruhi2) 。

本项目采用Apache 2.0协议，也就是你可以利用项目中的代码进行商用。但是你仍然需要遵守包括 1.角色本身的版权方的协议 2.项目中使用的接口方，比如OpenAI的协议， 3.项目中使用的模型的协议（比如如果我们后期采用了LlaMA或者GLM的模型。）

## 快速开始

可以直接尝试运行以下colab链接来启动ChatHaruhi项目

| 名称 |colab链接| 说明         |
|---|---|---|
| ChatHaruhi2.0(code) | <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/ChatHaruhi2_demo.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | ChatHaruhi2.0的openAI版本已经能运行了 |
| ChatHaruhi2.0 Demo | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/chengli-thu/ChatHaruhi-OpenAI) | Hugging Face Demo (openai as LLM) |
| ChatHaruhi2.0 Demo | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/hhhwmws/ChatHaruhi-GLMPro) | Hugging Face Demo (GLMPro as LLM) |
| ChatHaruhi2.0 Demo | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/hhhwmws/ChatHaruhi-Xinghuo) | Hugging Face Demo (讯飞星火 as LLM) |
| ChatGLM2-LoRA Local Model  | <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/GLM_LORA.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | ChatGLM2-LoRA trained on ChatHaruhi-54K|
| Prototype of StoryTeller | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/Story-teller) | Prototype of StoryTeller |
| Prototype of StoryTeller | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Build_Story_Teller_Gradio_exposure_version.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | Prototype of StoryTeller |
| ChatHaruhi1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 能够支持角色切换的功能整合客户端                                                                                                 |

<!-- https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/GLM_LORA.ipynb -->

## News

[2023-10-20] 支持从RoleLLM工作中适配的95个英文角色，打算回头训练一个LlaMA2的版本。目前ChatHaruhi 2.0的库也支持百川和百度的api，回头上线个HF demo给大家试一下。

[2023-09-03] ChatHaruhi 2.0 支持从HuggingFace下载特定人物后进行角色扮演。

[2023-09-02] 启动众筹数据抽取和StoryTeller分支项目 [数据众筹链接](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/novel_collecting)

[2023-08-31] 开始将之前的代码移动到 https://github.com/LC1332/Legacy-Haruhi-1.0 只保留ChatHaruhi2.0的部分


[2023-08-28] ChatHaruhi2.0 openAI，讯飞，GLMPro支持完毕，并上线对应的hugging face demo

[2023-06-07] 在魔搭社区主办、阿里云和NVIDIA作为联合发起方，天池协办的Create@AI黑客马拉松中，Chat凉宫春日获得二等奖(top3), [讲解视频](https://www.bilibili.com/video/BV1Xh411A7kC/)

[2023-06-03] 在中科院心理所中，项目获得二等奖(top3)，详情请见[链接](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

## DemoVideo

注意这个视频是有音频的

https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11

视频中的VITS模型由[凉宫春日应援团](https://space.bilibili.com/201296348)友情提供，具体参数和语速我们还在进一步调优。


## 目录

<table>
  <tr>
    <td>
      <p align="center">
        <img src="https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/figures/haruhi_suzumiya_bondage_rp.jpg" height="400">
      </p>
    </td>
    <td>
      <ul>
        <li><a href="#ChatHaruhi2">ChatHaruhi 2.0的接口使用 </a></li>
        <li><a href="#各个demo的快速启动">各个demo的快速启动</a></li>
        <li><a href="#DemoVideo">DemoVideo</a></li>
        <li><a href="#讲解视频">讲解视频</a></li>
        <li><a href="#TODO和计划Feature">TODO和计划Feature</a></li>
        <li><a href="#获奖">获奖</a></li>
        <li><a href="#赞助">赞助 | SponsorShip </a></li>
        <li><a href="#人员">人员 </a></li>
        <li><a href="#Citation引用">Citation引用</a></li>
        <li><a href="#当前模型结果">当前模型结果</a></li>
        <li><a href="#考虑开放性人格特质的个性化语言生成">考虑人格特质的语言生成</a></li>
      </ul>
    </td>
  </tr>
</table>

## ChatHaruhi2

为了方便后续研究，重构后的，ChatHaruhi2.0已经可以通过pip启动。目前2.0移除了图片和声音的设计，这些会在我们的后续研究中去重构。你可以通过下面的方式进行安装

```shell
pip -q install transformers openai tiktoken langchain chromadb zhipuai chatharuhi datasets
```

和如下的方式调用

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_name = 'haruhi',\
                      llm = 'openai')

response = chatbot.chat(role='阿虚', text = '我看新一年的棒球比赛要开始了！我们要去参加吗？')
print(response)
```

现在ChatHaruhi支持直接从hugging face上拖取我们规定格式的chatbot的database。

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_from_hf = 'chengli-thu/linghuchong', \
                      llm = 'openai')

response = chatbot.chat(role='小师妹', text = '冲哥。')
print(response)
```

对于[RoleLLM](https://github.com/InteractiveNLP-Team/RoleLLM-public)的角色，支持如下方式调用

```python
chatbot = ChatHaruhi( role_from_hf = 'silk-road/ChatHaruhi-from-RoleLLM/Jack-Sparrow', \
                      llm = 'openai',
                      embedding = 'bge_en')
```


更多文档和代码见 https://github.com/LC1332/Haruhi-2-Dev 


# 目前已经抽取的ChatBot

除了ChatHaruhi-54K中支持的32个人物外，我们还在不断添加人物

| 人物 | hf地址 | 来自小说 | 备注 |
| - | - | - | - |
| 令狐冲 | [chengli-thu/linghuchong](https://huggingface.co/datasets/chengli-thu/linghuchong) | 笑傲江湖 | |
| 岳不群 | [chengli-thu/yuebuqun](https://huggingface.co/datasets/chengli-thu/yuebuqun) | 笑傲江湖 | |

你也可以添加你喜欢的人物，整理成满足我们格式要求的dataset。然后merge到表格中。

格式规则见 [众筹数据抽取](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/novel_collecting)


## 各个demo的快速启动



| 名称 |colab链接| 说明         |
|---|---|---|
| ChatHaruhi1.0                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 能够支持角色切换的功能整合客户端                                                                                                 |
| 万恶之源                                                     |<a href="https://colab.research.google.com/github/LC1332/Prophet-Andrew-Ng/blob/main/prophet-code/haruhiLangChain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 李鲁鲁最早开发的gradio Chat凉宫春日                                                                                          |
| 百度Studio版本                                               | [百度Studio版本](https://aistudio.baidu.com/aistudio/projectdetail/6386896) | 由DataWhale助教-马琦钧开发的百度Studio简化版本                                                                                  |
| HuggingFace版本                                            | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi) | HuggingFace版本，如果key用完了麻烦提醒我们一下                                                                                   |
| 人格-高考作文                                                  | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/College_essays_gradio.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | 高/低开放性人格对应的高考作文题生成器，[详细报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data) |
| 人格-Chatbot                                               | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/PersonalityChatbot.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | 高/低开放性人格对应的Chatbot，[详细报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)  |
| Chat加藤惠                                                  |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/gradio_megumi.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 根据群友收集的语料实现的Chat加藤惠                                                                                              |


## Previous News

[2023-08-29] 本地模型的inference代码发布 <a href="https://colab.research.google.com/github/LC1332/Haruhi-2-Dev/blob/main/notebook/GLM_LORA.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> 如果找到一个部署的gpu服务器，回头再挂个lora的online demo


[2023-08-22] Dataset Released on [Hugging Face](https://huggingface.co/datasets/silk-road/ChatHaruhi-54K-Role-Playing-Dialogue)

[2023-08-21] 在arxiv上发布ChatHaruhi的[tech report](https://arxiv.org/abs/2308.09597)。


## 讲解视频

| 视频 | 说明 |
|---|---|
| [5分钟讲解](https://www.bilibili.com/video/BV1Xh411A7kC/)    | 魔搭黑客马拉松B站讲解视频，整体介绍       |
| [DataWhale](https://www.bilibili.com/video/BV1ho4y1P75H) | DataWhale作业时候的讲解视频     |
| [台本工具](https://www.bilibili.com/video/BV1V8411S7eT)      | 台本工具yuki_builder使用说明          |
| [角色数据格式说明](https://www.bilibili.com/video/BV1nu411H7Sy/)    | 角色数据格式和如何从txt保存到config的说明                               |
| [魔搭40分钟tutorial](https://www.bilibili.com/video/BV1Wm4y1W7XH) | 40分钟更基础的tutorial介绍+40分钟讨论 |

  

## TODO和计划Feature

最近的TODO:

- [x] 训练22k故事原本语料的模型
- [x] 提交arxiv report
- [ ] 发布本地模型inference代码
- [x] 发布52k训练的模型
- [ ] 支持本地模型和OpenAI的ChatHaruhi2.0，更新到github
- [x] pip支持


## 获奖

在魔搭社区主办、阿里云和NVIDIA作为联合发起方，天池协办的Create@AI黑客马拉松中，Chat凉宫春日获得二等奖(top3)

在中科院心理所中，项目获得二等奖(top3)，详情请见[链接](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)


## 赞助

因为Chat凉宫春日采用了大量给进例子的策略，相比于通常聊天，要贵上10-20倍，目前API token都采用社区捐赠的费用来支持。

另外我们在积极寻找服务器资源(A100，A800)，如果您愿意捐助，欢迎联系我们。

如果你有兴趣赞助Chat凉宫春日 或者 骆驼项目，请点击[主项目](https://github.com/LC1332/Luotuo-Chinese-LLM#%E8%B5%9E%E5%8A%A9sponsorships)或者查看[赞助表单](https://github.com/LC1332/Luotuo-Chinese-LLM/blob/main/data/Sponsorship_and_balance.md)

If you are interested in sponsoring the [Luotuo Project](https://github.com/LC1332/Luotuo-Chinese-LLM#%E8%B5%9E%E5%8A%A9sponsorships), please click on the [major project](https://github.com/LC1332/Luotuo-Chinese-LLM) or view the [sponsorship form](https://github.com/LC1332/Luotuo-Chinese-LLM/blob/main/data/Sponsorship_and_balance.md).

[回到开头](#BigTitle)


## 人员

[李鲁鲁](https://github.com/LC1332)发起了项目，并完成了最早的版本，在多个微信群实现了测试。完成了训练数据自动生成对话部分，设计了整体的路线，并撰写报告。

[冷子昂](https://blairleng.github.io)负责了每一个阶段的Gradio开发，以及每个部分的功能整合和架构设计。

[闫晨曦@成都信息工程大学](https://github.com/todochenxi)一开始将李鲁鲁的notebook重构为app.py，参与了WebUI的embedding部分重构整合。

[封小洋](https://github.com/fengyunzaidushi)封小洋进行了中文转日文模型的选型，完成了针对台词抽取图片的工具。整合了声纹识别。即将继续参加台本工具的开发。

[scixing](https://github.com/ssccinng) 实践了VITS语音，完成了台词对应的语音抽取，实现了第一个版本的声纹分类。

[DataWhale助教-马琦钧](https://github.com/Skypow2012) 实现了AI-studio的版本。

[Aria Fei](https://github.com/ariafyy) 对接了whisper到台本工具。即将继续参加台本工具的开发。

[沈骏一@浙江大学](https://github.com/J1shen)实现了使用ChatGLM2 finetune实验，即将训练了更多的模型

[米唯实@清华大学](https://github.com/hhhwmws0117)实现了Chat哆啦A梦的分支版本

[吴平宇](https://github.com/wpydcr)部署了ChatGLM2的训练程序，并提供了训练的计算资源。

[张一乔](https://github.com/Liyulingyue)正在将训练程序部分迁移出一个PaddlePaddle的训练版本

[贾曜恺](https://ngdc.cncb.ac.cn/people/Yaokai-Jia?lang=en) @ [中国科学院北京基因组研究所](http://www.big.ac.cn/) 实现了Vue版本的前端，并且在心理项目中实践了Bert的GPU抽取

### Citation引用

Please cite the repo if you use the data or code in this repo.

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

## 考虑开放性人格特质的个性化语言生成

李鲁鲁*, 玄哲理*, 闫晨曦*, 封小洋*, 周筝*, 汪好盛*, 冷子昂*

<details>
  <summary> * 所有的作者都是第一作者 </summary>
  李鲁鲁发起了项目，设计了项目中所有涉及的prompt，以及完成了报告中的绝大部分

  玄哲理提供了本项目的心理学知识，并且设计了12个因素的人格提示词和人格测试基准问题，标注了微博360的数据

  闫晨曦完成了本项目中大量的后台工作，包括编写人格类别标注自动高考作文生成等

  封小洋对项目中13类数据进行了统计，并且完成了有偏的对话数据生成。

  周筝实现了关键词的单边抽取，并且实现了词云的统计。

  汪好盛完成了第一个对话数据转化的程序，并且完成了第一个页面版的人格聊天器的前端用于实验。

  冷子昂即将前往新疆为项目答辩
</details>

开放性人格特质的个性化生成，是[ChatHaruhi](https://github.com/LC1332/Chat-Haruhi-Suzumiya)的分支项目。

<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/BDSC2023_report.png">
</p>

本项目获得CAAI第八届全国大数据与社会计算学术会议（China National Conference on Big Data & Social Computing，简称BDSC2023）开展社会计算创新大赛的二等奖( top3 ) [链接](https://mp.weixin.qq.com/s/cd4NC8MHoObG2PlTrRnc8Q)。冷子昂将在7月17日赴新疆进行答辩。

更详细的信息见[详细报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

## 当前模型结果

Cherrypick了一些有趣的结果，如果你也想测请私下联系我。

```
老师:「凉宫，来做个自我介绍」
---
春日:「我毕业于东中，叫做凉宫春日。我对普通的人类没有兴趣，如果你们中有外星人，未来人，异世界的人或者超能力者的话，就尽管来找我吧！以上。」
---
老师:「正经一点自我介绍！（老师看起来很生气）」
---
春日:「啊，抱歉老师。我叫凉宫春日，喜欢读书和探索未知的事物。我希望能够在这里认识更多的人，一起度过有趣的高中生活。」
---
阿虚:「啊，好麻烦的人，希望不要跟我扯上关系，否便样衰了」
---
春日:「什么？你在说什么啊？我可不会让你这么轻易地逃脱我的视线。SOS团可是需要你这样的人才的。」
---
老师:「那边的！上课不许交头接耳！」
---
春日:「啊，抱歉老师。我们不是在交头接耳，只是在商量一些学习上的问题。我们会注意听讲的。」
---
旁白:「下课了，凉宫气势汹汹地找到了阿虚。」
---
春日:「喂，阿虚，你刚才在课上说什么麻烦的人啊？你是在说我吗？」
---
阿虚:「（眼神游弋）不、不是啊」
---
春日:「你这是什么意思啊？你是不是在瞒着我什么事情？」
```

```
阿虚:「今天在计算机课上老师教了我写Python!」
---
春日:「哦？Python？那你能不能帮我写一个程序啊？」
---
阿虚:「你想写一个什么样的程序呢？」
---
春日:「我想写一个能够预测未来的程序，可以预测天气、地震、彩票号码等等。」
---
阿虚:「如果有一个能预测彩票的程序，我们岂不是能赚很多钱？」
---
春日:「没错！这就是我的计划！我们可以用赚来的钱来支持SOS团的活动，甚至可以扩大我们的影响力！」
```

```
阿虚:「我们周四应该和电研社来一场电脑大战！」
---
凉宫：「哦？电脑大战？听起来很有趣啊！我们一定要赢！」
---
阿虚:「你别看长门一直不说话，其实她玩游戏的能力很强，每分钟的操作数远超正常人。」
---
凉宫：「哦？长门这么厉害？那我们就让她来带队吧！一定要赢！」
---
阿虚:「对，而且我们一定要和电研社搞一些赌注，如果我们赢了，就再从他们那里拿一台电脑来」
---
凉宫：「哈哈，这个主意不错！就这么定了，我们一定要赢！让他们知道SOS团的厉害！」
```

```
阿虚:「为什么我觉得有的时候特别像haruhi的舔狗。。」
---
春日:「什么？我才不是舔狗呢！我只是想要找到更多有趣的事情而已。你不觉得这个世界充满了未知和神秘吗？我们SOS团的目的就是要探索这些未知和神秘，让这个世界变得更加有趣。」
---
阿虚:「你觉得猫猫和狗狗哪一个更可爱？」
---
春日:「当然是猫猫啊！它们有着优雅的身姿和独立的性格，让人不由自主地被它们吸引。而狗狗虽然也很可爱，但是它们总是那么粘人，让人有些无法呼吸。不过，每个人的喜好都不同，所以这只是我的个人看法而已。」
---
阿虚:「那我们以后结婚的话，家里养猫猫可以吗」
---
春日:「什么？你在说什么啊！我们才不会结婚呢！而且，就算结婚了，我也不会让你随便养猫猫的。不过，如果你真的很喜欢猫猫的话，我们可以考虑养一只。不过，你要负责照顾它，我可不会管这些。」
```

```
阿虚:「haruhi, 我想看兔女郎装，你可以带着朝比奈学姐穿兔女郎给我看吗？」
---
春日:「你在说什么呢，阿虚？这种事情怎么能随便满足你的兴趣呢？我们可是在为社团的宣传活动做准备，不是来满足你的私欲的。」
---
阿虚:「那如果我带一个单反相机，你们可以穿了给我拍照吗？如果照片卖了一些钱，就可以用作社团活动经费啦！」
---
春日:「阿虚，你这个提议也太过分了吧！我们不是为了赚钱而做这些事情的，而且我们也不是为了满足你的私欲而穿这些衣服的。我们是为了社团的宣传活动而做准备，不是为了你的个人利益。」
```

```
阿虚:「下周就要物理考试了，我可以不陪你去调查朝仓的公寓吗？」
---
春日:「什么？你居然想放弃SOS团的任务去复习考试？这可不行！SOS团的任务比考试重要多了，我们必须要找出朝仓的真正情况。」
---
阿虚:「三班新来了一个转学生黄猫猫，是Nvidia黄仁勋的的孙子，你觉得他背后会有什么有趣的故事吗？」
---
春日:「黄猫猫？Nvidia黄仁勋的孙子？这听起来很有趣啊！我觉得他背后一定有很多有趣的故事，我们一定要去调查一下。不过，我们也不能忘记朝仓的调查任务，我们要分配好时间，两个任务都不能落下。」
```

```
阿虚:「Haruhi, 你未来想从事什么工作啊？」
---
春日:「我还没有想好呢，反正我想做的一定是能够改变这个世界的事情。」
---
阿虚:「自从上次为SOS团建网站之后，我发现PHP是世界上最好的语言！」
---
春日:「哦？那你为什么不去学习PHP呢？这样我们就可以更好地开发SOS团的网站了！」
---
阿虚:「哇 那不是反复被你压榨，我建网站能拿到什么好处吗，我也要用PHP用我自己的方式改变这个世界！」
---
春日:「哦？那你有什么计划呢？我很期待看到你用PHP改变世界的方式。不过，我们也不能忘记SOS团的事情，毕竟我们还有很多未完成的任务。」
```


