中文 | English | 日本語 | [赞助](#赞助) | [报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/report.md) | [招人](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/Hiring.md) | [特定人格的生成](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)

# Chat凉宫春日 Chat-Haruhi-Suzumiya

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)]()
[![Data License](https://img.shields.io/badge/Data%20License-CC%20By%20NC%204.0-red.svg)]()
[![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi)

[**临时体验链接**](https://8b441ca6413e0c004f.gradio.live/) https://8b441ca6413e0c004f.gradio.live/ (三天一换中)

**Chat凉宫春日**是模仿凉宫春日等一系列动漫人物，使用近似语气、个性和剧情聊天的语言模型，

<details>
  <summary> 本项目由李鲁鲁，冷子昂，闫晨曦，封小洋，scixing，沈骏一，Aria Fei, 米唯实, 吴平宇, 贾曜恺等开发。 </summary>

李鲁鲁发起了项目，并完成了最早的版本，在多个微信群实现了测试。完成了训练数据自动生成对话部分，设计了整体的路线，并撰写报告。

冷子昂负责了每一个阶段的Gradio开发，以及每个部分的功能整合和架构设计。

闫晨曦一开始将李鲁鲁的notebook重构为app.py，参与了WebUI的embedding部分重构整合。

封小洋进行了中文转日文模型的选型，完成了针对台词抽取图片的工具。整合了声纹识别。即将继续参加台本工具的开发。

scixing实践了VITS语音，完成了台词对应的语音抽取，实现了第一个版本的声纹分类。

沈骏一实现了使用ChatGLM2 finetune实验

Aria Fei 对接了whisper到台本工具。即将继续参加台本工具的开发。

米唯实实现了Chat哆啦A梦的分支版本

吴平宇部署了ChatGLM2的训练程序，并提供了训练的计算资源。

贾曜恺开发了一个Vue前端实现方案

</details>

本项目是一个[在建项目](#TODO和计划Feature)，本项目中的代码和工具，也支持其他动漫人物的建立。目前初步支持凉宫春日、李云龙、于谦和神里绫华，正在增加更多角色。


<table>
  <tr>
    <td>
      <p align="center">
        <img src="https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/figures/haruhi_suzumiya_bondage_rp.jpg" height="400">
      </p>
    </td>
    <td>
      <ul>
        <li><a href="#快速开始">快速开始</a></li>
        <li><a href="#DemoVideo">DemoVideo</a></li>
        <li><a href="#ChatBot核心的构造">ChatBot核心的构造</a></li>
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

本项目的核心思想是在prompt构造的时候利用[Luotuo-BERT](https://github.com/LC1332/Luotuo-Text-Embedding)，对经典剧情进行了搜索，作为Fewshot（或者说更接近CoT）的构造标准。

Chat凉宫春日是[Luotuo(骆驼)](https://github.com/LC1332/Luotuo-Chinese-LLM)的子项目之一, 后者由李鲁鲁, 冷子昂, 陈启源发起。

本项目采用Apache 2.0协议，也就是你可以利用项目中的代码进行商用。但是你仍然需要遵守包括 1.角色本身的版权方的协议 2.项目中使用的接口方，比如OpenAI的协议， 3.项目中使用的模型的协议（比如如果我们后期采用了LlaMA或者GLM的模型。）

本项目是DataWhale的5月学习的作业，其中闫晨曦，封小洋等同学都由DataWhale社区招募。



## News

[2023-06-24] 增加李云龙、于谦、神里绫华角色数据，更新TODO。

[2023-06-07] 在魔搭社区主办、阿里云和NVIDIA作为联合发起方，天池协办的Create@AI黑客马拉松中，Chat凉宫春日获得二等奖(top3), [讲解视频](https://www.bilibili.com/video/BV1Xh411A7kC/)

[2023-06-03] 在中科院心理所中，项目获得二等奖(top3)，详情请见[链接](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)


## 快速开始



| 名称                                                       |colab链接| 说明                                                                                                               |
|----------------------------------------------------------|---|------------------------------------------------------------------------------------------------------------------|
| Gradio客户端                                                |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/reform_main.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 能够支持角色切换的功能整合客户端                                                                                                 |
| 万恶之源                                                     |<a href="https://colab.research.google.com/github/LC1332/Prophet-Andrew-Ng/blob/main/prophet-code/haruhiLangChain.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 李鲁鲁最早开发的gradio Chat凉宫春日                                                                                          |
| 百度Studio版本                                               | [百度Studio版本](https://aistudio.baidu.com/aistudio/projectdetail/6386896) | 由DataWhale助教-马琦钧开发的百度Studio简化版本                                                                                  |
| HuggingFace版本                                            | [![Huggingface Gradio](https://img.shields.io/static/v1?label=Demo&message=Huggingface%20Gradio&color=orange)](https://huggingface.co/spaces/silk-road/ChatHaruhi) | HuggingFace版本，如果key用完了麻烦提醒我们一下                                                                                   |
| 人格-高考作文                                                  | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/College_essays_gradio.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | 高/低开放性人格对应的高考作文题生成器，[详细报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data) |
| 人格-Chatbot                                               | <a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/PersonalityChatbot.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/> | 高/低开放性人格对应的Chatbot，[详细报告](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)  |
| [5分钟讲解](https://www.bilibili.com/video/BV1Xh411A7kC/)    | | 黑客马拉松B站讲解视频                                                                                                      |
| [DataWhale](https://www.bilibili.com/video/BV1ho4y1P75H) | | DataWhale作业时候的讲解视频                                                                                               |
| [台本工具](https://www.bilibili.com/video/BV1V8411S7eT)      | | 台本工具使用说明                                                                                                         |
| [角色生成工具](https://www.bilibili.com/video/BV1nu411H7Sy/)    | | 角色生成工具使用说明                                                                                                       |
| Chat加藤惠                                                  |<a href="https://colab.research.google.com/github/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/gradio_megumi.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>| 根据群友收集的语料实现的Chat加藤惠                                                                                              |

  
## DemoVideo

注意这个视频是有音频的

https://github.com/LC1332/Chat-Haruhi-Suzumiya/assets/5266090/8b88c8ac-262f-4705-a4e9-489b1ec0ce11

视频中的VITS模型由[凉宫春日应援团](https://space.bilibili.com/201296348)友情提供，具体参数和语速我们还在进一步调优。

## 引言


<details>
  <summary> 冗长的引言 </summary>

随着ChatGPT的发展，用户们逐渐发现可以让大型语言模型进行角色扮演。越来越多的研究和相应的应用也随之产生。有大量基于GPT或者类似语言模型的APP陆续上线，如character.ai，Glow等陆续上线。社区中，关于使用Prompt进行角色扮演的交流讨论也逐渐发酵，在很多prompt分享网站，或者github中，都可以见到大量的讨论。

<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/figure_sample.jpg">
</p>

在大多数的应用中，开发者或者用户使用了类似的prompt。将这样的prompt直接输入在ChatGPT的连续对话中，或者作为system whisper接入到turbo的接口中。

```
Act as 'Character' from 'Movie/Book/Anything'

I want you to act like {character} from {series}. I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use. Do not write any explanations. Only answer like {character}. You must know all of the knowledge of {character}. My first sentence is "Hi {character}."

```

然而，这样prompting虽然实现起来很简单，却有以下缺点: 1. 这样的prompt使用高度依赖大语言模型本来的记忆。如果大语言模型对于觉得的记忆本身是模糊的，则无法模仿特定的角色。 2. 这里的 `know all of the knowledge of {character}` 的定义也是模糊的，无法很好的防御大语言模型`幻觉`效应的产生。 3. 即使是使用这样的prompt，聊天机器人的对话风格还是会很大程度受到语言模型的影响，调整prompt或许能够缓解这样的问题，但是每一个特定的角色都要非常精细的调整prompt。 这些缺点明显限制了这种角色扮演聊天机器人的使用。

</details>

## 目标

本项目的核心目标，是研究能否能够让自然语言模型在对话中扮演一个动漫或者影视作品中的现实人物。在这个过程中，我们认为一个虚拟人物有三个核心的构成 

<details>
  <summary> 知识与背景 </summary>

每个虚拟人物都有自己所处在的背景。如《哈利波特》中的人物处在哈利波特的魔法世界。凉宫春日处在一个日本的高中里。其他的动漫人物也有各自的世界设定。所以在ChatBot的构造中，我们希望ChatBot能够了解对应故事的设定。这对于大型语言模型的记忆能力是较大的考验。往往需要通过外部知识库的引入去解决。

</details>

<details>
  <summary> 人格或性格 </summary>

人物的人格和性格设定也是动漫、影视甚至游戏作品中非常重要的部分。人格和性格的设定在整部作品中需要是一致的。有的文学作品在创作时，甚至先定义人物的人格设定，再进行后续的写作工作。所以我们希望ChatBot所反应的人格和性格，与作品原来的设定也是一致的。在6月8日至6月20日之间，Chat凉宫春日的团队会去参加中科院心理所组织的一个特定人格语言生成的[小比赛](https://mp.weixin.qq.com/s/60Lqcum0Ef9DTxqiWIWtsw)，对这方面展开更细节的研究。

</details>

<details>
  <summary> 语言习惯 </summary>

语言习惯是最容易被语言模型进行模仿的，对于近两年的大型语言模型，只要在context中给出合适的例子，语言模型往往会进行模仿输出。这里我们希望这样的文学影视作品的爱好者与ChatBot互动时，能够‘复现’文学影视作品的经典桥段，这样一定会让这些作品的爱好者获得更好的体验。

有很多研究者认为实现这些目标必须通过微调语言模型才能够实现这些目标。本项目会分为两个阶段，在第一个阶段，我们仅仅使用外部知识库和prompting的方法，来实现模仿特定影视人物的ChatBot。在第二个阶段中，我们会讨论如何去自动生成更多的语料并进行模型的微调，可以使用一个本地的模型来完成这样一个ChatBot。在下个章节中马上进入整个项目的完整设计。

</details>

## ChatBot核心的构造

这个工作的第一阶段尝试我们均使用便宜又好用的turbo3.5模型进行实验。在每一句对话的时候，都会构造一个较长的prompt，这个prompt由系统提示词、剧情桥段、过往对话记忆和新的用户询问4个部分构成。


<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/pipeline.png">
</p>

关于每个部分更详细的解释见[项目的report](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/report.md)

## TODO和计划Feature

最近的TODO:

- [x] 重构台本工具yuki_builder
- [x] 增加李云龙
- [x] 增加于谦
- [x] 增加神里绫华
- [ ] 原神的人物还考虑增加 八重神子，胡桃，钟离，流浪者，雷电将军
- [ ] 增加一些经典武侠人物
- [ ] 预计增加一个项目问答的李鲁鲁人物
- [ ] 重构训练工具 kyon_generator
- [ ] 重新训练Haruhi的ChatGLM2模型
- [ ] 测试端和GLM2整合
- [ ] 集齐多人人物之后上线多人模型

本项目完整的开发计划如下图所示:

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/bluePrint.jpg">
</p>

更详细的模块解释见[项目的report](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/report.md)

我们计划最终产生一个多个前端版本的 Chat凉宫春日，具体特征如下

- Gradio版本

    - 可以在colab启动，方便任何人使用

    - 支持静态图的显示，念白经典台词的时候会同时显示对应的经典画面

    - (opt) 如果Gradio支持语音的话，再做一个合成日文语音的版本

- 本地版本

    - 支持一个Live2D的老婆，口型与语音同步

    - 支持输出的文本转成日文再用合成语音念出来

    - 争取换成haruhi酱的形象

- 后端特征

    - 理论上支持角色更换

    - 日语翻译支持本地/gpt3.5 模型的选择，能不花钱就不花钱呗

    - (后期) 支持使用本地模型去替换gpt3.5，能不花钱就不花钱

- 额外工具

    - 支持从字幕同步的动画片中，抽取特定人物的台词，支持声纹和图片的分类，尽可能抓取到特定人物画面下，这个人的台词。

- (opt)研究部分

    - 研究聊天空间覆盖程度，看看GPT是否能生成更多的聊天

    - 不论用什么方式，把对话数据补充到接近5万条

    - 争取训练自己的Haruhi模型

    - 构思合理的定量化User Study

    - 争取写一个TechReport挂到arxiv


## 获奖

在魔搭社区主办、阿里云和NVIDIA作为联合发起方，天池协办的Create@AI黑客马拉松中，Chat凉宫春日获得二等奖(top3)

在中科院心理所中，项目获得二等奖(top3)，详情请见[链接](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/characters/personality-data)


## 赞助

因为Chat凉宫春日采用了类似CoT的策略，相比于通常聊天，要贵上10-20倍，目前API token都采用社区捐赠的费用来支持。

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
@misc{ChatHaruhi,
  author = {Cheng Li, Ziang Leng, Chenxi Yan, Xiaoyang Feng, SCI xing and Yaokai Jia },
  title = {ChatHaruhi: Reviving Anime Character in Reality via Large Language Model },
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/LC1332/Chat-Haruhi-Suzumiya}},
}
```


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

## TODO

**当前关键进度**

+ 台本工具 —— scixing，封小洋			需求已经确定

封小洋在合并整体程序 0629，希望0630能够整体调通出一版（最好是colab能跑）

+ 重构WebUI —— 冷子昂，闫晨曦			需求已经确定

据说已经初步有一个版本，今天上传到git并且做链接？

+ 推广精品角色到3个  （等待台本工具）

+ 尝试0613新特征 —— 米唯实			初步探索中

我今天和米唯实讨论一下

+ 训练本地模型 —— 沈骏一、张财、吴平宇 需求已经确定

看看BaoBig粒可视化的进度，最好等台本工具结束补一批数据生成。

---

生成和实测数据的可视化

- [ ] 确认收到实测和生成的数据
- [ ] 尽可能整理成一问一答的相同格式

阿虚:「说了一句话」
春日:「说了一句话」

- [ ] 拿相同格式的文本抽取embedding
- [ ] 用新发现的牛逼工具可视化

https://colab.research.google.com/drive/1GNdmBnc5UA7OYBZPtHu244eiAN-0IMZA?usp=sharing#scrollTo=XBF1d3mMh6vq

- [ ] 跑一下，如果新工具支持中文，那万事大吉
- [ ] 如果新工具不支持中文，可以把外部标签改成英文，但是内部点的时候还是尽量看到中文

- [ ] 可以用之前的tSNE

---

如果做训练的话，沈骏一把生成数据也接手一下

- [ ] 原来剧本中(后一句有haruhi说话的）台词，可以全部都用标准haruhi的pipeline 生成一遍

不是continuous

不能复现原有角色的话，可以认为训练失败了

试一下ChatGLM2，看看能不能tuning

---

封小洋 is working on that

- [ ] 已经验证了声纹的1-NN是有效的
- [ ] 有一个Python基础切分的程序
- [ ] 在每个人物标注5-10段语音情况下，可以开始跑脚本
- [ ] （扩充） 假设我们可以在脚本中删除人觉得错误的行，甚至修正一些角色名，这些数据可以作为补充，程序会读取一个人工修正（有删失）的脚本，进一步扩充标定数据

---
[Aria Fei](https://github.com/ariafyy) is working on that

使用鲁叔标定的数据，测试更多的声纹模型

标定数据

https://drive.google.com/file/d/1u-GhdIwinaxv8q4aelWRd9HXtGvWK2E7/view?usp=sharing

原始数据

https://drive.google.com/file/d/164yjLh0zN_7kcfW94b0fHXl8Pn2RXlWs/view?usp=sharing

https://drive.google.com/file/d/1cB-sQ1Yo6OlVV_7Lcg99gamCubfowtsL/view?usp=sharing

