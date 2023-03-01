from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_protect
from scripts import search_closest_quotes, AUTHORS_LIST


def index(request):
    return render(request, "searchbar/index.html")


@csrf_protect
def show_searchbar(request):
    required_data = []
    sentence = ""
    if request.method == "POST":
        sentence = request.POST["sentence"]
        results = search_closest_quotes(sentence)
        for i, row in results.iterrows():
            quote_dict = {
                "quote": row["quote"],
                "author": row["author"],
                "author_description": row["author_description"],
            }
            required_data.append(quote_dict)

    return render(
        request,
        "searchbar/index.html",
        {"quotes": required_data, "sentence": sentence, "authors_list": AUTHORS_LIST},
    )
