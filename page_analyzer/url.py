from validators import url as check_valid
from urllib.parse import urlparse


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
