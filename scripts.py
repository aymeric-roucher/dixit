import json
import psycopg2
import os
from datasets import load_from_disk
import pickle
import numpy as np
import pandas as pd

from sentence_transformers.util import semantic_search

def open_sql_connection():
    password_railway = os.getenv('PGPASSWORD')
    conn = psycopg2.connect(
        database="railway",
        user="postgres",
        password=password_railway,
        host="containers-us-west-127.railway.app",
        port="5800",
    )
    conn.autocommit = True
    return conn

SQL_CURSOR = open_sql_connection().cursor()
sql_authors = '''select name from authors;'''
SQL_CURSOR.execute(sql_authors)
AUTHORS_LIST = [tuple[0] for tuple in SQL_CURSOR.fetchall()]

QUOTES_DATASET = load_from_disk('./export_dataset')
QUOTES_DATASET = QUOTES_DATASET.add_faiss_index(column="embedding")
QUOTES_DATASET = QUOTES_DATASET.remove_columns('embedding')

model = pickle.load(open("model.pickle", "rb"))

def get_authors_descriptions(author_list: list) -> pd.DataFrame:
    sql = '''
    SELECT name, description \
    FROM authors WHERE authors.name in %(author_names)s;'''
    SQL_CURSOR.execute(sql, dict(author_names=tuple(author_list)))
    author_descriptions = SQL_CURSOR.fetchall()
    return pd.DataFrame({
        "author": [desc[0] for desc in author_descriptions],
        "author_description": [desc[1] for desc in author_descriptions]
    })

def search_closest_quotes(sentence: str, k: int=15) -> pd.DataFrame:
    sentence_embedding = model.encode([sentence])
    scores, samples = QUOTES_DATASET.get_nearest_examples(
        'embedding', sentence_embedding, k=k
    )
    author_descriptions_df = get_authors_descriptions(np.unique(samples['author']))
    quotes = pd.DataFrame.from_dict(samples)
    quotes = quotes.merge(author_descriptions_df, on='author')
    quotes["scores"] = scores
    quotes = quotes.sort_values("scores", ascending=True) # lower is better
    return quotes

def get_quotes_from_author(author_name:str):
    indexes_author = [i for i, el in enumerate(QUOTES_DATASET['author']) if el == author_name]
    print("IX AUTHOR", indexes_author)
    return [QUOTES_DATASET['quote'][i] for i in indexes_author]

def get_author_description(author_name:str):
    sql = "SELECT description, extract_html, thumbnail_url FROM authors WHERE name = %(author_name)s;"
    SQL_CURSOR.execute(sql, {"author_name": author_name})
    return SQL_CURSOR.fetchone()