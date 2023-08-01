from argparse import Namespace
from transformers import AutoModel, AutoTokenizer
import torch
import jsonlines
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def download_models():
    print("正在下载Luotuo-Bert")
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                           init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert-medium", trust_remote_code=True, model_args=model_args).to(
        device)
    print("Luotuo-Bert下载完毕")
    return model


def get_embedding(model, texts):
    model = model.to(device)
    tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert-medium")
    # str or strList
    texts = texts if isinstance(texts, list) else [texts]
    # 截断
    for i in range(len(texts)):
        if len(texts[i]) > 510:
            texts[i] = texts[i][:510]
    # Tokenize the texts_source
    inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
    inputs = inputs.to(device)
    # Extract the embeddings
    # Get the embeddings
    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
    return embeddings


def merge_jsonl_files(folder_path, output_file):
    with jsonlines.open(output_file, mode='w') as writer:
        for filename in os.listdir(folder_path):
            if filename.endswith('.jsonl'):
                file_path = os.path.join(folder_path, filename)
                with jsonlines.open(file_path) as reader:
                    for item in reader:
                        writer.write(item)

model = download_models()