import zipfile
import gradio as gr
from PIL import Image
from chatharuhi import ChatHaruhi
import wget
import os
import openai
import copy



NAME_DICT = {'汤师爷': 'tangshiye', '慕容复': 'murongfu', '李云龙': 'liyunlong', 'Luna': 'Luna', '王多鱼': 'wangduoyu',
             'Ron': 'Ron', '鸠摩智': 'jiumozhi', 'Snape': 'Snape',
             '凉宫春日': 'haruhi', 'Malfoy': 'Malfoy', '虚竹': 'xuzhu', '萧峰': 'xiaofeng', '段誉': 'duanyu',
             'Hermione': 'Hermione', 'Dumbledore': 'Dumbledore', '王语嫣': 'wangyuyan',
             'Harry': 'Harry', 'McGonagall': 'McGonagall', '白展堂': 'baizhantang', '佟湘玉': 'tongxiangyu',
             '郭芙蓉': 'guofurong', '旅行者': 'wanderer', '钟离': 'zhongli',
             '胡桃': 'hutao', 'Sheldon': 'Sheldon', 'Raj': 'Raj', 'Penny': 'Penny', '韦小宝': 'weixiaobao',
             '乔峰': 'qiaofeng', '神里绫华': 'ayaka', '雷电将军': 'raidenShogun', '于谦': 'yuqian'}

try:
    os.makedirs("characters_zip")
except:
    pass
try:
    os.makedirs("characters")
except:
    pass
ai_roles_obj = {}
for ai_role_en in NAME_DICT.values():
    file_url = f"https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/character_in_zip/{ai_role_en}.zip"
    try:
        os.makedirs(f"characters/{ai_role_en}")
    except:
        pass
    if f"{ai_role_en}.zip" not in os.listdir(f"characters_zip"):
        destination_file = f"characters_zip/{ai_role_en}.zip"
        wget.download(file_url, destination_file)
        destination_folder = f"characters/{ai_role_en}"
        with zipfile.ZipFile(destination_file, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
    db_folder = f"./characters/{ai_role_en}/content/{ai_role_en}"
    system_prompt = f"./characters/{ai_role_en}/content/system_prompt.txt"
    ai_roles_obj[ai_role_en] = ChatHaruhi(system_prompt=system_prompt,
                                          llm="openai",
                                          story_db=db_folder,
                                          verbose=True)


async def get_response(user_role, user_text, ai_role, chatbot):
    role_en = NAME_DICT[ai_role]
    ai_roles_obj[role_en].dialogue_history = copy.deepcopy(chatbot)
    response = ai_roles_obj[role_en].chat(role=user_role, text=user_text)
    user_msg = user_role + ':「' + user_text + '」'
    chatbot.append((user_msg, response))
    return chatbot


async def respond(user_role, user_text, ai_role, chatbot):
    return await get_response(user_role, user_text, ai_role, chatbot), None


def clear(user_role, user_text, chatbot):
    return None, None, []


def get_image(ai_role):
    role_en = NAME_DICT[ai_role]
    return Image.open(f'images/{role_en}.jpg'), None, None, []


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Chat凉宫春日 ChatHaruhi
        ## Reviving Anime Character in Reality via Large Language Model

        ChatHaruhi2.0的demo implemented by [chenxi](https://github.com/todochenxi)

        更多信息见项目github链接 [https://github.com/LC1332/Chat-Haruhi-Suzumiya](https://github.com/LC1332/Chat-Haruhi-Suzumiya)

        如果觉得有趣请拜托为我们点上star. If you find it interesting, please be kind enough to give us a star.

        user_role 为角色扮演的人物 请尽量设置为与剧情相关的人物 且不要与主角同名
        """
    )
    with gr.Row():
        chatbot = gr.Chatbot()
        role_image = gr.Image(height=400, value="./images/haruhi.jpg")
    with gr.Row():
        user_role = gr.Textbox(label="user_role")
        user_text = gr.Textbox(label="user_text")
    with gr.Row():
        submit = gr.Button("Submit")
        clean = gr.ClearButton(value="Clear")
    ai_role = gr.Radio(['汤师爷', '慕容复', '李云龙',
                        'Luna', '王多鱼', 'Ron', '鸠摩智',
                        'Snape', '凉宫春日', 'Malfoy', '虚竹',
                        '萧峰', '段誉', 'Hermione', 'Dumbledore',
                        '王语嫣',
                        'Harry', 'McGonagall',
                        '白展堂', '佟湘玉', '郭芙蓉',
                        '旅行者', '钟离', '胡桃',
                        'Sheldon', 'Raj', 'Penny',
                        '韦小宝', '乔峰', '神里绫华',
                        '雷电将军', '于谦'], label="characters", value='凉宫春日')
    ai_role.change(get_image, ai_role, [role_image, user_role, user_text, chatbot])
    user_text.submit(fn=respond, inputs=[user_role, user_text, ai_role, chatbot], outputs=[chatbot, user_text])
    submit.click(fn=respond, inputs=[user_role, user_text, ai_role, chatbot], outputs=[chatbot, user_text])
    clean.click(clear, [user_role, user_text, chatbot], [user_role, user_text, chatbot])
demo.launch(debug=True, share=True)
