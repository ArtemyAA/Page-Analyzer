from validators import url as check_valid
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def normalize_url(url):
    parsed = urlparse(url)
    normalized = parsed.scheme + '://' + parsed.netloc
    return normalized


def validate(url):
    errors = {}
    if not url:
        errors['no_url'] = 'Url обязателен!'
    elif len(url) > 255:
        errors['url_is_too_long'] = 'URL превышает 255 символов'
    elif not check_valid(url):
        errors['url_not_valid'] = 'Некорректный URL'
    return errors


def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status
        response.encoding = 'utf-8'
        html_content = response.text
        return html_content
    except RequestException:
        return None


def parse_html(url):
    content = get_html_content(url)
    if not content:
        return None, '', '', ''
    soup = BeautifulSoup(content, 'html.parser')
    h1 = soup.h1.get_text() if soup.h1 else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return 200, h1, title, description
