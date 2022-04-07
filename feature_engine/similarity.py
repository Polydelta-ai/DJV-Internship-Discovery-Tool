import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import linear_kernel


my_stop_words = ENGLISH_STOP_WORDS.union([
    "2020",
    "2021",
    '22',
    '9910',
    ])

def get_similarities(focus_column, stop_words = my_stop_words):

    focus_column = focus_column.to_list()

    tfidfVectorizer = TfidfVectorizer(analyzer = 'word', stop_words=stop_words)
    tfidf_wm = tfidfVectorizer.fit_transform(focus_column)
    cosine_similarities = linear_kernel(tfidf_wm, tfidf_wm)

    df = pd.DataFrame(cosine_similarities)

    return df


def weighted_similarity(df, weights, column_name, index_name):

    component_scores = []
    for column, weight in weights.items():
        component_score = get_similarities(df[column])
        component_scores.append((component_score,weight))

    weighted_similarity_score = sum([component_score[0] * component_score[1] for component_score in component_scores])

    weighted_similarity_score.columns = df[column_name]
    weighted_similarity_score.index = df[index_name]

    return weighted_similarity_score 


def get_most_similar(x, df, threshold=0.1):
    job = df.iloc[x]
    similar_jobs = job[job > threshold]
    similar_jobs = similar_jobs.sort_values(ascending=False)
    
    return similar_jobs.iloc[1:]