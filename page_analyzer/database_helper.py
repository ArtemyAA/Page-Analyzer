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
            (new_url['name'], new_url['created_at']))
    conn.commit()
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
    conn.close()
    return url


def get_urls_list():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('''
                    SELECT urls.id, urls.name, MAX(ch.created_at), ch.status_code
                    FROM urls JOIN url_checks as ch
                    ON urls.id=ch.url_id
                    GROUP BY urls.id, urls.name, ch.status_code
                    ORDER BY urls.id DESC;
                    ''')
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


def add_check(url_id, status_code, h1=None,
              title=None, description=None, created_at=None):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            '''INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);''',
            (url_id, status_code, h1, title, description, created_at))
    conn.commit()
    conn.close()


def get_check_list(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC;', (id,))
        url_checks = curs.fetchall()
    conn.close()
    return url_checks
