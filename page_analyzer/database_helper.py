from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import DictCursor
import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def execute_query(query, params=None, fetchall=True):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            if fetchall:
                return curs.fetchall()
            else:
                return curs.fetchone()


def add_url_to_db(new_url):
    created_at = datetime.datetime.now()
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
                '''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s)
                RETURNING id;
                ''',
                (new_url['name'], created_at))
            inserted_id = curs.fetchone()['id']
        conn.commit()
    return inserted_id


def get_url_by_id(id):
    query = 'SELECT id, name, created_at FROM urls WHERE id=(%s);'
    return execute_query(query, (id,), False)


def get_url_by_name(name):
    query = '''
            SELECT id, name, created_at
            FROM urls
            WHERE name=(%s);
            '''
    return execute_query(query, (name,), False)


def get_urls_list():
    query = '''
            SELECT DISTINCT ON (urls.id)
            urls.id, urls.name, c.created_at, c.status_code
            FROM urls LEFT JOIN url_checks as c
            ON urls.id=c.url_id
            ORDER BY urls.id DESC, c.created_at DESC;
            '''
    return execute_query(query)


def add_check(url_id, status_code, h1,
              title, description):
    created_at = datetime.datetime.now()
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(
                '''
                INSERT INTO url_checks
                (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s);
                ''',
                (url_id, status_code, h1, title, description, created_at))
        conn.commit()


def get_check_list(id):
    query = '''
            SELECT *
            FROM url_checks
            WHERE url_id=(%s)
            ORDER BY id DESC;
            '''
    return execute_query(query, (id,))
