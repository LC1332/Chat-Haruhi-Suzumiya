import hashlib
import json
import os
import shutil
from zipfile import ZipFile
from store_data import StoreData
import gradio as gr
from app import ChatPerson
import configparser


def create_gradio(chat_person):
    # from google.colab import drive
    # drive.mount(drive_path)
    def generate_user_id(ip_address):
        hash_object = hashlib.sha256(ip_address.encode())
        return hash_object.hexdigest()

    def save_dialogue(host, messages):
        hash_value = generate_user_id(host)
        dialogue_path = chat_person.ChatGPT.dialogue_path
        path = os.path.join(dialogue_path, f"{hash_value}.jsonl")
        if os.path.exists(path):
            f = open(path, 'a', encoding='utf-8')
        else:
            if not os.path.exists(dialogue_path):
                os.makedirs(dialogue_path)
            f = open(path, 'w+', encoding='utf-8')
        for msg in messages:
            # "阿虚:「你好」" -->  {"role": "阿虚", "text": "你好"}
            res = msg.split(':')
            item = {"role": res[0], "text": res[1][1:-1]}
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
        f.close()

    def respond(role_name, user_message, chat_history, request: gr.Request):
        print("history is here : ", chat_history)
        input_message = role_name + ':「' + user_message + '」'
        bot_message = chat_person.getResponse(input_message, chat_history)
        chat_history.append((input_message, bot_message))
        save_dialogue(request.client.host, (input_message, bot_message))
        # self.save_response(chat_history)
        # time.sleep(1)
        # jp_text = pipe(f'<-zh2ja-> {bot_message}')[0]['translation_text']
        # jp_audio_store = vits_haruhi.vits_haruhi(bot_message, 6)
        # return "" , chat_history, bot_message, jp_text
        return "", chat_history, bot_message

    def getImage(query):
        return chat_person.ChatGPT.text_to_image(query)

    def switchCharacter(characterName, chat_history):
        chat_history = []
        chat_person.switchCharacter(characterName)
        # print(chat_person.ChatGPT.image_path)
        return chat_history, None

    def check_path(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def upload_file(role_name, file_obj):
        character_path = f"../characters/{role_name}"
        check_path(character_path)
        check_path(os.path.join(character_path, "texts"))
        check_path(os.path.join(character_path, "images"))
        check_path(os.path.join(character_path, "jsonl"))
        check_path(os.path.join(character_path, "dialogues"))

        with ZipFile(file_obj.name) as zfile:
            if file_obj.label == '上传台本':
                zfile.extractall(os.path.join(character_path, "texts"))
            else:
                images_path = os.path.join(character_path, "images")
                zfile.extractall(images_path)
                filenames = []
                for filename in zfile.namelist():
                    filenames.append(filename.encode('cp437').decode('gbk'))
                files = os.listdir(os.listdir(images_path))
                for i, file_name in enumerate(files):
                    if file_name.endwith(('.jpg', '.jpeg',
                                          '.png')):
                        new_file_name = filenames[i]
                        new_file_path = os.path.join(images_path, new_file_name)

                        # 构造旧的文件路径
                        old_file_path = os.path.join(images_path, file_name)

                        # 使用shutils模块重命名文件
                        shutil.move(old_file_path, new_file_path)

    def generate_prompt(role_name, prompt):
        character_path = f"../characters/{role_name}"
        check_path(character_path)
        with open(os.path.join(character_path, 'system_prompt.txt'), 'w+', encoding='utf-8') as f:
            f.write(prompt)

    def generate_character(role_name):
        # 在config.ini中加添角色信息
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read('config.ini', encoding='utf-8')

        # 添加新的配置项
        config.add_section(role_name)
        config[role_name]['character_folder'] = f"../characters/{role_name}"
        config[role_name]['image_embed_jsonl_path'] = f"../characters/{role_name}/jsonl/image_embed.jsonl"
        config[role_name]['title_text_embed_jsonl_path'] = f"../characters/{role_name}/jsonl/title_text_embed.jsonl"
        config[role_name]['images_folder'] = f"../characters/{role_name}/images"
        config[role_name]['texts_folder'] = f"../characters/{role_name}/texts"
        config[role_name]['system_prompt'] = f"../characters/{role_name}/system_prompt.txt"
        config[role_name]['dialogue_path'] = f"../characters/{role_name}/dialogues/"
        config[role_name]['max_len_story'] = 1500
        config[role_name]['max_len_history'] = 1200
        config[role_name]['gpt'] = True
        config[role_name]['local_tokenizer'] = "THUDM/chatglm2-6b"
        config[role_name]['local_model'] = "THUDM/chatglm2-6b"
        config[role_name]['local_lora'] = "Jyshen/Chat_Suzumiya_GLM2LoRA"

        # 保存修改后的配置文件
        with open('config.ini', 'w', encoding='utf-8') as config_file:
            config.write(config_file)

        configuration = {
            "image_embed_jsonl_path": config[role_name]['image_embed_jsonl_path'],
            "title_text_embed_jsonl_path": config[role_name]['title_text_embed_jsonl_path'],
            "images_folder": config[role_name]['images_folder'],
            "texts_folder": config[role_name]['texts_folder']
        }
        # 存储成jsonl格式
        run = StoreData(configuration)
        run.preload()

        # radio添加新的角色

    with gr.Blocks() as demo:
        gr.Markdown(
            """
            ## Chat凉宫春日 ChatHaruhi
            项目地址 [https://github.com/LC1332/Chat-Haruhi-Suzumiya](https://github.com/LC1332/Chat-Haruhi-Suzumiya)
            - 骆驼项目地址 [https://github.com/LC1332/Luotuo-Chinese-LLM](https://github.com/LC1332/Luotuo-Chinese-LLM) 
            - 此版本为图文版本，完整功能（+语音）的demo见项目 角色名建议输入 阿虚 或者影视剧中有的人物。或者也可以是新学生或者老师。
            """
        )
        with gr.Column(visible=False) as top:
            format_rule = """
        台本格式：台本文件夹打包成zip
            文件名为剧情内容.txt
            示例：
                fileName: SOS团起名由来.txt
                fileContent:
                    春日:「社团名字我刚刚已经想到了!」
                    阿虚:「……那你说来听听啊!」
                    春日:「SOS团!让世界变得更热闹的凉宫春日团，简称SOS团。」         
        图片格式：图片文件夹打包成zip
            图片名即为与该图片相似的文本  如 SOS团.jpg"""
            with gr.Column() as gen:
                with gr.Row():
                    with gr.Column():
                        # role_name
                        role_name = gr.Textbox(label="role_name")
                        with gr.Row():
                            texts = gr.File(label="上传台本")
                            images = gr.File(label="上传图片")
                            prompt = gr.Textbox(label="prompt模板", lines=10, interactive=True)
                    rule = gr.Textbox(label="文件格式", lines=10)
                    rule.value = format_rule
                with gr.Row():
                    texts_btn = gr.Button("上传台本")
                    images_btn = gr.Button("上传图片")
                    prompt_btn = gr.Button("生成prompt")
                    generate_btn = gr.Button("创建角色")

                texts_btn.click(upload_file, [role_name, texts])
                images_btn.click(upload_file, [role_name, images])
                prompt_btn.click(generate_prompt, [role_name, prompt], prompt)
                generate_btn.click(generate_character, role_name)

        with gr.Column() as bottom:
            api_key = gr.Textbox(label="输入key", value="sr-xxxxxxxx")
            character = gr.Radio(["凉宫春日", "李云龙", "于谦", "神里绫华"], label="Character", value='凉宫春日')
            image_input = gr.Textbox(visible=False)
            japanese_input = gr.Textbox(visible=False)
            with gr.Row():
                chatbot = gr.Chatbot()
                image_output = gr.Image()
            audio = gr.Audio(visible=False)
            role_name = gr.Textbox(label="角色名")
            msg = gr.Textbox(label="输入")
            with gr.Row():
                clear = gr.Button("Clear")
                image_button = gr.Button("给我一个图")
                # audio_btn = gr.Button("春日和我说")
            # japanese_output = gr.Textbox(interactive=False, visible=False)
            sub = gr.Button("Submit")
            # audio_store = gr.Textbox(interactive=False)

            # def update_audio(audio, japanese_output):
            #     japanese_output = japanese_output.split("春日:")[1]
            #     jp_audio_store = vits_haruhi.vits_haruhi(japanese_output, 4)
            #     return gr.update(value=jp_audio_store, visible=True)

            character.change(fn=switchCharacter, inputs=[character, chatbot], outputs=[chatbot, image_output])

            clear.click(lambda: None, None, chatbot, queue=False)
            # msg.submit(respond, [role_name, msg, chatbot], [msg, chatbot, image_input, japanese_output])
            msg.submit(respond, [role_name, msg, chatbot], [msg, chatbot, image_input])
            # sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input, japanese_output])
            sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input])
            # audio_btn.click(fn=update_audio, inputs=[audio, japanese_output], outputs=audio)

            image_button.click(getImage, inputs=image_input, outputs=image_output)

    demo.launch(debug=True, share=True)


chat_person = ChatPerson()
create_gradio(chat_person)
