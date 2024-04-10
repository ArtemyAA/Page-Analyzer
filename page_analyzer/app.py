from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    flash)
from dotenv import load_dotenv
import page_analyzer.database_helper as dbh
import os
from page_analyzer.validator import (
    validate,
    normalize_url)
from requests.exceptions import RequestException
import requests
from page_analyzer.html_parser import parse_html

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def welcome():
    return render_template('search.html')


@app.route('/urls', methods=['POST'])
def add_url():
    new_url = request.form.to_dict()
    url_name = normalize_url(new_url['url'])
    errors = validate(url_name)
    if errors:
        for error_message in errors.values():
            flash(error_message, 'danger')
        return render_template(
            'search.html',
            new_url=new_url), 422
    existed_url = dbh.get_url_by_name(url_name)
    if existed_url:
        flash('Страница уже существует', 'info')
        id = existed_url['id']
        return redirect(url_for('get_url', id=id))
    else:
        new_url['name'] = url_name
        id = dbh.add_url_to_db(new_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', id=id))


@app.route('/urls', methods=['GET'])
def show_urls():
    all_urls = dbh.get_urls_list()
    return render_template(
        'urls.html',
        all_urls=all_urls)


@app.route('/urls/<int:id>')
def get_url(id):
    url = dbh.get_url_by_id(id)
    checks = dbh.get_check_list(id)
    return render_template(
        'url.html',
        current_url=url,
        checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    url = dbh.get_url_by_id(id)
    try:
        response = requests.get(url['name'])
        response.raise_for_status()
        response.encoding = 'utf-8'
        html_content = response.text
    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))
    h1, title, description = parse_html(html_content)
    dbh.add_check(id, response.status_code, h1, title, description)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
