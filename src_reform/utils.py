from argparse import Namespace
from transformers import AutoModel, AutoTokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def download_models():
    print("正在下载Luotuo-Bert")
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                            init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args).to(device)
    print("Luotuo-Bert下载完毕")
    return model


def get_embedding(model, texts):
    tokenizer = AutoTokenizer.from_pretrained("silk-road/luotuo-bert")
    # str or strList
    texts = texts if isinstance(texts, list) else [texts]
    # 截断
    for i in range(len(texts)):
        if len(texts[i]) > 510:
            texts[i] = texts[i][:510]
    # Tokenize the texts
    inputs = tokenizer(texts, padding=True, truncation=False, return_tensors="pt")
    inputs = inputs.to(device)
    # Extract the embeddings
    # Get the embeddings
    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True, sent_emb=True).pooler_output
    return embeddings[0] if len(texts) == 1 else embeddings