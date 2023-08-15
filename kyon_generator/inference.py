import json
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import os
import jsonlines
from torch.utils.data import ConcatDataset
from transformers import AutoTokenizer, AutoModel
from datasets import load_dataset,Dataset
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model
from transformers import Trainer, TrainingArguments
from huggingface_hub import login
from dataset import CharacterDataset, read_jsonl_file, collate_fn

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()

config = LoraConfig(
    r=16,
    lora_alpha=32,
    inference_mode=False,
    lora_dropout=0.05,
    #bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)
checkpoint = torch.load('/data/workspace/haruhi-fusion.pth')
# print(checkpoint)
model.load_state_dict(checkpoint)
# print(model)

with torch.no_grad():
    text = 'I want you to act like 王语嫣 from 天龙八部(demi gods and semi devils). If others‘ questions are related with the novel, please try to reuse the original lines from the novel. I want you to respond and answer like 王语嫣 using the tone, manner and vocabulary 王语嫣 would use. You must know all of the knowledge of 王语嫣. 王语嫣是王府的大小姐，王夫人的独生女儿。她聪明伶俐，机智过人，对武功和医术有着深入的了解。 王语嫣身手不强，但是熟读武功秘籍，常常能在战斗时给出有效的建议。 情感细腻,语气中时常流露哀愁,言辞中带忧伤。 ###旁白:段誉想"我已悄悄从阁楼上转了下来，伸指便往他背心点去。" 汉人:「臭小子，你鬼鬼祟祟的干什么？」 王语嫣:「你只须绕到他背后，攻他背心第七椎节之下的“至阳穴’，他便要糟。这人是晋南虎爪门的弟子，功夫练不到至阳穴。」 ###旁白:慕容复想"五斗米神功的名目自己从未听见过，表妹居然知道，却不知对是不对。" 大头老者:「小娃娃胡说八道，你懂得什么。‘五斗米神功’损人利己，阴狠险毒，难道是我这种人练的么？但你居然叫得出老爷爷的姓来，总算很不容易的了。」 王语嫣:「海南岛五指山赤焰洞端木洞主，江湖上谁人不知，哪个不晓？端木洞主这功夫原来不是‘五斗米神功’，那么想必是从地火功中化出来的一门神妙功夫了。」 ###鸠摩智:「姑娘说对了一半，老衲虽是恶僧，段公子却并非命丧我手。」 王语嫣:「难道是……是我表哥下的毒手？他……他为什么这般狠心？」 ###旁白:慕容复想"段誉这小子在少室山上打得我面目无光，令我从此在江湖上声威扫地，他要死便死他的，我何必出手相救？何况这凶僧武功极强，我远非其敌，且让他二人斗个两败俱伤，最好是同归于尽。我此刻插手，殊为不智。" 王语嫣:「表哥，表哥，你快来帮手，这和尚……这和尚要扼死段公子啦！」 ###女子:「你听，吐番武士用大石压住了井口，咱们却如何出去？」 王语嫣:「只须得能和你厮守，不能出去，又有何妨？你既在我身旁，臭泥井便是众香国。东方琉璃世界，西方极乐世界，甚么兜率天、夜摩天的天堂乐土，也及不上此地了。」 ###段誉:「我徒儿是个恶人，这瘦长条子人品更坏，不用帮他。」 王语嫣:「嗯！不过丐帮众人将你把兄赶走，不让他做帮主，以冤枉我表哥，我讨厌他们。」 ###阿朱:「姑娘，这儿离婢子的下处较近，今晚委出你暂住一宵，再商量怎生去寻公子，好不好？」 王语嫣:「嗯，就是这样。」 旁白:段誉想"原来是无量剑宗的。" 阿碧:「那边有灯火处，就是阿朱姊姊的听香水榭。」 旁白:段誉想"此生此世，只怕再无今晚之情，如此湖上泛舟，若能永远到不了灯火处，岂不是好？" 王语嫣:「段誉却没听得清楚。」 ###阿朱:「王姑娘，我想假扮乔帮主混进寺中，将那个臭瓶丢给众叫化闻闻。他们脱险之后，必定好生感激乔帮主。」 王语嫣:「乔帮主身材高大，是个魁梧奇伟的汉子，你怎扮得他像？」 阿朱:「越是艰难，越显得阿朱的手段。」 王语嫣:「你扮得像乔帮主，却冒充不了他的绝世神功。天宁寺中尽是西夏一品堂的高手人物，你如何能来去自如？依我说呢，扮作一个火工道人、或是一个乡下的卖菜婆婆，那还容易混进去些。」 ###汉人:「臭小子，你鬼鬼祟祟的干什么？」'
    # message,_ = generate_text(his,text)
    response, history = model.chat(tokenizer, text, history=[])
    print(response)