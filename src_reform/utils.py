from argparse import Namespace
from transformers import AutoModel, AutoTokenizer

def download_models():
    print("正在下载Luotuo-Bert")
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                            init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)
    print("Luotuo-Bert下载完毕")
    return model