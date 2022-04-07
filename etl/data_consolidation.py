# Import necessary libraries
import pandas as pd
import os


def get_consolidate_data():
    # Load datasets
    indeed = pd.read_csv('extractor/indeed_results/indeed_new_run.csv')
    indeed = indeed[indeed.columns.to_list()[1:]]

    tamu = pd.read_csv('extractor/TAMU_results/tamu.csv')
    tamu = tamu[tamu.columns.to_list()[1:]]

    usa_jobs = pd.read_csv('extractor/USAJobs_results/usa_jobs_internships.csv')
    usa_jobs = usa_jobs[usa_jobs.columns.to_list()[1:]]

    # Transform USAJobs data
    usa_jobs.rename(columns =dict(
        position_title = "job_title",
        organization = "company_name",
        position_location = "company_location",
        major_duties = "full_job_description",
        position_uri = "job_link",
    ), inplace=True)


    # Transform TAMU data
    tamu.rename(columns=dict(
        Titles = "job_title",
        Agency = "company_name",
        Location = "company_location",
        Description = "full_job_description",
        URLs = "job_link",
    ), inplace=True)

    tamu = tamu[tamu['Job Category']=="Internships"]

    # Create index for each dataframe and consolidate
    indeed['source'] = 'indeed'
    indeed['source_index'] = indeed.index.to_list()

    tamu['source'] = 'tamu'
    tamu['source_index'] = tamu.index.to_list()

    usa_jobs['source'] = 'usa_jobs'
    usa_jobs['source_index'] = usa_jobs.index.to_list()

    data = []
    for df in [tamu, usa_jobs, indeed]:
        subdf = df[[
            "job_title",
            "full_job_description",
            "company_name",
            "company_location",
            "job_link",
            "source",
            "source_index"
        ]]
        data.append(subdf)

    data = pd.concat(data, axis=0)
    data.job_title = data.job_title.str.replace("ACE:","")

    # Save data
    data.to_csv('new_combined_source_data.csv', index=False)

if __name__ == "__main__":
    get_consolidate_data()