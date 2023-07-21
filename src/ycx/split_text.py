import os


output_folder = 'liyunlong_file_output'
for file in os.listdir('liyunlong_file'):
    with open(os.path.join('liyunlong_file', file), encoding='utf-8') as f:
        data = f.read()
        for i, dialogue in enumerate(data.split('--')):
            with open(os.path.join(output_folder, f"{file[:-4]}_{i}.txt"), 'w+', encoding='utf-8') as fw:
                fw.write(dialogue.strip())
