#type: ignore

from utils import return_punctuation, get_stop_words


def change_to_tokens(news, remove_stop_words=True):
    news_list = news.split()
    cleaned_text = []
    devanagari_punctuation = return_punctuation()
    if remove_stop_words:
        stopword = get_stop_words()
        for news_text in news_list:
            if news_text not in stopword and news_text not in devanagari_punctuation:
                cleaned_text.append(news_text)
    else:
        for news_text in news_list:
            if news_text not in devanagari_punctuation:
                cleaned_text.append(news_text)

    return cleaned_text
