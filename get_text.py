#type: ignore
from utils import clean_text


def get_text_kantipur(firstAttr, secondAttr, soup):
    texts = ""
    text_data = soup.find(firstAttr, secondAttr)
    title = text_data.find('div', {'class': 'article-header'}).text.strip()
    get_texts = text_data.find_all('p')
    for textdata in get_texts:
        texts += textdata.text
    return clean_text(texts), title


def get_text_nagarik(firstAttr, secondAttr, soup):
    texts = ""
    text_data = soup.find(firstAttr, secondAttr)
    title = text_data.find('h1').text.strip()
    get_texts = text_data.find_all('p')
    strong_texts = [text.text for text in text_data.find_all('strong')]
    for textdata in get_texts:
        text_data = textdata.text
        if "प्रकाशित:" not in text_data and text_data not in strong_texts:
            texts += text_data
    return clean_text(texts), title
