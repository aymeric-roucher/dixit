from django.shortcuts import render


def index(request):
    return render(request, 'author/index.html', {'author': "OKOK"})


def author_summary(request, author_name):
    return render(request, 'author/index.html', {'author_name': author_name})
