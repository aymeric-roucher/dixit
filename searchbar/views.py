from django.shortcuts import render
import numpy as np
import os
import pickle
from django.views.decorators.csrf import csrf_protect
from sentence_transformers.util import semantic_search
import faiss
from scripts import open_sql_connection

conn = open_sql_connection()
cursor = conn.cursor()

files = [f for f in os.listdir(".") if os.path.isfile(f)]

model = pickle.load(open("model.pickle", "rb"))

sql_authors = '''select name from authors;'''
cursor.execute(sql_authors)
authors_unique = [tuple[0] for tuple in cursor.fetchall()]
faiss_index = faiss.read_index('index_alone.faiss')

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
    _, samples = faiss_index.search(
        sentence_embedding, k=k
    )
    sql3 = f'''
    SELECT quotes_result.index, quotes_result.quote, authors.name, authors.description \
    FROM (SELECT * FROM quotes WHERE index in {tuple(samples[0])}) as quotes_result\
    LEFT JOIN authors \
    ON quotes_result.author = authors.name;'''
    cursor.execute(sql3)
    samples = cursor.fetchall()
    return samples


# our result page view
@csrf_protect
def show_searchbar(request):
    required_data = []
    sentence = ""
    if request.method == "POST":
        sentence = request.POST["sentence"]
        results = get_quote(sentence)
        for i in range(len(results)):
            quote_dict = {
                "quote": results[i][1],
                "author": results[i][2],
                "author_description": results[i][3],
                "id": results[i][0],
            }
            required_data.append(quote_dict)

    return render(
        request,
        "searchbar/index.html",
        {"quotes": required_data, "sentence": sentence, "authors_list": authors_unique},
    )
