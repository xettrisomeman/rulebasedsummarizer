#type: ignore
from scipy import spatial
from string import punctuation


import pandas as pd
from wordcloud import WordCloud

news = [
    'nagarik',
    'kantipur'
]


def split_news(news):
    news_tokens = [news for news in news.split("।") if len(news.strip()) > 10]
    return news_tokens


def validate_url(url):
    source = ""
    if len(url) > 52:
        for news_portal in news:
            data = url.split(news_portal)
            if len(data) > 1:
                source = news_portal
        if source:
            return source
        else:
            return ValueError("We only support kantipur and nagarik news.")
    return ValueError("Link is broken.")


def clean_text(texts):
    special_tokens = ['\xa0', '\u200d', '\u202f']
    for token in special_tokens:
        texts = ' '.join(texts.split(token))
    return texts


def get_stop_words():
    filename = "stopwords.txt"
    stop_words = []
    with open(filename, 'r', encoding="utf-8") as fname:
        data_list = fname.readlines()
        for data in data_list:
            stop_words.append(data.strip())
    return stop_words


def return_punctuation():
    punct = set(list(punctuation) + ["......",
                ":-", "-", "―", "_", "।", '॥', '।', "—"])
    return punct


def compute_similarity(vector_a, vector_b):
    return 1 - spatial.distance.cosine(vector_a, vector_b)


def make_word_cloud(font_path, tokens):
    wordcloud = WordCloud(font_path=font_path,
                          width=300,
                          height=200,
                          background_color='black').generate_from_frequencies(tokens)
    return wordcloud


def make_dataframe(text_list):
    df = pd.DataFrame(columns=['लेबल', 'गणना'])
    df['लेबल'] = text_list.keys()
    df['गणना'] = text_list.values()
    return df
#     plt.figure(figsize=(16, 20))
#     plt.title("समाचार शब्द गणना")
#     sns.barplot(x='गणना', y='लेबल',  data=df)
#     plt.xticks(fontsize=20)
#     plt.yticks(fontsize=20)
