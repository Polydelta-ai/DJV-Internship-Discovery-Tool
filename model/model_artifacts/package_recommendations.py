from importlib.metadata import files
import pandas as pd
import os
from pathlib import Path
import json


def get_data():
    
    
    PATH = str(Path().resolve().parent.joinpath('pd-rec-engine-prototype', 'model', 'model_artifacts'))
    directory = os.listdir(PATH)
    filenames = [f for f in directory if 'intern' in f]
    print(filenames)
    dfs = []
    for f in filenames:
        print(f)
        df = pd.read_csv(PATH + "/" + f)
        dfs.append(df)

    df = pd.concat(dfs, axis=1)
    df = df.T
    df.drop_duplicates(keep='first', inplace=True)
    internships = df.T.columns.to_list()[1:]
    internships = [int(i) for i in internships]


    model = pd.read_csv(PATH + "/" +'model_run-2022-02-24_12-30PM.csv') #2022-02-24_12-30PM
    tamu = pd.read_csv(PATH + "/" +'tamu.csv')
    indeed = pd.read_csv(PATH + "/" +'indeed.csv')
    usa_jobs = pd.read_csv(PATH + "/" +'usa_jobs.csv')

    return internships, model, tamu, indeed, usa_jobs



def show_top_10(iloc_list, df):
    
    weighted_columns = [c for c in df.columns.to_list() if "W-" in c]
    data = df[weighted_columns]
    
    top_10_internships = []
    top_10_weights = []
    
    
    for i in iloc_list:
        top_10 = data.iloc[i].sort_values(ascending=False).head(11)
        ilocs = [int(s.replace('W-','')) for s in top_10.index.to_list()]
        
        top_10 = top_10[1:]
        ilocs = ilocs[1:]     

        top_10_weights.extend(top_10)
        top_10_internships.extend(ilocs)
        
    combined_df = pd.DataFrame(dict(
        ilocs = top_10_internships,
        weights = top_10_weights,
    ))

    # print(combined_df)
    combined_top = combined_df.sort_values(ascending=False, by='weights').head(10)
    
    return combined_top.ilocs.to_list(), combined_top.weights.to_list()


def package_recommendations(top_internships, weights, model, tamu, indeed, usa_jobs):

    package = []

    for job in top_internships:
        weights = weights
        job_title = model.iloc[job].job_title
        job_description = model.iloc[job].full_job_description
        company_name = model.iloc[job].company_name
        source = model.iloc[job].source
        source_index = model.iloc[job].source_index

        if source == "tamu":
            link = tamu.iloc[source_index].URLs

        if source == "usa_jos":
            link = usa_jobs.iloc[source_index].position_uri

        if source == "indeed":
            link = indeed.iloc[source_index].job_link

        recommendation = dict(
            weights = weights,
            job_title = job_title,
            job_description = job_description,
            company_name = company_name,
            link = link
        )

        print('jt:', job_title)
        print('jd:', job_description)
        print('cn:', company_name)
        print('source:',source)
        print('si:', source_index )

        package.append(recommendation)
    
    package = pd.DataFrame(package)
    

    return package

def generate_recommendations():

    internships, model, tamu, indeed, usa_jobs = get_data()

    jobs, weights = show_top_10(internships, model)
    package = package_recommendations(jobs, weights, model, tamu, indeed, usa_jobs)
    package.to_csv('recommendations.csv')