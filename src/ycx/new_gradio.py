from zipfile import ZipFile

import gradio as gr


def update_audio(audio, japanese_output):
    # japanese_output = japanese_output.split("春日:")[1]
    # jp_audio_store = vits_haruhi.vits_haruhi(japanese_output, 4)
    # return gr.update(value=jp_audio_store, visible=True)
    return 1


def respond(role_name, user_message, chat_history):
    # input_message = role_name + ':「' + user_message + '」'
    # bot_message = self.get_response(input_message, chat_history)
    # chat_history.append((input_message, bot_message))
    # self.save_response(chat_history)
    # # time.sleep(1)
    # jp_text = pipe(f'<-zh2ja-> {bot_message}')[0]['translation_text']
    # # jp_audio_store = vits_haruhi.vits_haruhi(bot_message, 6)
    # return "", chat_history, bot_message, jp_text
    return 1


def upload_file(file_obj):
    # 上传文件
    filenames = []
    with ZipFile(file_obj.name) as zfile:
        zfile.extractall('./texts_source')
    for filename in zfile.namelist():
        filenames.append(filename.encode('cp437').decode('gbk'))
    print(filenames)


def generate(file):
    return {gen: gr.update(visible=False),
            chat: gr.update(visible=True)}


with gr.Blocks() as demo:
    gr.Markdown(
        """
        ## Chat凉宫春日 ChatHaruhi
        此版本为测试版本，非正式版本，正式版本功能更多，敬请期待
        """
    )
    with gr.Tab("Chat"):
        api_key = gr.Textbox(label="输入key", value="sr-xxxxxxxx")
        character = gr.Radio(["凉宫春日", " 灼眼的夏娜", "李云龙"])
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
            audio_btn = gr.Button("春日和我说")
        japanese_output = gr.Textbox(interactive=False, visible=False)
        sub = gr.Button("Submit")

        # audio_store = gr.Textbox(interactive=False)

        clear.click(lambda: None, None, None, chatbot, queue=False)
        msg.submit(respond, [api_key, role_name, msg, chatbot], [msg, chatbot, image_input, japanese_output])
        sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input, japanese_output])
        audio_btn.click(fn=update_audio, inputs=[audio, japanese_output], outputs=audio)
    with gr.Tab("Custom Character"):
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
                        texts = gr.File(label="Upload Texts")
                        images = gr.File(label="Upload Images")
                rule = gr.Textbox(label="文件格式", lines=10)
                rule.value = format_rule
            generate_btn = gr.Button("生成")

        with gr.Column(visible=False) as chat:
            custom_api_key = gr.Textbox(label="输入key", value="sr-xxxxxxxx")
            image_input = gr.Textbox(visible=False)
            japanese_input = gr.Textbox(visible=False)
            with gr.Row():
                custom_chatbot = gr.Chatbot()
                custom_image_output = gr.Image()
            custom_audio = gr.Audio(visible=False)
            custom_role_name = gr.Textbox(label="角色名")
            custom_msg = gr.Textbox(label="输入")
            with gr.Row():
                custom_clear = gr.Button("Clear")
                custom_image_button = gr.Button("给我一个图")
                custom_audio_btn = gr.Button("春日和我说")
            custom_japanese_output = gr.Textbox(interactive=False)
            custom_sub = gr.Button("Submit")

        # audio_store = gr.Textbox(interactive=False)

        custom_clear.click(lambda: None, None, None, chatbot, queue=False)
        custom_msg.submit(respond, [api_key, role_name, msg, chatbot], [msg, chatbot, image_input, japanese_output])
        custom_sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input, japanese_output])
        custom_audio_btn.click(fn=update_audio, inputs=[audio, japanese_output], outputs=audio)
        generate_btn.click(generate, role_name, [gen, chat])

demo.launch(debug=True, share=True)
