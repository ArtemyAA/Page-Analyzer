from bs4 import BeautifulSoup


def parse_html(html_content):
    if not html_content:
        return '', '', ''
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.h1.get_text() if soup.h1 else ''
    title = soup.title.string if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return h1, title, description
