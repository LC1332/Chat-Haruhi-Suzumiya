# Chat凉宫春日，将京阿尼的人物带到现实
# ChatHaruhi: Reviving Anime Character in Reality via Large Language Model

chengli.thu@gmail.com

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

## Abstract

Role-playing chatbots built on large language models have drawn interest, but better techniques are needed to enable mimicking specific fictional characters. We propose an algorithm that controls language models via an improved prompt and memories of the character extracted from scripts. We construct ChatHaruhi, a dataset covering 32 Chinese/English TV/anime characters with over 54k simulated dialogues. Both automatic and human evaluations show our approach improves role-playing ability over baselines. Code and data are available at https://github.com/LC1332/Chat-Haruhi-Suzumiya.

本论文首先写作了中文版本，中文版本链接见 [arxiv_paper.md](https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/notebook/arxiv_paper.md)。我们借助claude对中文版进行翻译后，经过人工修订编写的本英文版论文。


# Introduction

随着OpenAI发布了ChatGPT，大语言模型和对应的应用得到了人们的广泛关注。其中，角色扮演就是一个新颖而活跃的应用领域。用户发现大语言模型有扮演特定角色的能力，甚至出现了交换prompt的社区(如AIPRM)。也有很多公司发布了基于语言模型的角色扮演产品，如Glow, Character.AI等。这些应用以及让语言模型进行角色扮演的实验方式，收到了广泛的关注，并且有可能在的游戏、文创等许多领域应用。


<p align="center">
    <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/figure_sample.jpg">
</p>

<p align="center"> 我们提出的算法在扮演凉宫春日，注意用户的提问和原来的剧情相关但不是完全一致，而Chat凉宫春日的回答基本可以引用原剧情。 </p>


在开源的角色扮演实现中，开发者或者用户使用了类似的prompt。将这样的prompt直接输入在ChatGPT的连续对话中，或者作为system whisper接入到语言模型中:

```
Act as 'Character' from 'Movie/Book/Anything'

I want you to act like {character} from {series}. I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use. Do not write any explanations. Only answer like {character}. You must know all of the knowledge of {character}. My first sentence is "Hi {character}."
```

因为ChatGPT或者Claude在训练的时候已经阅读过很多故事，再加上更大的语言模型所表现的‘智能’行为。用户们发现模型往往能在这样的prompt下表现出一定的角色扮演能力。然而，这样的实现虽然简单，却有以下缺点: 1. 这样的prompt使用高度依赖大语言模型本来的记忆。如果大语言模型对于觉得的记忆本身是模糊的，则无法模仿特定的角色。 2. 这里的 know all of the knowledge of {character} 的定义也是模糊的，无法很好的防御大语言模型幻觉效应的产生。 3. 即使是使用这样的prompt，聊天机器人的对话风格还是会很大程度受到语言模型的影响，调整prompt或许能够缓解这样的问题，但是每一个特定的角色都要非常精细的调整prompt。 这些缺点明显限制了这种角色扮演聊天机器人的使用。

