
from django.shortcuts import render
import pandas as pd
import os
import pickle

files = [f for f in os.listdir('.') if os.path.isfile(f)]

model = pickle.load(open("model.pickle", "rb"))
embeddings_dataset = pickle.load(open("embeddings_dataset.pickle", "rb"))

# our home page view
def home(request):    
    return result(request)

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

def get_embeddings(text_list, tokenizer, model):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="pt"
    )
    encoded_input = {k: v.to('cpu') for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    return cls_pooling(model_output)


# custom method for generating predictions
def get_quote(sentence):

    sentence_embedding = model.encode([sentence])
    scores, samples = embeddings_dataset.get_nearest_examples(
        "embeddings", sentence_embedding, k=10
    )
    return scores, samples


# our result page view
def result(request):
    required_data = []
    if request.method == "POST":
        if request.POST['sentence'] == '':
            messages.error(request, 'Please type something.')
        else:
            sentence = request.POST['sentence']
            scores, results = get_quote(sentence)
            results = pd.DataFrame.from_dict(results)
            
            for i, quote in results.iterrows():
                quote_dict = {
                    "quote": quote['quote'],
                    "author": quote['author'],
                    "category": quote['category'],
                    'id': i,
                }            
                required_data.append(quote_dict)

    return render(request, 'index.html', {'quotes':required_data})
