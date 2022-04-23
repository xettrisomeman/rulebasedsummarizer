#type: ignore

import numpy as np


from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline


def generate_vectors(news_tokens):
    np.random.seed(42)
    model = Pipeline([('count', CountVectorizer(lowercase=False)),
                      ('tfidf', TfidfTransformer())])
    data = model.fit_transform(news_tokens)
    return data


def generate_summary(summary_value, new_data, title):
    max_datas = []
    for idx, value in enumerate(summary_value):
        value.remove(1)
        max_data = np.argsort(value)[-1]
        max_datas.append(value[max_data])
    texts = []
    summarized_text = ""
    title = title.strip()
    for _, text, _ in new_data:
        texts.append(text.strip())
    if title in texts:
        summarized_text += title + " । "
    for idx in np.argsort(max_datas)[::-1]:
        if texts[idx] != title:
            summarized_text += texts[idx] + " । "
    return summarized_text
