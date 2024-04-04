from validators import url as check_valid
from urllib.parse import urlparse
from page_analyzer.database_helper import already_exists
import requests
from bs4 import BeautifulSoup


def parse(url):
    parsed = urlparse(url)
    normalized = parsed.scheme + '://' + parsed.netloc
    return normalized


def validate(url):
    errors = {}
    if not url:
        errors['no_url'] = 'Url обязателен!'
    elif not check_valid(url):
        errors['url_not_valid'] = 'Некорректный формат url'
    elif len(url) > 255:
        errors['url_is_too_long'] = 'Url не должен быть длиннее 255 символов'
    elif not already_exists(url):
        errors['url_already_exists'] = 'Url уже есть в базе данных'
    return errors


def get_url_info(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    status_code = response.status_code
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.h1.get_text() if soup.h1 else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return status_code, h1, title, description
