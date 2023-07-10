from argparse import Namespace

from nomic import atlas
import numpy as np
from transformers import AutoModel

import text

num_embeddings = 10000


def download_models():
    # Import our models. The package will take care of downloading the models automatically
    model_args = Namespace(do_mlm=None, pooler_type="cls", temp=0.05, mlp_only_train=False,
                           init_embeddings_model=None)
    model = AutoModel.from_pretrained("silk-road/luotuo-bert", trust_remote_code=True, model_args=model_args)
    return model


pkl_path = './pkl/texts.pkl'
maps_path = './pkl/maps.pkl'
dict_path = "../characters/haruhi/text_image_dict.txt"
image_path = "../characters/haruhi/images"
model = download_models()
text = text.Text("../characters/haruhi/texts", model=model, num_steps=50, pkl_path=pkl_path, dict_path=dict_path,
                 image_path=image_path, maps_path=maps_path)
# text.read_text(save_maps=True, save_embeddings=True)
embeddings = np.array([i.numpy() for i in list(text.load(load_pkl=True).values())])
data = text.load(load_maps=True)
project = atlas.map_embeddings(embeddings=embeddings,
                               data=data,
                               build_topic_model=True,
                               topic_label_field="titles",
                               id_field='id',
                               name="Chat-Haruhi",
                               colorable_fields=['titles'],
                               description="Embedding Visualization",
                               # reset_project_if_exists=True,
                               )