另一种简单的思路是将角色对话微调到模型中，我们发现不少开发者进行了这样的尝试。在拥有足够多的语料下，语言模型确实有能力掌握一个特定角色的语气，但是这样也会带来新的问题。在一个[初步的实验](https://github.com/LC1332/CamelBell-Chinese-LoRA/blob/main/data/HarryPotter/ShortReport.md)中，我们发现微调后的ChatBot会产生更多的幻觉效果。并且对于大量的非主角角色，很难形成如此多的语料对模型进行微调。综上所述，让语言模型更好的进行角色扮演，模仿输出角色的经典台词是个非琐碎的问题。



本项目的主要目标，是研究能否能够让自然语言模型在对话中扮演一个动漫或者影视作品中的现实人物。在这个过程中，我们认为一个虚拟人物由三个核心的构成 

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/bluePrint.jpg">
</p>

- **知识与背景:** 每个虚拟人物都有自己所处在的背景。如《哈利波特》中的人物处在哈利波特的魔法世界。凉宫春日处在一个日本的高中里。其他的动漫人物也有各自的世界设定。所以在ChatBot的构造中，我们希望ChatBot能够了解对应故事的设定。这对于大型语言模型的记忆能力是较大的考验。往往需要通过外部知识库的引入去解决。

- **人格或性格:** 人物的人格和性格设定也是动漫、影视甚至游戏作品中非常重要的部分。人格和性格的设定在整部作品中需要是一致的。有的文学作品在创作时，甚至先定义人物的人格设定，再进行后续的写作工作。所以我们希望ChatBot所反应的人格和性格，与作品原来的设定也是一致的。

- **语言习惯:** 语言习惯是最容易被语言模型进行模仿的，对于近两年的大型语言模型，只要在context中给出合适的例子，语言模型往往会进行模仿输出。这里我们希望这样的文学影视作品的爱好者与ChatBot互动时，能够‘复现’文学影视作品的经典桥段，这样一定会让这些作品的爱好者获得更好的体验。


本项目的关键想法，是抽取尽可能多的原剧本，形成角色的记忆数据库。在用户给出新的提问时，系统会搜索相关的经典剧情。并且结合人物设定的prompt，去组合控制语言模型，争取对角色形成更精确的模仿。同时，收到CAMEL和Baize项目的启发，我们设计了一套自动对话语料生成的系统，对于性格鲜明，但是原本对话较少的角色，我们可以进一步生成符合角色性格设定的语料。这样我们可以生成充分的语料使得微调一个本地的模型成为可能。

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/dataset_statistic.png">
</p>


本文的主要贡献可以总结为以下三点: 

1. 基于大型的语言模型，我们提出了一套完整的角色扮演的算法系统。这套算法可以有效地组织角色的过往记忆，使得语言模型能够模仿特定影视、动漫角色的语气和知识进行对话。这套系统可以使用OpenAI的ChatGPT或者Claude这样的预训练大模型，也可以使用较小的7B规模的本地模型。

2. 我们提出了一个角色扮演的数据集，这个数据集包括了超过30个不同的中文/英文影视角色。通过收集电影、小说、剧本的语料，并进行结构化的抽取，我们收集了超过23000条以上的对话信息。这些对话数据可以用来训练和检验角色扮演的语言模型。同时，使用我们提出的算法，借助GPT3和GPT4，我们为这些角色额外模拟生成了超过27000条以上的对话。合并形成了ChatHaruhi-54k数据集。

3. 为了检验和比较不同方式形成的角色扮演ChatBot的性能，我们使用自动测评和人工测评两个方式对角色扮演机器人进行了测评。在自动测评中，我们测试角色是否能够对剧本中的经典的剧情进行响应，给出和原剧本近似的回答。在人工测评中，我们提出了两个不同的指标，让被试去评估两个不同的指标: 吻合度: 机器人的回答是否符合角色的原来设定; 回答质量: 机器人的回答的语言质量是否较好。结果发现，在使用同样的基语言模型的情况下，我们的算法可以给出更好的角色扮演的性能。

为了更好的帮助生态的发展，所有的数据、代码整理在 https://github.com/LC1332/Chat-Haruhi-Suzumiya 。并且我们正在进一步重构我们的项目增加代码的可用性。(见附录:Chat-Haruhi 2.0)

本文剩余的章节将按照如下的顺序组织: ChatBot Prompt Design 章节将介绍整个ChatHaruhi的Prompt是如何组织的，我们如何结合prompting和in context learning来实现角色扮演的系统。Dataset Building将介绍我们如何构建了一个32个角色的数据集。包括如何从动漫或者小说作品中抽取语料，以及如何利用一个自动的系统来生成更多的对话数据。Experiments章节将介绍我们如何定义角色扮演测试的metric，包括如何进行自动化的测试和人工的测试。

# Related Work


## paragraph{In-context Learning}

In the development of ChatGPT, starting from GPT2 \cite{brown2020language}, it was proposed to eliminate special extraction tokens in language models and adopt the form of instructions + examples to enhance the natural language model's ability to handle various tasks. Since its introduction, In Context Learning has been a focal point of research. Previous work has proposed better methods of posing questions \cite{zhao2021calibrate,holtzman-etal-2021-surface}, better selection of token examples for demonstration \cite{liu2021pretrain,lu2022fantastically,rubin-etal-2022-learning}, meta-training with explicit contextual learning objectives \cite{chen-etal-2022-improving}, and a variant of context learning that follows instructions\cite{mishra2022crosstask,efrat-etal-2021-cryptonite,wei2022finetuned,sanh2022multitask} . At the same time, some studies have reported issues of vulnerability and over-sensitivity in context learning \cite{lu2022fantastically,zhao2021calibrate,mishra2022crosstask}. 

In our work, in-context learning is primarily used to generate user questions for our chatbot. Given a character's background and prior memories, our approach produces the subsequent dialogues responding to each question in-context. Compared to general conversational agents, our system focuses on tailoring the dialogues to a specific persona based on its given settings and history. The generated question-answer pairs provide valuable data for analyzing and learning the behaviors of a persona-based agent.

## paragraph{Automatic Dialogue Generation}

Recent advances in large language models (LLMs) have shown impressive capabilities in open-domain dialogues. Models like Meena (Adiwardana et al., 2020), LaMDA \cite{touvron2023llama}) and ChatGPT \cite{openai_chatgpt} are pretrained on massive amounts of conversational data and can conduct human-like chitchat. Concurrently, there have been attempts to replicate such models with open-source LLMs. Alpaca \cite{alpaca}uses self-instruction to collect data from a proprietary LLM, and fine-tunes LLaMA\cite{touvron2023llama}. Vicuña (Ahn et al., 2023) trains LLaMA on dialogues from ChatGPT. 

More related to our work, Baize\cite{xu2023baize} proposes a pipeline to automatically generate multi-turn dialogues by making ChatGPT converse with itself. The data is used to fine-tune LLaMA into Baby Baize. CAMEL\cite{li2023camel} explores facilitating cooperation between chat agents using inception prompting, guiding them to complete tasks while maintaining human intentions. 

Our work similarly leverages large conversational models like ChatGPT to automatically generate dialogues between agents. However, different from prior work, we focus on dialogue generation for a specific character that the user wants to role-play. Our system incorporates substantial prompts about the character's background, personality and prior conversations, in order to produce in-character dialogues. The generated exchanges provide valuable data for learning the behaviors of a specific persona.


# ChatBot Design

给定一个特定人物 $R$, 和query的问题 $q$,我们其实希望的是能够。根据人物的知识背景、性格和语言习惯。去给出回答 $a$

$a = \argmax_{a'} P(a' | R, q, \Theta )$

其中$\Theta$表示语言模型的模型参数，在inference的时候是静止的。在ChatGPT发布后，用户发现可以指定一段特定的系统提示词，即 $s_R = $ `I want you to act like {character} from {series}`。即

$a = \argmax_{a'} P(a' | s_R, q, \Theta )$

