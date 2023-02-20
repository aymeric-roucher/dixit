from django.shortcuts import render
import requests
import pandas as pd
from django.views.decorators.csrf import csrf_protect

quote_base = pd.read_csv("quotes_classical_clean.csv", sep="|")


def no_author(request):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        print("BASE AUTHOR NAME", author_name)
        return author_summary(request, author_name)
    return render(request, "author/index.html")


@csrf_protect
def author_summary(request, author_name):
    try:
        author_request = requests.get(
            f'https://en.wikipedia.org/api/rest_v1/page/summary/{author_name.replace(" ", "_")}',
            timeout=1,
        ).json()
    except:
        author_request = None
    if author_request is None or author_request["title"] == "Not found.":
        author_data = {
            "author_name": author_name,
            "found": False,
            "author_summary": None,
            "picture_link": None,
            "other_by_author": list(
                quote_base.loc[quote_base["author"] == author_name, "quote"].values[
                    :100
                ]
            ),
        }
    else:
        author_data = {
            "author_name": author_name,
            "found": True,
            "author_summary": author_request["extract_html"],
            "picture_link": (
                author_request["thumbnail"]["source"]
                if "thumbnail" in author_request.keys()
                else ""
            ),
            "other_by_author": list(
                quote_base.loc[quote_base["author"] == author_name, "quote"].values[
                    :100
                ]
            ),
        }
    return render(request, "author/index.html", author_data)
