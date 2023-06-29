import gradio as gr
from app import ChatPerson
from text import Text

def create_gradio(chat_person):
    # from google.colab import drive
    # drive.mount(drive_path)
    with gr.Blocks() as demo:
        gr.Markdown(
            """
            ## Chat凉宫春日 ChatHaruhi
            此版本为测试版本，非正式版本，正式版本功能更多，敬请期待
            """
        )
        image_input = gr.Textbox(visible=False)
        japanese_input = gr.Textbox(visible=False)
        with gr.Row():
            chatbot = gr.Chatbot()
            image_output = gr.Image()
        audio = gr.Audio(visible=False)
        role_name = gr.Textbox(label="角色名", placeholde="输入角色名")
        msg = gr.Textbox(label="输入")
        with gr.Row():
            clear = gr.Button("Clear")
            image_button = gr.Button("给我一个图")
            audio_btn = gr.Button("春日和我说")
        # japanese_output = gr.Textbox(interactive=False, visible=False)
        sub = gr.Button("Submit")
        # audio_store = gr.Textbox(interactive=False)
        
        
        # def update_audio(audio, japanese_output):
        #     japanese_output = japanese_output.split("春日:")[1]
        #     jp_audio_store = vits_haruhi.vits_haruhi(japanese_output, 4)
        #     return gr.update(value=jp_audio_store, visible=True)
        

        def respond(role_name, user_message, chat_history):
            input_message = role_name + ':「' + user_message + '」'
            bot_message = chat_person.getResponse(input_message, chat_history)
            chat_history.append((input_message, bot_message))
            # self.save_response(chat_history)
            # time.sleep(1)
            # jp_text = pipe(f'<-zh2ja-> {bot_message}')[0]['translation_text']
            # jp_audio_store = vits_haruhi.vits_haruhi(bot_message, 6)
            # return "" , chat_history, bot_message, jp_text
            return "" , chat_history, bot_message


        
        

        clear.click(lambda: None, None, chatbot, queue=False)
        # msg.submit(respond, [role_name, msg, chatbot], [msg, chatbot, image_input, japanese_output])
        msg.submit(respond, [role_name, msg, chatbot], [msg, chatbot, image_input])
        # sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input, japanese_output])
        sub.click(fn=respond, inputs=[role_name, msg, chatbot], outputs=[msg, chatbot, image_input])
        # audio_btn.click(fn=update_audio, inputs=[audio, japanese_output], outputs=audio)

        # image_button.click(text.text_to_image, inputs=image_input, outputs=image_output)

    demo.launch(debug=True,share=True)

chat_person = ChatPerson()
create_gradio(chat_person)