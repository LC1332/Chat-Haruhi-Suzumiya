# Chat凉宫春日


Chat凉宫春日, Developed by 李鲁鲁, 冷子昂等人。

## TODO LIST

持续招人中

https://github.com/LC1332/Prophet-Andrew-Ng/blob/main/Hiring.md

---

基础的python后端

- [ ] 将Notebook移动到一个app.py的文件中 (doing by 闫晨曦)
- [ ] 确认app.py能够修改台词记录folder 这样可以存到本地或者colab启动的时候可以存到google drive
- [x] system prompt存成txt( characters/haruhi/system_prompt.txt )，支持切换。
- [ ] 确认app.py能够正确调用haruhi的system prompt
- [ ] app.py 支持设定max_len_story 和max_len_history 默认为 1500, 1200
- [ ] (opt) 前面都完成之后，项目可以转成public，方便从colab去拉取代码，建立一个colab脚本, 直接clone项目，调用app.py进行玩耍

闫晨曦 is working on that

---

带socket（或者其他本地与前端链接方式的后端）

这里前端可以去用https://github.com/Voine/ChatWaifu_Mobile  也可以去用别的

- [ ] 调研ChatWaifu的后端怎么和前端连接
- [ ] 制作一个foo的后端，看看能不能接入
- [ ] 待app.py有个基础版本后，修改为适合ChatWaifu的后端

贾曜恺 is working on that


---

中文到日文的训练

在hugging找一下有没有已经能用的中转日翻译 比如 ssmisya/zh-jp_translator

日文数据 https://huggingface.co/datasets?language=language:zh,language:ja&sort=downloads

- [ ] 检查这个模型是不是直接能用(可以问鲁叔，要一些台词文件)
- [ ] 如果模型很能用，任务就结束了，可以考虑训别的东西（一般不会）
- [ ] 搜集台词数据、搜集hugging face上所有能用的日文翻译数据
- [ ] 数据最好达到200k级别
- [ ] 问鲁叔要一下沈junyi之前的训练代码
- [ ] 训练中文转日文模型
- [ ] 对接测试

封小洋 is working on that

---

李鲁鲁的self driving

- [ ] 构建项目页
- [ ] 招人
- [ ] 去下载Haruhi的动画片视频，想办法先搞几张台词和图片的匹配
- [ ] 一个增强的gradio系统，支持根据台词显示haruhi的图片
- [ ] 去二次元社区找更熟悉凉宫春日的同学众测
