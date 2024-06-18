import tensorflow as tf
import tensorflow_io as tfio
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import load_model, Model

from google.cloud import storage

models = {}
dataframes = {}

def init():
    storage_client = storage.Client()

    bucket = storage_client.bucket("travellabel_ml_models")
    blob = bucket.blob("recsys_collaborative/collaborative_model.h5")
    blob.download_to_filename("collaborative_model.h5")

    models['recsys_collab'] = load_model("collaborative_model.h5")

    blob = bucket.blob("recsys_collaborative/tempat_wisata.csv")
    blob.download_to_filename("tempat_wisata.csv")
    dataframes['recsys_collab'] = pd.read_csv("tempat_wisata.csv")

def _collab_get_place_frame(place):
    df = dataframes['recsys_collab']
    if isinstance(place, int):
        return df[df.place == place]
    if isinstance(place, str):
        return df[df.place_name == place]

def _collab_extract_weights(name, model):
    weight_layer = model.get_layer(name)
    weights = weight_layer.get_weights()[0]
    weights = weights / np.linalg.norm(weights, axis=1).reshape((-1, 1))
    return weights

def collab_recommend(place_name, n=10, neg=False):
    df = dataframes['recsys_collab']

    place = df['place_name'].unique().tolist()
    place2place_encoded = {x: i for i, x in enumerate(place)}
    place_encoded2place = {i: x for i, x in enumerate(place)}
    df["place"] = df["place_name"].map(place2place_encoded)

    model: Model = models['recsys_collab']
    place_weights = _collab_extract_weights('place_embedding', model)

    place_frame = _collab_get_place_frame(place_name)
    if place_frame.empty:
        raise LookupError(f"Place {place_name} not registered in collab_recommend")

    index = place_frame.place.values[0]

    encoded_index = place2place_encoded.get(place_name)

    dists = np.dot(place_weights, place_weights[encoded_index])
    sorted_dists = np.argsort(dists)

    n = n + 1

    if neg:
        closest = sorted_dists[:n]
    else:
        closest = sorted_dists[-n:]

    sim = []

    for close in closest:
        decoded_id = place_encoded2place.get(close)
        place_frame = _collab_get_place_frame(decoded_id)
        place_name = place_frame.place_name.values[0]

        similarity = dists[close]
        sim.append({"place_id": decoded_id, "name": place_name, "similarity": similarity})

    res = pd.DataFrame(sim).sort_values(by="similarity", ascending=False)
    return res[res.place_id != index]['name'].tolist()

# tester
if __name__ == "__main__":
    print(collab_recommend("Gunung Semeru", n=15, neg=False))
