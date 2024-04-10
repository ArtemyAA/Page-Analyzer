from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import DictCursor
import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_to_db(new_url):
    created_at = datetime.datetime.now()
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
                '''INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id;''',
                (new_url['name'], created_at))
            inserted_id = curs.fetchone()['id']
        conn.commit()
    return inserted_id


def get_url_by_id(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
                'SELECT id, name, created_at FROM urls WHERE id=(%s);', (id,))
            url = curs.fetchone()
            return url


def get_url_by_name(name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
                '''SELECT id, name, created_at
                FROM urls WHERE name=(%s);''', (name,))
            url = curs.fetchone()
            return url


def get_urls_list():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute('''
                        SELECT DISTINCT ON (urls.id)
                        urls.id, urls.name, c.created_at, c.status_code
                        FROM urls LEFT JOIN url_checks as c
                        ON urls.id=c.url_id
                        ORDER BY urls.id DESC, c.created_at DESC;
                        ''')
            urls_list = curs.fetchall()
            return urls_list


def add_check(url_id, status_code, h1,
              title, description):
    created_at = datetime.datetime.now()
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
                '''INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s);''',
                (url_id, status_code, h1, title, description, created_at))
        conn.commit()


def get_check_list(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute('''SELECT * FROM url_checks
                        WHERE url_id=(%s) ORDER BY id DESC;''', (id,))
            url_checks = curs.fetchall()
            return url_checks
