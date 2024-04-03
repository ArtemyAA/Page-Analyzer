from flask import (
    Flask,
    render_template,
    request, redirect,
    url_for,
    flash,
    get_flashed_messages)
from dotenv import load_dotenv
from datetime import date
import page_analyzer.database_helper as dbh
import os
from page_analyzer.validator import validate, parse

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def welcome():
    return render_template('search.html')


@app.route('/urls', methods=['POST'])
def add_url():
    new_url = request.form.to_dict()
    parsed_url = parse(new_url['url'])
    errors = validate(parsed_url)
    if errors:
        if 'no_url' in errors:
            flash(errors["no_url"], 'danger')
        if 'url_not_valid' in errors:
            flash(errors['url_not_valid'], 'danger')
        if 'url_is_too_long' in errors:
            flash(errors['url_is_too_long'], 'danger')
        if 'url_already_exists' in errors:
            flash(errors['url_already_exists'], 'info')
            added_url = dbh.get_url_by_name(parsed_url)
            id = added_url['id']
            return redirect(url_for(get_url, id=id))
        errors = get_flashed_messages(with_categories=True)
        return render_template(
            'search.html',
            new_url=new_url,
            errors=errors)
    new_url['created_at'] = date.today()
    new_url['name'] = parsed_url
    dbh.add_url_to_db(new_url)
    flash('Страница успешно добавлена', 'success')
    added_url = dbh.get_url_by_name(parsed_url)
    id = added_url['id']
    return redirect(url_for('get_url', id=id))


@app.route('/urls', methods=['GET'])
def show_urls():
    all_urls = dbh.get_urls_list()
    return render_template('urls.html', all_urls=all_urls)


@app.route('/urls/<int:id>')
def get_url(id):
    url = dbh.get_url_by_id(id)
    errors = get_flashed_messages(with_categories=True)
    return render_template('url.html', current_url=url, errors=errors)
