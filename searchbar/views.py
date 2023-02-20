from django.shortcuts import render
import numpy as np
import os
import pickle
from django.views.decorators.csrf import csrf_protect
from sentence_transformers.util import semantic_search

files = [f for f in os.listdir(".") if os.path.isfile(f)]

model = pickle.load(open("model.pickle", "rb"))
embeddings_dataset = pickle.load(open("embeddings_dataset.pickle", "rb"))
authors_unique = np.unique(embeddings_dataset["author"])


def index(request):
    return render(request, "searchbar/index.html")


def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]


def get_embeddings(text_list, tokenizer, model):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_input = {k: v.to("cpu") for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)


def get_quote(sentence, k=30):
    sentence_embedding = model.encode([sentence])
    scores, samples = embeddings_dataset.get_nearest_examples(
        "embeddings", sentence_embedding, k=k
    )
    return samples


# our result page view
@csrf_protect
def show_searchbar(request):
    required_data = []
    sentence = ""
    selected_author = None
    if request.method == "POST":
        sentence = request.POST["sentence"]
        # selected_author = request.POST["selected_author"]
        results = get_quote(sentence)
        for i in range(len(list(results.values())[0])):
            quote_dict = {
                "quote": results["quote"][i],
                "author": results["author"][i],
                "category": results["category"][i],
                "id": i,
            }
            required_data.append(quote_dict)

    return render(
        request,
        "searchbar/index.html",
        {"quotes": required_data, "sentence": sentence, "authors_list": authors_unique},
    )
