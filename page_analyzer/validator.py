from validators import url as check_valid
from urllib.parse import urlparse
from bs4 import BeautifulSoup


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


def parse_html(html_content):
    if not html_content:
        return '', '', ''
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.h1.get_text() if soup.h1 else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return h1, title, description