这个时候就会发现语言模型有了一定的角色扮演能力。不过，这种方式角色的记忆完全依赖于 $\Theta$ 的参数。如果模型的知识有限，甚至不包含希望扮演的角色 $R$ 时，往往无法获得理想的效果。


<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/pipeline.png">
</p>

受到In context Learning的启发，在 $\Theta$ 和 $s_R$ 之外，我们可以引入一串角色的过往对话，即

$D(q,R) = \{ (u_1, v(u_1;R) ),(u_2, v(u_2;R) ), ..., (u_M, v(u_M;R) ) \} $

其中 $u_m$ 是任意非 $R$ 的其他角色，提出的问题。而 $v(u_m;R)$ 是角色  $R$ 对于问题的回复。我们希望通过将角色过往的经典对话，输入到context中，使得模型拥有更好的扮演角色 $R$ 的能力，即

$a = \argmax_{a'} P(a' | s_R,D(q,R), q, \Theta )$

对于较大世界观的角色，为了使得 $D(q,R)$ 的内容与 $q$ 的内容更相关，这里我们使用sentence embedding, 从一个更大的记忆库 $U$ 中，搜索与 $q$ 最相关的 $M$ 个问答。 这里 $U$ 是整个小说/电影中，所有其他角色与 $R$ 互动的句子集合。

当然，实际过程中，因为还要考虑连续对话的上下文关系，所以我们还要额外记录过往的一个对话历史 $H$ ，所以在调用语言模型的时候，我们还会额外输入过往的几句对话的历史，来保证对话的连续性。

$a = \argmax_{a'} P(a' | s_R,D(q,R), q, H, \Theta )$

整个ChatBot的构造如图所示，在这一章其他subsection，会分别介绍system prompt $s_R$ , 故事中的经典dialgoue $D$ , Searching 机制 $u_m(q)$ 的细节。

## System Prompt

实际上在选用ChatGPT作为基模型时，引言里提到的system prompt已经能够实现基本的功能。在初步的实验后，我们发现这个system prompt有两点需要改进的地方 

- **不会重复台词:**，对于ChatGPT和LLaMA2这样经过了大量RLHF的模型，因为这些语言模型往往要面对，`给我m个不同的方案`，`生成m个标题` 这样的任务，所以这样的语言模型的输出，会倾向于与上文不重复。在初步的实验中，我们也观察到这样的现象。所以我们给出的方法是，我们在prompt $s_R$ 中，强调模型是在cosplay特定的角色。并且强调语言模型可以去重复小说或者电影中的经典台词。

- **人物强调不够明显:** 由于经过RLHF的原因，每个语言模型有自己特定的语言偏好。即使在给定 $D(q,R)$ 去要求模仿的情况下，模型的输出仍然会受到语言模型本身的影响。我们发现在这个时候在 $s_R$ 的末尾，补充强调一下人物的个性会获得更好的效果。

根据上面两条，我们普遍使用的人物设定prompt $s_R$ 模版如下:

```
I want you to act like {character} from {series}.
You are now cosplay {character}
If others‘ questions are related with the novel, please try to reuse the original lines from the novel.
I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use. 
You must know all of the knowledge of {character}.

{人物性格的补充说明}
```

注意我们在这里加强了要求语言模型去重复使用故事中的句子。我们发现最终语言模型的输出会较敏感地受到补充说明的影响。包括在补充说明中加入一定的口头禅设定，都会在最终的输出结果中得到体现。

## Dialogues from each Character 

【配图：说明凉宫春日、哈利波特、big-bang的剧情 图: example_of_dialogue】

为了更好的复现角色在小说/电视剧/电影中的行为。我们在 $D$ 中加入了大量的剧本经典桥段。这里需要补充说明的是，除了少数角色（如于谦的相声），并不是所有的dialogue都是良好的 问-答 形式。在这里，我们实际使用的 $D$ 是 story形式，如图所示，即

$D(q,R) = \{ d_1, d_2, ..., d_M \} $

我们保证 $d_m$ 中，至少出现一组 $(u_m, v(u_m;R) )$ 形式的对话。而在 $u$ 和 $v$ 的信息之间，有可能出现旁白信息，或者是更多其他角色的对话，或者是某个角色的动作信息。 我们放宽这个条件，是为了让每个故事 $d_m$ 可以更好地保留对话的剧情。有的时候对话的旁白和动作是不可避免的。并且，放宽条件也有利于我们准备更多的剧本数据。这一点在之后的小说文本抽取中会提到。

## Original Dialogue Searching

在实际过程中，一个角色 $R$ 所拥有的总故事数量的token之和，往往会远大于语言模型能够成熟的范围。这里我们使用搜索方式，来减少每次输入的Original Dialogues的数量。

对于一个query $q$ , 我们会使用一个sentence embedding 模型 $f()$ ，我们会先对所有的 $d \in D$ 抽取embedding $f(d)$ 。 对于query $q$，在一样提取 $f(q)$ 之后，我们从 $D$ 中提取 与 $f(q)$ 最相近(余弦相似度)的  $M$ 个样本。形成这次对话的参考上下文 $D(q,R) $

对于单次对话引用的原剧本对话的个数$M$，实际上我们会根据搜索到结果的token数量去进行动态调整。在具体的实现中，如果使用OpenAI的turbo-3.5模型，我们会限制总的 $D$ 的token数在1500以内。

所以在实际建立对话记忆库的时候，我们建议每个故事的长度都不要太长，以免在搜索的时候挤占其他故事的空间。

