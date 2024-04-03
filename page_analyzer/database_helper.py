from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import DictCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_to_db(new_url):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            'INSERT INTO urls (name, created_at) VALUES (%s, %s);',
            (new_url['url'], new_url['created_at']))
    conn.close()


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            'SELECT id, name, created_at FROM urls WHERE id=(%s);', (id,))
        url = curs.fetchone()
    conn.close()
    return url


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            'SELECT id, name, created_at FROM urls WHERE name=(%s);', (name,))
        url = curs.fetchone()
    conn.commit()
    conn.close()
    return url


def get_urls_list():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls;')
        urls_list = curs.fetchall()
    conn.close()
    return urls_list


def already_exists(url):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE name=(%s);', (url,))
        check = curs.fetchall()
    conn.close()
    if check:
        return False
    return True
