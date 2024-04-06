from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    get_flashed_messages)
from dotenv import load_dotenv
from datetime import date
import page_analyzer.database_helper as dbh
import os
from page_analyzer.validator import validate, normalize_url, parse_html

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
        for error_type, error_message in errors.items():
            if error_type == 'url_is_too_long':
                flash(error_message, 'danger')
            elif error_type == 'url_not_valid':
                flash(error_message, 'danger')
            else:
                flash(error_message, 'danger')
        return render_template(
            'search.html',
            new_url=new_url), 422
    elif dbh.already_exists(url_name):
        flash('Страница уже существует', 'info')
        added_url = dbh.get_url_by_name(url_name)
        id = added_url['id']
        return redirect(url_for('get_url', id=id))
    else:
        new_url['created_at'] = date.today()
        new_url['name'] = url_name
        dbh.add_url_to_db(new_url)
        flash('Страница успешно добавлена', 'success')
        added_url = dbh.get_url_by_name(url_name)
        id = added_url['id']
        return redirect(url_for('get_url', id=id))


@app.route('/urls', methods=['GET'])
def show_urls():
    all_urls = dbh.get_urls_list()
    return render_template('urls.html', all_urls=all_urls)


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
    status_code, h1, title, description = parse_html(url['name'])
    if status_code == 200:
        created_at = date.today()
        dbh.add_check(id, status_code, h1, title, description, created_at)
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('get_url', id=id))
