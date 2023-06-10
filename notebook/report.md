# Chat凉宫春日，将京阿尼的人物带到现实

这是一篇记叙性的文档，用于初步描述我们在DataWhale 5月学习中，初步完成的Chat凉宫春日 中的一些细节。

这个项目仍然在招人和进一步进展中，我们希望在完整的项目完成后可以产生一篇更为科学的技术报告，完整的报告、代码和数据将被公开在https://github.com/LC1332/Chat-Haruhi-Suzumiya。

## 引言

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

## 目标

本项目的核心目标，是研究能否能够让自然语言模型在对话中扮演一个动漫或者影视作品中的现实人物。在这个过程中，我们认为一个虚拟人物有三个核心的构成 

- **知识与背景:** 每个虚拟人物都有自己所处在的背景。如《哈利波特》中的人物处在哈利波特的魔法世界。凉宫春日处在一个日本的高中里。其他的动漫人物也有各自的世界设定。所以在ChatBot的构造中，我们希望ChatBot能够了解对应故事的设定。这对于大型语言模型的记忆能力是较大的考验。往往需要通过外部知识库的引入去解决。

- **人格或性格:** 人物的人格和性格设定也是动漫、影视甚至游戏作品中非常重要的部分。人格和性格的设定在整部作品中需要是一致的。有的文学作品在创作时，甚至先定义人物的人格设定，再进行后续的写作工作。所以我们希望ChatBot所反应的人格和性格，与作品原来的设定也是一致的。在6月8日至6月20日之间，Chat凉宫春日的团队会去参加中科院心理所组织的一个特定人格语言生成的[小比赛](https://mp.weixin.qq.com/s/60Lqcum0Ef9DTxqiWIWtsw)，对这方面展开更细节的研究。

- **语言习惯:** 语言习惯是最容易被语言模型进行模仿的，对于近两年的大型语言模型，只要在context中给出合适的例子，语言模型往往会进行模仿输出。这里我们希望这样的文学影视作品的爱好者与ChatBot互动时，能够‘复现’文学影视作品的经典桥段，这样一定会让这些作品的爱好者获得更好的体验。

有很多研究者认为实现这些目标必须通过微调语言模型才能够实现这些目标。本项目会分为两个阶段，在第一个阶段，我们仅仅使用外部知识库和prompting的方法，来实现模仿特定影视人物的ChatBot。在第二个阶段中，我们会讨论如何去自动生成更多的语料并进行模型的微调，可以使用一个本地的模型来完成这样一个ChatBot。在下个章节中马上进入整个项目的完整设计。

## 项目的设想

本项目完整的开发计划如下图所示:

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/bluePrint.jpg">
</p>

在这里我们分模块简单介绍Chat凉宫春日的开发计划，更详细的特征设定可以在[项目的readme](https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main#%E8%AE%A1%E5%88%92feature)中找到。

+ **核心ChatBot:** 根据之前的叙述。我们希望核心的ChatBot部分能够尽可能的能够展现我们要模仿角色的背景、人物性格和语言习惯。这部分主要由一个带搜索的知识库与prompt设计构成。

+ **多样化的前端实现:** 尽管本项目的重点在于prompt的设计和个性化的语言生成。我们也希望能够兼顾用户的使用体验。我们提供三种不同的前端 1. 一个带图文的gradio前端，这个前端可以在colab直接启动。并且随着ChatBot返回的语句，还可以支持搜索剧情中最接近内容的图片进行显示。2. （开发中）一个带语音的web前端，考虑到母语羞涩的问题，我们会把语音翻译成日语再使用VITS等TTS工具进行输出。 3. （计划开发）一个支持LIVE2D人物显示的前端。 我们希望通过多模态、多样化的前端，用户可以以不同方式，更沉浸的感受ChatBot。

+ **自动台词抽取:** 本工作Chat凉宫春日部分的语料是完全手工抽取的。我们正在建立一个能从动画连续剧和台词中，抽取人物间对话的一个系统。这样可以批量自动地生成特定人物的语料。方便更多多样化角色ChatBot的建立。

+ **自动对话生成:**

+ **本地模型训练:**


## ChatBot核心的构造

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/pipeline.png">
</p>


### System Prompt

### 语料与搜索

## 模拟生成更多聊天数据

动机

### 第一句话的生成

### 连续对话的生成

## 辅助工具

## 更多前端的设计

### 实验


## 总结与讨论