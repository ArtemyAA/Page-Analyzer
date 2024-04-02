from flask import (
    Flask, 
    render_template,
    request, redirect,
    url_for,
    flash,
    get_flashed_messages
    )

from validators import url
from dotenv import load_dotenv
from datetime import date
import database_helper as dbh
import os
from validator import validate

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def welcome():
    return render_template('search.html')

@app.route('/urls', methods=['POST'])
def add_url():
    new_url = request.form.to_dict()

    errors = validate(new_url)
    if errors:
        flash
        return
    new_url['created_at'] = date.today()
    

@app.route('/urls', methods=['GET'])
def show_urls():




    

@app.route('/urls/<id>')
def get_url(id):
    
    return 'Здесь будет описание url с определенным id'