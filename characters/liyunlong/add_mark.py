import os


def add_mark(folder):
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f1, open('texts2/'+file, 'w+', encoding='utf-8') as f2:
            for line in f1.readlines():
                print(line)
                line = line.replace('：', ':「')
                if '\n' not in line:
                    line = line + ('」')
                else:
                    line = line.replace('\n', '」')
                print(line)
                f2.write(line)
                f2.write('\n')

add_mark('texts')
# for i in range(1, 15):
#     with open(f'texts/{i}.txt', 'w+') as f:
#         print(1)
