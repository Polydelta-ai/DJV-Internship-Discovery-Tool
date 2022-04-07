from operator import ge
from random import randint
import pandas as pd
import feather 
from pandas.core.algorithms import mode
from pandas.core.frame import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import linear_kernel

import os 
from pathlib import Path
from datetime import datetime




my_stop_words = ENGLISH_STOP_WORDS.union(["2020","2021",'22','9910'])


def load_data():
    """
    This reads a feature matrix CSV and loads it into a pandas data frame
    """
    feature_vector_directory = str(Path().resolve().parent.joinpath('feature_engine','feature_vectors'))
    file_directory = [f for f in os.listdir(feature_vector_directory) if "Feature_Matrix" in f]
    file_directory.sort(reverse=True)
    filename = file_directory[0]
    feature_matrix = pd.read_csv("/".join([feature_vector_directory, filename]))

    return feature_matrix


def generate_similarity_df(feature_matrix_column, label_columns_df_index_list):
    """
    This function generates a pandas DataFrame of similarities scores for a given column
    of the feature matrix.

    Parameters:
    feature_matrix_column (str): Name of column from the feature_matrix DataFrame
    title_prefix (str): Code assigned to column title to indicate the similarity matrix 
    (i.e. "JT" for Job Title similarity)

    Returns:
    Pandas Data Frame
    """
    data = feature_matrix_column.to_list()
    tfidfVectorizer = TfidfVectorizer(analyzer = 'word', stop_words=my_stop_words)
    tfidf_wm = tfidfVectorizer.fit_transform(data)
    similarity_matrix = linear_kernel(tfidf_wm, tfidf_wm)
    similarity_matrix_titles = [i for i in label_columns_df_index_list]
    similarity_df = pd.DataFrame(similarity_matrix, columns=similarity_matrix_titles)

    return similarity_df


def generate_similarity_model_artifact():
    """
    This function loads a feature matrix and produces a weighted similarity score
    """
    # Similarity based on feature vector labels
    feature_matrix = load_data()
    label_columns = [col for col in feature_matrix.columns.to_list() if "LR" in col]
    label_columns_df = feature_matrix[label_columns]
    label_columns_df_index_list = label_columns_df.index.to_list()
    label_columns_similarity = cosine_similarity(label_columns_df, label_columns_df)
    label_columns_similarity_df = pd.DataFrame(label_columns_similarity, columns=feature_matrix.index.to_list())

    # Generate similarity dataframes
    job_title_similarity_df = generate_similarity_df(feature_matrix['job_title'], label_columns_df_index_list)
    full_job_description_similarity_df = generate_similarity_df(feature_matrix['full_job_description'],label_columns_df_index_list)
    company_name_similarity_df = generate_similarity_df(feature_matrix['company_name'], label_columns_df_index_list)

    weights = [
        (0.50, label_columns_similarity_df),
        (0.25, job_title_similarity_df),
        (0.15, full_job_description_similarity_df),
        (0.10, company_name_similarity_df),
    ]
    weighted_similarity_score_df = sum([weight[0] * weight[1] for weight in weights])
    weighted_similarity_score_df.columns = [f'W-{i}' for i in weighted_similarity_score_df.columns.to_list()]

    # Combine feature matrix and similarity score
    all_dfs = [
        feature_matrix, 
        weighted_similarity_score_df 
    ] 

    # Generate and save model artifacts
    model_artifacts = pd.concat(all_dfs, axis=1)
    file_timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M%p")
    file_location = f"model_artifacts/model_run-{file_timestamp}.parquet"
    model_artifacts.to_parquet(file_location, index=False)


if __name__ == "__main__":
    generate_similarity_model_artifact()