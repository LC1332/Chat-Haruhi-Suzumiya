import os


def split_text(input_folder, output_folder):
    for file in os.listdir(input_folder):
        with open(os.path.join(input_folder, file), encoding='utf-8') as f:
            data = f.read()
            for i, dialogue in enumerate(data.split('\n\n')):
                with open(os.path.join(output_folder, f"{file[:-4]}_{i}.txt"), 'w+', encoding='utf-8') as fw:
                    fw.write(dialogue.strip())


split_text('yuqian', 'yuqian_output')
