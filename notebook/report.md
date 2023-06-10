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



## 项目的设想