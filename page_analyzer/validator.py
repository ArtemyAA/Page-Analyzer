from validators import url as check_valid
from urllib.parse import urlparse
from page_analyzer.database_helper import already_exists


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
