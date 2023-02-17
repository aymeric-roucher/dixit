from django.shortcuts import render
import requests
import pandas as pd

quote_base = pd.read_csv('quotes_clean.csv', sep='|')

def index(request):
    return render(request, 'author/index.html', {'author': "OKOK"})


def author_summary(request, author_name):
    author_request = requests.get(f'https://en.wikipedia.org/api/rest_v1/page/summary/{author_name.replace(" ", "_")}').json()
    if author_request['title'] == "Not found.":
        author_summary = 'Author not found in Wikipedia.'
        other_by_author = []
    else:
        author_summary = author_request['extract_html']
        picture_link = author_request['thumbnail']['source']
        other_by_author = list(quote_base.loc[quote_base['author'] == author_name, 'quote'].values[:10])
    return render(request, 'author/index.html', {'author_name': author_name, 'author_summary': author_summary, 'other_by_author':other_by_author, 'picture_link':picture_link})
