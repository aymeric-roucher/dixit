from django.shortcuts import render
import requests
import pandas as pd
from django.views.decorators.csrf import csrf_protect
from scripts import open_sql_connection

conn = open_sql_connection()
cursor = conn.cursor()


def no_author(request):
    if request.method == "POST":
        author_name = request.POST["author_name"]
        return author_summary(request, author_name)
    return render(request, "author/index.html")


@csrf_protect
def author_summary(request, author_name):
    sql = "SELECT quote FROM quotes WHERE author = %(author_name)s;"
    cursor.execute(sql, {"author_name": author_name})
    author_quotes = [row[0] for row in cursor.fetchall()]
    author_data = {
        "author_name": author_name,
        "found": False,
        "author_summary": None,
        "picture_link": None,
        "other_by_author": author_quotes,
    }
    sql = "SELECT description, extract_html, thumbnail_url FROM authors WHERE name = %(author_name)s;"
    cursor.execute(sql, {"author_name": author_name})
    author_row = cursor.fetchone()
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