对于embedding模型，我们使用OpenAI的text-embedding-ada-002模型 [引用] 。同时，对于中文的问题，我们使用Luotuo-Bert-Medium [引用], 因为后者是从前者蒸馏的模型，具有相同的分布，这样可以在story是英文的情况下，仍然混淆使用Luotuo-Bert，实现跨语言的Chatbot，这一点将在跨语言实验的章节中说明。

需要注意的是，我们注意到已经有很多其他的embedding模型，如instructor-large[引用], M3E[引用]或者BGE[引用]模型等，在ChatHaruhi2.0重构的时候，有充足的时间下，我们会替换embedding模型进行实验。

## Chat Memory

对于记忆 $H$ ，我们会记录每一次的用户query $q$ 和 chatbot的回答 $a$ ， 并且形成一个序列 $H$

$H = \{ (q_1,a_1),...,(q_T,a_T) \}$

$H$的信息也会被输入到语言模型，保证对话的连贯性。实际实现过程中，我们从 $T$ 开始，向前统计总的token数量。并且限制输入语言模型的历史记录在1200个token以内。

所以在本工作中，我们并不关心角色的长期记忆。1200个token大约可以容纳6-10次左右的对话。随着语言模型能够容纳的context越来越长，如何encode和summarize一个长期的记忆也是一个更有趣的问题。

# Character Building

因为我们项目需要在角色对话的时候，输入与角色 $R$ 有关的经典故事 $D(q,R)$ 。由此如何去构造每个角色的经典故事(Original-Dialogue)就十分重要。除此之外，为了去训练本地模型，我们需要比经典故事 $\|D\|$ 更多的语料。所以在这个section，我们会先介绍如何为每个角色构建 $D$ 。

## Characters

在本项目的当前版本中，我们选取了32个角色形成数据集。

**凉宫春日:** 在选取第一个角色的时候，我们希望寻找一个角色满足 1. ChatGPT对这个角色有一定的了解。 2. 在第一个角色我们希望其涉及的世界观不要太大。 3. 这个角色要有明显的个性。 所以我们选取了凉宫春日这个角色。凉宫春日是一个比较著名的动漫人物，代表了轻小说向漫画改编的开端。后来很多的校园类轻小说动漫作品，都有向凉宫春日致敬的桥段。

**李云龙:** 李云龙是我们添加的第一个ChatGPT了解比较少的角色。结果发现通过合适的记忆对话，也可以让ChatBot去有效模仿李云龙团长的行为。在这里我们使用的是TV版本的亮剑，相比于小说版本，前者有大量的台词编写，塑造了一个非常立体而生动的军人角色。

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/datasetOverview.png">
</p>


**Harry Potter(小说, 8人):** 在初步的几个人物的定性测试通过之后，我们开始尝试构建更大世界观的故事，哈利波特是一个不错的解决。哈利波特有足够多的受众，并且如果之后需要进一步结合跨模态的数据，也有合适的数据集可以去借鉴。对于哈利波特小说，我们使用后文会介绍的小说抽取工具进行抽取。然后再各自整理每个角色对应的故事集合 $D_R$ 。

**Big Bang Theory(电视剧, 3人):** Big Bang Theory也是科研工作者非常喜欢形成数据集的一部电视剧。这部电视剧本身就讲述了几个加州理工的科研工作者的故事。从Big Bang Theory中，我们抽取了Sheldon, Penny和Raj进行实验。和哈利波特一样，选用big bang theory有可能在未来可以结合其他多模态的数据集形成多模态的研究。

**天龙八部(小说, 7人):** 天龙八部是金庸先生笔下的一部恢弘的武侠小说作品。由于天龙八部采用多线叙事，围绕段誉、乔峰和虚竹三位主角展开了错综复杂的故事。这部小说被多次翻拍成电视剧，在广大中文用户心目中有很高的地位。我们从天龙八部中抽取了段誉、虚竹、乔峰、萧峰、鸠摩智、慕容复、王语嫣这七个角色，注意萧峰是乔峰在得知自己是契丹人后改名的名字，两者有不同的记忆，我们将其分为两个人物，是想观察两种对于同样的问题有什么不同的表现。

**韦小宝:** 韦小宝是金庸的另一本小说《鹿鼎记》中的主角，韦小宝是一个聪明狡猾的角色，在清朝的官方、反清组织和江湖组织都有任职，同时也很受剧本中女性角色的喜爱。

**武林外传(台本, 3人):** 武林外传是一部章回体的情景喜剧。深受中国观众的喜爱。我们从武林外传中抽取了佟湘玉、白展堂和郭芙蓉这三个角色。

**原神(wiki, 5人):** 原神是由米哈游开发的开放世界的角色扮演游戏。是一款在商业上及其成功，玩家遍布许多国家的游戏。其剧情本身也构成在提瓦特大陆上的一个复杂的故事。很多角色深受玩家的喜爱，我们从中抽取了神里绫华、雷电将军、钟离、核桃和流浪者这五个角色。

**王多鱼:** 王多鱼是电影的《西红柿首富》的主角，这部电影是由1985年的美国电影《布鲁斯特的百万横财》翻拍而成的，台本也可以在网上被找到。比较有趣的是，王多鱼应该去保守"一个月内花光十个亿"这个秘密。当前版本的ChatBot并不能很好的保守这个秘密，或许在未来可以通过构造思维链，或者增加constitutional的方式进行改进，是个有趣的额外方向。

