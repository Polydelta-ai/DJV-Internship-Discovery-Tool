from similarity import weighted_similarity, get_most_similar
import pandas as pd
import os
import sys

from rules_education import * 



def apply_rule_based_labels(df, labelers, feature_names):
    """
    This function takes a list of rule-based labeler functions
    and returns a dataframe with the rules applied

    params: 
        labelers: list of string type objects that are the 
        names offunctions (each function must begin with "label_")
        
        feature_names: list of feature names that strips out "label_"
        which is used to name to the column header in the returned 
        dataframe.
    """
    
    for i in range(len(feature_names)):
        df[feature_names[i]] = df.apply(eval(labelers[i]), axis = 1)
       

    rule_based_label_df = df

    return rule_based_label_df



def get_unlabeled_rows(df, feature_names):
    """
    This function filters out the rows of the data frame that has not
    been labeled by rules or inference.

    Params:
        - df: Dataframe from which to get the unlabeled rows
        - feature_names: list of column headers to check for rule
            based or infered labels

    returns:
        Data frame of unlabeled rows
    """

    filter_parameters = " & ".join([f'{feature_column} == False' for feature_column in feature_names])
    unlabeled_rows_df = df.query(filter_parameters)

    return unlabeled_rows_df




def infer_labels(df_of_unlabeled_rows, df_of_labeled_rows, similarity_threshold, weighted_similarity_score, feature_names):
    """
    This function infers the labels of rows that were not labeled via
    the rule-based functions by inheriting the labels of the most similar 
    rule-based labeled jobs.

    Params:
        - df_of_unlabeled_rows: data frame of rows that were not previously labeled
        - df_of_labeled_rows: reference data frame that is used to lookup previously 
          labeled rows
        - similarity_threshold: Minimum standardized threshold to achieve to be marked
          "similar"
        - weighted_similarity_score: data frame of weighted similarities of all rows
        - feature_names: list of column headers to check for rule 
          based or infered labels


    Returns:
        Data frame of rule-based and infered labels
    """

    unlabeled_rows_list = df_of_unlabeled_rows.index.to_list()
    

    for feature_name in feature_names:
        for row in unlabeled_rows_list:
            similar_jobs = get_most_similar(row, weighted_similarity_score, threshold=similarity_threshold)
            drop_rows = [row for row in similar_jobs.index.to_list() if row in df_of_unlabeled_rows.job_title.to_list()]
            similar_jobs = similar_jobs.drop(labels = drop_rows)
            
            similar_job_labels = [] 
            for similar_job_row in similar_jobs.index.to_list():
                label = df_of_labeled_rows[df_of_labeled_rows['job_title'] == similar_job_row][feature_name].iloc[0]
                similar_job_labels.append(label)

            weighted_similarity_label_df = pd.DataFrame({'similarity_score': similar_jobs, 'label': similar_job_labels})
            print('System: Calculating weighted similarities')
            
            try:
                label = weighted_similarity_label_df.groupby(['label']).sum().similarity_score.sort_values(ascending=False).index.to_list()[0]
            except:
                label = False

            print('System: Updating labels')
            df_of_labeled_rows.loc[row, feature_name] = label

    return df_of_labeled_rows



def label_features(df, labeler_names,  weights, index_name, column_name):
    

    weighted_similarity_score = weighted_similarity(df, weights, index_name, column_name)    
    
    feature_names = []  # Generalized
    feature_names = [label.replace('_label_','').strip() for label in labeler_names]

    # Rule Based Education Labels
    rule_based_feature_matrix = apply_rule_based_labels(df, labeler_names, feature_names)
    
    # Get rows that need infered feature labels because the rules
    # did not immediately apply to them
    rule_based_unlabeled_rows = get_unlabeled_rows(rule_based_feature_matrix, feature_names)
    
    # Add infered labels to rule-based label
    labeled_df = infer_labels(
        rule_based_unlabeled_rows, 
        rule_based_feature_matrix, 
        0.1,  # similarity threshold
        weighted_similarity_score, 
        feature_names)

    # Get the rows that are still unlabeled after (1) applying the rules
    # and (2) infering rules from similar rows that are similar and labeled
    remaining_unlabeled_rows_df = get_unlabeled_rows(labeled_df, feature_names)
    
    labeled_df['unspecified_education_family'] = False
    for index in remaining_unlabeled_rows_df.index.to_list():
        rule_based_feature_matrix.loc[index,'unspecified_education_family'] = True

    return labeled_df
