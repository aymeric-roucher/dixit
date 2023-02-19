from django.shortcuts import render
import requests
import pandas as pd

quote_base = pd.read_csv('quotes_classical_clean.csv', sep='|')

def index(request):
    return render(request, 'author/index.html')


def author_summary(request, author_name):
    author_request = requests.get(f'https://en.wikipedia.org/api/rest_v1/page/summary/{author_name.replace(" ", "_")}').json()
    if author_request['title'] == "Not found.":
        author_data = {
            'author_name': author_name,
            'found': False, 'author_summary': None, 'picture_link': None,
            'other_by_author': list(quote_base.sample(n=10)['quote'].values),
        }
    else:
        author_data = {
            'author_name': author_name,
            'found': True,
            'author_summary': author_request['extract_html'],
            'picture_link': (author_request['thumbnail']['source'] if 'thumbnail' in author_request.keys() else ''),
            'other_by_author': list(quote_base.loc[quote_base['author'] == author_name, 'quote'].values[:100]),
        }
    return render(request, 'author/index.html', author_data)
