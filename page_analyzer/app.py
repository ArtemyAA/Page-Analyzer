from flask import (
    Flask, 
    render_template,
    request, redirect,
    url_for,
    flash,
    get_flashed_messages
    )
from validator import validate #сделать валидатор
import os
from dotenv import load_dotenv
import psycopg2
from datetime import date

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def welcome():
    return render_template('search.html')

@app.route('/urls', methods=['POST'])
def add_url():

