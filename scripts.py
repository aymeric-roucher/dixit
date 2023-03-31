import psycopg2
import os
import pickle
import pandas as pd
import faiss

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

QUOTES_DATASET = pd.read_csv('data/quotes_export_save_28-02.csv', sep='|')
QUOTES_INDEX = faiss.read_index('data/index_28-02.faiss')

with open("model.pickle", "rb") as pkl:
    model = pickle.load(pkl)

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
    scores, sample_indexes = QUOTES_INDEX.search(
        sentence_embedding, k=k
    )
    quotes = QUOTES_DATASET.iloc[sample_indexes[0]]
    author_descriptions_df = get_authors_descriptions(quotes['author'].unique())
    quotes = quotes.merge(author_descriptions_df, on='author')
    quotes["scores"] = scores[0]
    quotes = quotes.sort_values("scores", ascending=True) # lower is better
    return quotes

def get_quotes_from_author(name:str):
    return QUOTES_DATASET.loc[QUOTES_DATASET['author'] == name, 'quote']

def get_author_extract(name:str):
    sql = "SELECT description, extract_html, thumbnail_url FROM authors WHERE name = %(name)s;"
    SQL_CURSOR.execute(sql, {"name": name})
    return SQL_CURSOR.fetchone()

def get_similar_authors(name:str):
    try:
        index = AUTHORS_LIST.index(name)
        return AUTHORS_LIST[index-3:index] + AUTHORS_LIST[index+1:index+4]
    except: # if author does not exist
        return AUTHORS_LIST[:6]
