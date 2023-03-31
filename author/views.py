from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from scripts import get_quotes_from_author, get_author_extract, get_similar_authors


def no_author(request):
    if request.method == "POST":
        name = request.POST["name"]
        return author_summary(request, name)
    return render(request, "author/index.html")

def search_author(request):
    name = request.GET.get('name', '').strip()
    if name:
        return redirect('author', name=name)
    else:
        return redirect('searchbar')


@csrf_protect
def author_summary(request, name):
    name = name.replace('_', ' ')
    author_quotes = get_quotes_from_author(name)
    suggested_authors = get_similar_authors(name)
    author_data = {
        "name": name,
        "found": False,
        "author_summary": None,
        "picture_link": None,
        "other_by_author": author_quotes,
        "suggested_authors": suggested_authors,
    }

    author_row = get_author_extract(name)
    if author_row is None:
        return render(request, "author/index.html", author_data)

    _, extract_html, thumbnail_url = author_row
    author_data.update(
        {
            "found": True,
            "author_summary": extract_html,
            "picture_link": thumbnail_url,
        }
    )
    return render(request, "author/index.html", author_data)