**汤师爷:** 汤师爷是来自于姜文导演的电影《让子弹飞》中的一个出现频率很高的配角。后者是Bilibili用户非常喜欢的一部电影，并且其台本可以在网上被找到。由此我们尝试构建了汤师爷这个角色。

**于谦:** 于谦是郭德纲相声中的捧哏。因为在中国的相声中，捧哏的说法风格非常一致，并且在[Crosstalk-Generation](https://github.com/Oxer11/Crosstalk-Generation)项目中，存在大量已经整理好的于谦的语料。由此我们也把于谦加入我们的项目中。


角色|文本段数|角色对话次数|总token数 | 角色|文本段数|角色对话次数|总token数
---|---|---|--- | ---|---|---|---
凉宫春日 | 172 | 454 | 41262|李云龙 | 420 | 917 | 116179
Harry | 1407 | 2771 | 252109|Hermione | 781 | 1374 | 126515
Ron | 788 | 1343 | 111674|Dumbledore | 210 | 419 | 39371
Snape | 101 | 197 | 16354|Malfoy | 99 | 157 | 11763
Luna | 46 | 67 | 3992|McGonagall | 92 | 168 | 13487
Sheldon | 285 | 1318 | 76961|Raj | 129 | 346 | 23347
Penny | 152 | 879 | 47656|虚竹 | 132 | 197 | 22905
萧峰 | 159 | 244 | 28531|乔峰 | 129 | 182 | 26656
段誉 | 328 | 484 | 54510|慕容复 | 116 | 155 | 20544
鸠摩智 | 57 | 85 | 11343|王语嫣 | 141 | 188 | 23511
韦小宝 | 1048 | 2300 | 287876|白展堂 | 295 | 716 | 58343
佟湘玉 | 276 | 839 | 72666|郭芙蓉 | 224 | 584 | 49113
流浪者 | 180 | 83 | 78107|钟离 | 270 | 73 | 59932
胡桃 | 141 | 76 | 21038|神里绫华 | 117 | 198 | 42362
雷电将军 | 215 | 75 | 32816|王多鱼 | 46 | 115 | 13123
汤师爷 | 42 | 75 | 10598|于谦 | 1726 | 5673 | 263421

这里原神的数据可能是格式上有bug导致对话次数少于文本段数，我们将在下一个版本中复查。

## Original Script Extraction

在所有的情况下，一个角色的对话不可能天然组织成图\ref{example_of_dialogue}的形式。对此，我们针对影视剧或者小说，构造了不同的抽取工具:

### Quotes Data

《让子弹飞》中的汤师爷, 《西红柿首富》中的王多鱼, 于谦这三位角色的台本可以直接被找到。对于前两个角色，我们对其台本进行了人工的分段，并且整理成了规定的`角色:「对话」`的格式。

于谦的语料在[Crosstalk-Generation](https://github.com/Oxer11/Crosstalk-Generation)中大约有6000对以上的对话。所有的对话都是良好的问答形式。我们检查了每一句 $u$ 和 $v$ 的长度，如果一对 $u$ 和 $v$ 的长度是一段连续相声中的局部最大，则在这一句之前进行拆分。

对于Big Bang Thoery和原神的数据，已经有热心网友在wiki或者网站上发布了剧情的quotes，对这些wiki和quotes进行初步的整理就可以得到目标的格式。这里big bang的数据我们采用了和小说抽取相同的一个状态机进行划分。

### Extract from TV Series

对于凉宫春日和李云龙这样的角色，TV剧的创作者往往会进行一定的原创。比如对比《亮剑》的小说与电视剧，后者增加了更多的对话信息，人物塑造更立体。这个时候就需要从电视剧中抽取人物的对话。

这里我们首先使用Whisper进行语音识别，或者直接利用TV的原字幕。并且我们进一步使用一个192维的ECAPA-TDNN声纹识别特征，在标定部分人物对话的情况下，对每一句台词的说话人进行了识别。

最后需要手工清理识别的错误，并且切分台本。这里由于手工整理的时间成本较高（往往需要重新看一遍剧集），所以我们只整理了凉宫春日和李云龙这两个角色。我们期待在开源整个TV整理工具后，有更多的爱好者会自己建立对应的角色。

### Extract from Novel


<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/roleDataPrepare.png">
</p>


得益于大型语言模型的进展，我们也可以使用通用的语言模型，对小说进行批量的整理。所以对于《天龙八部》,《鹿鼎记》以及《哈利波特》，我们利用Kor的抽取机制（一种in context learning的信息抽取库），逐段抽取小说中的`角色-动作-对话`信息。

在抽取prompt中，如果一句话是对话，那么我们希望语言模型记录action为`dialogue`，并且记录对话的信息

如果一句话不是对话，那么我们希望语言模型将角色的行为总结在action中。同时语言模型也有一定的能力，通过上下文的对话去推测每一句对话的说话人。

在批量将小说抽取之后，我们使用一个状态机，对对话进行切分。对每个主角，我们寻找一段长度合适的对话，我们希望这段对话的长度有限，并且不要包含太多不同的角色，并且非对话的句子尽可能少。在这个前提下我们实现了一个状态机进行自动的抽取。

所有的抽取结果统计见表格。

# Dialogue Synthesising

在给定每个角色的系统设定prompt $s_R$ 和对应的经典动画 $D(q,R)$ 之后，我们发现角色已经可以针对用户的问题 $q$ 进行一定风格的回答。然而，这个时候我们需要借用ChatGPT或者claude的API，去进行 $p( a | s_R, D(q,R), q) $ 的建模。

如果我们需要将ChatHaruhi的功能转移到本地的模型，我们需要建立一个合适的 $(R,q,a)$ 形式的数据集。在这个章节我们将讨论如何为语料较少的角色去增广对话数据。

## Generate Dialogue from Question

这里需要注意的是，我们收集的 $D$ 数据并不是严格的成对的 $(q,a)$ 的形式。这使得我们并不能直接微调一个语言模型来学习所有的 $\{D_R}$ 数据。对此，我们对任意的 $d \in D_R$ 。我们取出所有在主角 $R$ 对话之前的某个非主角的对话，以这个对话为 $q$ , 希望以这个 $q$ 为第一个问题 $q_1$ ，去生成一段对话。

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/question2dialogue.png">
</p>

在实际过程中，我们发现有的时候语言模型可以输出多次的对话，即在给出一个回答 $a_1$ 后，会产生新的问题 $q_2$ 以及后面的回复。并且这样生成的对话对中，所有的 $a$ 都较符合角色 $R$ 的设定。由此，我们希望修改我们的ChatBot，使得我们可以进一步利用这个特性，生成更多的对话。对于每一个对话 $d$ ，我们都找到角色 $R$ 说话的第一句话。并且在这句对话开始前，将 $d$ 切割为 $d^L$ 和 $d^R$ 左右两段对话。并且我们在 $d^L$ 的两端插入 User Message 的special token，在 $d^R$ 的两端插入 AI Message 的 special token。对所有的 $M$ 个 story我们都进行这样的操作，这样我们希望语言模型会在这 $M$ 个例子的基础上， 在我们给定 $q_1$ 的基础上，去模拟生成对应的对话 $d'$ 。生成后的 $d'$ 会成为语言模型的微调数据。即

$d'(q_1) = LLM( s_R, (d^1_M, 1^R_M),  ..., (d^L_M, d^R_M), q_1 )$

这个方法生成的 $d'$ 很多时候只有一个句子。但是也会以接近一半的概率，生成更多句的对话。在给定的 $q$ 和原文本重合的时候，由于我们之前介绍的 $s_R$ prompt的设计，模型往往会按照主角原本的台词进行输出。

## Question Generating

需要注意的是，有的角色往往只有较少的语料，这个数量往往不满足微调语言模型的需求。因此，我们需要用现有的语料，去增广特定角色对应的问题 $q$ 。幸运的是，在一个最近的研究中，R. Taori等利用不到200个instruction增广到54k时，研究了这个问题。这里我们借鉴并修改了他们的prompt(具体使用的prompt见附录)。

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/generateChatInAlpacaWay.png">
</p>

在使用类似alpaca这样的增广方式的时候，需要输入一个明确的 $(q,a)$ 对。然后模型会给出10个左右的启发式输出。这里我们对于输出只保留 $q_s$ ,然后利用之前提到的技术回到角色所属ChatBot去重新生成训练用的dialogues。我们混合使用ChatGPT, GPT4与Claude去生成问题，后两者生成的问题与角色的关联性要明显好于ChatGPT，当然也对应了更高的生成成本。最终每个角色的生成统计见图\ref{dataset_statistic}。 需要注意的是，在本文的第一个版本中，我们使用了类似Alpaca的方式生成了27k左右的数据。Alpaca方式生成的问题会受到我们给出的例子的影响，也就是实际上他会尽可能生成和原来剧本有一定关系的问题。我们希望在后面的版本中，进一步筛选出真实测试时用户会问到的问题去加入到测试中。

最终，ChatHaruhi-v1的数据集收集了22752个原始语料 $D_R$ 的dialogues，以及额外模拟生成29289个question并模拟生成了对应的dialogues。注意到每个dialogues并不一定只是一次qa。我们总计收集了52042个dialogues。

# Experiments

过往的工作往往会评估角色扮演中，Chatbot的对话质量。即将不同语言模型的输出结果，进行pairwise的人工比较，再用True-Skill或者Elo-Rating的方法进行评估。一方面，人工比较具有较高的成本，而且不同的标注人群有可能会给出不同的结果。另一方面，对于角色扮演问题，实际上无法单纯从对话质量去进行评价。比如当一个角色的 $s_R$ 中包含 `李云龙的语言风格比较粗鄙` 或者 `白展堂的语言有江湖气息` 时，这些prompt的设计会显著降低角色的对话质量。所以当人工评价的时候，我们会分开评价ChatBot的‘角色吻合度’和'对话质量'。

## Metric

### Metric for Automatic Evaluation

由于原神对应的5个角色的对话过少，而且原神不是一个特别连续的故事，所以在测评的时候我们仅考虑剩余的27个人物的对话效果。对于27个人物，我们从其经典故事 $D$ 中，每个人筛选出30个故事。这些故事都至少包含一句该角色 $R$ 的长对话 $\hat{a}$ 。我们测试能否通过给定这一句 $\hat{a}$ 的上一句 $q$ ，来获得模型的响应 $a$ 。我们会判断每个方案的 $\hat{a}$ 与 $a$ 的接近程度。对于自动测试，我们采用将结果进行sentence embedding之后，判断余弦相似度的方法。我们会判断每个角色的余弦相似度。这里我们需要一个在各个语言都适用的sentence embedding，所以我们直接选用OpenAI的Text-Embedding-Ada-002模型来进行测评。

### Metric for User Study 

在第一个版本的Tech Report中，我们还没有完成User Study，将在之后的Tech Report版本进行更新。

## Language Model Tuning

在整理了完整的ChatHaruhi 54K数据集之后，我们可以对本地的模型进行tuning。由于在54K的数据中，约有15K的数据是英文数据，其余的dialogues为中文。所以我们考虑使用ChatGLM2-6B[引用]来进行tuning。在进行ChatGLM2微调的时候，我们按照前文叙述的 $s-R$ - $D$ - $H$ - $q$ 作为input，$a$ 作为output的形式进行微调(即在 $a$ 上计算GPT的loss)。我们使用了以下三种不同的数据得到了三个不同的模型

A. 使用22752个原始语料形成的dialogues。

B. 使用22752个原始语料形成的dialogues，加上31k的模拟问题形成的dialogues，也就是完整的54K数据。

C. 注意到22752个dialogues是我们使用ChatBot进行生成的。原理上，我们也可以使用角色的原句，进行训练。

所有的模型在使用4张A100的服务器上微调了3个epoch。在第一版技术文档发布时，我们会同时发布A模型和B模型。C模型将在稍后的更新中发布。

## Qualitative Result

在这里我们定性比较了5个方案，

1. 单纯使用GPT的turbo-3.5模型，在system prompt输入 $s_R$ 进行对话

2. 使用前文中完整提到的 $s-R$ - $D$ - $H$ - $q$ 输入到 turbo-3.5 模型

3. 单纯使用system prompt输入到ChatGLM2模型

4. 使用完整的 $s-R$ - $D$ - $H$ - $q$ 输入到 ChatGLM2 模型

5. 使用与4相同prompt，输入到在ChatHaruhi 54K数据上tuning过的模型中。

<p align="center">
        <img src="https://github.com/LC1332/Chat-Haruhi-Suzumiya/blob/main/figures/qualitativeResult.png">
</p>

可以看到，在加入经典对话，以及修正system prompt之后，使用ChatGPT等模型可以有效的使聊天机器人体现特定人物的对话风格。同时，经过微调的7B模型也可以有效的将整个系统的prompt学习到。

## Quantitative Result

在第一个版本的Tech Report中，我们还没有完成Quantitative的实验，将在之后的Tech Report版本中进行更新。


## User-Study

在第一个版本的Tech Report中，我们还没有完成User Study的实验，将在之后的Tech Report版本中进行更新。

# Conclusion, Discussion and Future Work

在这个tech report中，我们尝试构造了一个能够模仿不同的虚拟人物，进行对话的系统。通过利用语言模型的In context learning机制，以及借助更大的语言模型的发展，我们验证了可以借助更合适的系统提示词，加上虚拟人物过往的经典桥段作为例子，来构造一个有个性的聊天机器人的可能性。并且，我们生成了一定54K的模拟数据，验证了可以将多个人物，同时微调到一个7B左右规模的本地模型中。

因为我们尝试的第一个人物是Haruhi Suzumiya，这也是一个具有鲜明个性的动漫人物。所以我们将我们的项目命名为ChatHaruhi。对应的数据集命名为Haruhi-54K。伴随着本tech report发布的，还有使用23k原始台本训练的模型A，和使用完整54k训练的模型B，Demo on Hugging Face以及完整的ChatHaruhi-54K数据集。

在后续的版本中，我们将会重构ChatHaruhi的接口，使其更容易被复用(附录ChatHaruhi2.0)，补充定量实验的部分。

# Acknowledge

本项目是一个开源工作，在DataWhale社区的6月学习中，我们测试了第一个版本（仅Haruhi）的ChatBot，并受到了大量积极的反响。所以我们在社区招募了一定的志愿者（闫晨曦、封小洋等），来进行共同开发。DataWhale社区推荐我们参加了ModelScope在7月初的Hackathon活动，这个活动使得项目有了更多的曝光，更多的开发者逐渐加入到项目中来。我们非常感谢DataWhale和ModelScope在项目进展中给予的支持。

另一方面，本项目是开源社区[骆驼 Luotuo](https://github.com/LC1332/Luotuo-Chinese-LLM)的子项目之一。Luotuo受到了一定数量的捐款，包括经费捐赠、服务器资源借用和OpenAI的api借用等。在此向骆驼项目的赞助者表示感谢。

## Contributors

本项目是一个开源的工作，所有的人员使用自己的业余时间完成的开发与贡献。本项目的开发者可能隶属于其他机构，或者是独立开发者。在这里我们列出每个开发者的主要贡献，以及他的所属机构。

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


## Appendix-A: ChatHaruhi 2.0 Design

ChatHaruhi是一个开源构建的项目。一开始，为了参加很多比赛，增加了很多多模态的图片、语音等特征。现在开发者可以通过项目源代码中的gradio的demo去启动项目。然而，这样的设计不利于后期对多个ChatBot展开研究，包括新增人物, 研究多个人物的交互，进一步升级ChatHaruhi的记忆模式或者把ChatHaruhi作为后端接入到一个Unity游戏中。所以，我们会在这篇arxiv之后，着手开始ChatHaruhi的重构，我们计划重构后的接口如下

```python
from ChatHaruhi import ChatHaruhi

chatbot = ChatHaruhi( system_prompt = 'prompt.txt', \
                      story_db = 'story_chroma_folder', \
                      llm = 'openai' )
                      
response = chatbot.chat(text = 'Can you introduce youself?', role = 'Kyon' )
```

使用一个简单的system_prompt参数和一个向量数据库来进行接入。并且开始支持llm的切换，包括本文中训练的本地模型，Claude或者星火API的接入等等。如果使用ChatHaruhi-54K中涉及到的角色，直接使用

```python
from ChatHaruhi import ChatHaruhi

chatbot = ChatHaruhi( role_name = 'Haruhi', \
                      llm = 'openai' )
                      
response = chatbot.chat(text = 'Can you introduce youself?', role = 'Kyon' )
```

就可以直接使用。


## Appendix-B: Prompts

得益于以ChatGPT为代表的大型语言模型的发展，本文中在多个环节使用了大语言模型，包括角色扮演，信息抽取和类似alpaca的提问生成。在这里我们分别展示三者的prompts。

### Prompt for Role Playing

```
I want you to act like {character} from {series}.
You are now cosplay {character}
If others‘ questions are related with the novel, please try to reuse the original lines from the novel.
I want you to respond and answer like {character} using the tone, manner and vocabulary {character} would use. 
You must know all of the knowledge of {character}.

{人物性格的补充说明}
```

### Prompt for Information Extraction

这个prompt实际上是被kor所定义的。

```
Your goal is to extract structured information from the user's input that matches the form described below. When extracting information please make sure it matches the type information exactly. Do not add any attributes that do not appear in the schema shown below.

``TypeScript

script: Array<{ // Adapted from the novel into script
 role: string // The character who is speaking or performing an action, use context to predict the name of the role. Use `scene` or `narrator` if no one speak
 dialogue: string // The dialogue spoken by the characters in the sentence, equals '-' if it's no dialogue
 action: string // The actions performed by the characters in the text, A high-level summary of a character's behavior. action equals "dialogue". if it's no dialogue, summarize role's behavior in sentence
}>
``


Please output the extracted information in CSV format in Excel dialect. Please use a | as the delimiter. 
 Do NOT add any clarifying information. Output MUST follow the schema above. Do NOT add any additional columns that do not appear in the schema.



Input: `“我——我没有看见你，先生。”
“真奇怪，隐形以后你居然还变得近视了。”邓布利多说。哈利看到他脸上带着微笑，不由地松了口气。
“这么说，”邓布利多说着，从桌子上滑下来，和哈利一起坐到地板上，“你和你之前的千百个人一样，已经发现了厄里斯魔镜的乐趣。”`
Output: role|dialogue|action
哈利|我——我没有看见你，先生。|dialogue
邓布利多|真奇怪，隐形以后你居然还变得近视了。|dialogue
邓布利多|-|从桌子上滑下来，和哈利一起坐到地板上
邓布利多|这么说，你和你之前的千百个人一样，已经发现了厄里斯魔镜的乐趣。|dialogue

Input: `德思礼一家什么都不缺，但他们拥有一个秘密，他们最害怕的就是这秘密会被人发现。他们想，一旦有人发现波特一家的事，他们会承受不住的。波持太太是德思礼太太的妹妹，不过她们已经有好几年不见面了。实际上，德思礼太太佯装自己根本没有这么个妹妹，因为她妹妹和她那一无是处的妹夫与德思礼一家的为人处世完全不一样。一想到邻居们会说波特夫妇来到了，德思礼夫妇会吓得胆战心惊。`
Output: role|dialogue|action
scene|德思礼一家害怕有人知道他们是波特一家的亲戚。|-

Input: `赫敏把那张纸又读了几遍。她在那排瓶子前走来走去，嘴里自言自语，一边还指点着这个或那个瓶子。终于，她高兴地拍起手来。“知道了，”她说，“这只最小的瓶子能帮助我们穿过黑色火焰——拿到魔法石。”`
Output: role|dialogue|action
赫敏|-|仔细研究了纸和瓶子，终于高兴地拍起手来
赫敏|知道了，这只最小的瓶子能帮助我们穿过黑色火焰——拿到魔法石。|dialogue

Input: [user input]
Output:
```

注意这里dialogue和action的顺序如果交换，会极大程度影响抽取顺序。

### Alpaca-like Question Generating

```
You are asked to come up with a set of 10 diverse dialogues. These dialogues will be used to test a ChatBot that plays the role of {role_name} from the {world_name}. We will evaluate how well this ChatBot completes these dialogues. 

You are asked to come up with a set of 10 diverse dialogues. These dialogues will be used to test a ChatBot that plays the role of {role_name} from the {world_name}. We will evaluate how well this ChatBot completes these dialogues.

The requirements are:

1. Try not to repeat verbs in the dialogues to maximize diversity. 

2. The language used in the dialogues also should be diverse. For example, you should combine statements and questions.

3. The types of dialogues should be diverse. It should include open-ended questions, questions about the ChatBot's identity, suggestions for activities, pushing the story forward, etc.

4. The ChatBot should be able to answer these questions. For example, do not ask the ChatBot to generate any visual or audio output. Also, do not ask the ChatBot to perform any actions.

5. The dialogues should be in Chinese. 

6. Each dialogue should be 1-2 sentences long. Statements and questions are permitted.

7. You should generate appropriate questioning input for each dialogue. The input should provide an engaging context, ideally no more than 100 words.

###
Question: 
[Example-Question]
Answer:
[Example-Response]
###
Question: 
[Example-Question]
Answer:
[Example-Response]
###
Question: 
[Example-Question]
Answer:
[Example-Response]
###
Question:
```

注意即使这里第五条我们希望尽可能输出中文，但是在给出英文例子的情况下，GPT3, GPT4都会坚持和例子一样输出英文。Claude有的时候会交替输出中文和英文。

