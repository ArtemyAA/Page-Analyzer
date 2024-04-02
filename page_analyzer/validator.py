from validators import url as check_valid
from urllib.parse import urlparse
from page_analyzer.database_helper import already_exists


def parse_and_normalize(url):
    parsed = urlparse(url)
    normalized = parsed.scheme + '://' + parsed.netloc
    return normalized


def validate(url):
    errors = {}
    norm = parse_and_normalize(url)
    if not url:
        errors['no_url'] = 'Url обязателен!'
    elif not check_valid(norm):
        errors['url_not_valid'] = 'Некорректный формат url'
    elif len(norm) > 255:
        errors['url_is_too_long'] = 'Url не должен быть длиннее 255 символов'
    elif not already_exists(norm):
        errors['url_already_exists'] = 'Url уже есть в базе данных'
    return errors
