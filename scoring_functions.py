#type: ignore

from utils import compute_similarity


def sentence_similarity_scores(text_data, vector, use_k):
    matrix = vector.toarray()
    new_score = []
    for mtrx, (text, data) in zip(matrix, text_data):
        new_score.append((mtrx, text, data))
    text_with_scores = sorted(
        new_score, key=lambda x: x[2], reverse=True)[:use_k]
    similarity_score = []
    for (mtrx, _, _) in text_with_scores:
        source = mtrx
        scores = []
        for (mtrx, _, _) in text_with_scores:
            target = mtrx
            score = compute_similarity(source, target)
            scores.append(score)
        similarity_score.append(scores)
    return similarity_score, text_with_scores


def sentence_position_scores(text_data):
    text_with_scores = []
    length = len(text_data)
    mid = round(length/2)
    for idx, (text, value) in enumerate(text_data):
        score = ((length - idx) / length) + value
        if idx >= mid:
            score = ((length - mid + (idx - mid + 1)) / length) + value
        text_with_scores.append((text, round(score, 3)))
    return text_with_scores


def sentence_title_scores(news_tokens, text_with_scores, title):
    title_list = title.split()
    new_score_list = []
    for news_token, (text, score) in zip(news_tokens, text_with_scores):
        old_score = score
        news_length = len(news_token)
        score = 0
        new_score = 0
        for title in title_list:
            if title in news_token:
                score += 1
        new_score = score / news_length + old_score
        new_score_list.append((text, round(new_score, 3)))
    return new_score_list


def sentence_vector_scores(vector, news_tokens):
    text_with_scores = []
    matrix = vector.toarray()
    scores = matrix.sum(axis=1)
    for i, score in enumerate(scores):
        if score > 0:
            text_with_scores.append((news_tokens[i], round(score, 3)))
    return text_with_scores
