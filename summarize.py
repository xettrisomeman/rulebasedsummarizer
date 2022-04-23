#type: ignore

import matplotlib.pyplot as plt
import seaborn as sns

from utils import (validate_url,  make_dataframe, make_word_cloud, split_news)
from crawl import get_soup
from preprocess import change_to_tokens
from model import (generate_summary, generate_vectors)
from scoring_functions import (
    sentence_title_scores,
    sentence_vector_scores,
    sentence_similarity_scores,
    sentence_position_scores
)

from get_text import (get_text_kantipur, get_text_nagarik)

from collections import Counter
import streamlit as st


plt.rc("font", family="Lohit Devanagari")


def get_summary(url, source, common_size=20):
    if isinstance(source, str):
        news, title = get_soup(source, url)
        first_sentence = news.split('।')[0]
        summary = generate_summary(news, title, first_sentence)
        tokens = change_to_tokens(news)
        text_dict = dict(Counter(tokens).most_common(common_size))
        df = make_dataframe(text_dict)
        wordcloud = make_word_cloud(font_path="mangal.ttf", tokens=text_dict)
        return [summary, df, wordcloud]
    return ["We only support kantipur and nagarik."]


def get_source(source, soup):
    if source.lower() == 'kantipur':
        return get_text_kantipur(firstAttr="article", secondAttr={
                                 "class": "normal"}, soup=soup)
    elif source.lower() == 'nagarik':
        return get_text_nagarik(firstAttr='div', secondAttr={
                                'class': 'news-singles'}, soup=soup)


def get_scores(vector, news_tokens, title, use_k=5):
    text_with_scores = sentence_vector_scores(vector, news_tokens)
    new_text_score = sentence_title_scores(
        news_tokens, text_with_scores, title)
    new_text_score = sentence_position_scores(new_text_score)
    similarity_score, new_text_score = sentence_similarity_scores(
        new_text_score, vector, use_k)
    return similarity_score, new_text_score


def get_summary(url):
    source = validate_url(url)
    if isinstance(source, str):
        try:
            soup = get_soup(url)
            news, title = get_source(source, soup)
            news_tokens = split_news(news)
            vector = generate_vectors(news_tokens)
            similarity_score, new_text_score = get_scores(
                vector, news_tokens, title, use_k=5)
            summary = generate_summary(similarity_score, new_text_score, title)
            tokens = change_to_tokens(news)
            text_dict = dict(Counter(tokens).most_common(20))
            df = make_dataframe(text_dict)
            wordcloud = make_word_cloud(
                font_path="mangal.ttf", tokens=text_dict)
            return [summary, df, wordcloud]
        except ValueError as e:
            return e
    return source


def show_wordcloud(wordcloud):
    fig = plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    return fig


def show_word_frequency(df):
    fig = plt.figure(figsize=(16, 20))
    plt.title("समाचार शब्द गणना")
    sns.barplot(x='गणना', y='लेबल',  data=df)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    return fig


# url = "https://ekantipur.com/local-elections-2022/2022/04/23/165072773172322713.html"


st.title("Nepali Text Summarization Using Rule Based Methods")

form = st.form(key='my-form')
url = form.text_input("Enter full url to scrape the data: ")
submit = form.form_submit_button("Summarize")


if submit:
    summary = get_summary(url)
    if type(summary) != ValueError:
        summary, df, wordcloud = get_summary(url)
        st.subheader("Text Summarization:")
        st.write(summary)
        st.subheader("Count of words:")
        st.pyplot(show_word_frequency(df))

        st.subheader("WordCloud: ")
        st.pyplot(show_wordcloud(wordcloud))
    else:
        fonts = f'<p style="color:Red;">{summary}</p>'
        st.markdown(fonts, unsafe_allow_html=True)
