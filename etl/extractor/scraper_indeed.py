from fileinput import filename
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from datetime import datetime



from time import sleep
from random import randint


def get_search_terms():
    """
    This function takes no parameters and generates a list 
    representation of the search terms in 
    "indeed_search_terms.txt" in the same folder.

    returns: list
    """

    with open('indeed_search_terms.txt', 'r') as f:
        terms = f.read()
        terms = terms.split('\n')
        terms = [term.strip() for term in terms]
    
    return terms


def get_job_title(job):
    """
    Takes a beautiful soup job object from a list of job_objects returned from:
    jobs = soup.find_all('a','tapItem') 

    return: string
    """

    spans = job.h2.find_all('span') 
    for i in range(len(spans)):
        try:
            title = spans[i]['title'].strip()
        except KeyError:
            continue
    
    return title


def get_job_link(job):
    """
    Takes a beautiful soup job object from a list of job_objects returned from:
    jobs = soup.find_all('a','tapItem') 
    """

    link1 = job.get('href')
    link = 'https://www.indeed.com' + link1

    return link


def get_record(job):
    
    job_title = get_job_title(job)
    company_name = job.find('span', 'companyName').text
    company_location = job.find('div', 'companyLocation').text
    job_link = get_job_link(job)
    salary = 'Unspecified'
    job_type = 'Unspecified'

    full_job_post = requests.get(job_link)
    full_job_post = BeautifulSoup(full_job_post.text, 'html.parser')
    full_job_description = full_job_post.find('div', {'id': "jobDescriptionText"}).text


    # find the elements
    job_details_section = full_job_post.find('div', {'id': "jobDetailsSection"})
    job_details = job_details_section.find_all('div', 'jobsearch-JobDescriptionSection-sectionItem')
    
    # parse Salary and Job Type
    for detail in job_details:
        
        if "Salary" in detail.text:
            salary = detail.text.replace('Salary','')
        
        if "Job Type" in detail.text:
            job_type = detail.text.replace('Job Type','')
            list_of_job_types = [s for s in re.split("([A-Z][^A-Z]*)", job_type) if s]
            job_type = ", ".join(list_of_job_types)


    # Get Extract Date
    extract_date = datetime.today().strftime('%Y-%m-%d')


    job_record = dict(
        job_title = job_title,
        company_name = company_name,
        company_location = company_location,
        job_link = job_link,
        job_type = job_type,
        salary = salary,
        full_job_description = full_job_description,
        extract_date = extract_date,
    )
    
    return job_record


def get_filename(url):
    """
    This function takes an URL and parses out the search term
    to create a filename string that can be used for saving 
    a csv of results.

    returns: string
    """

    start = url.find("q=") + 2
    end = url.find("&l=")

    filename = url[start:end]
    filename = filename.replace('+','-')

    return filename


def scrape_indeed_url(url):
    """
    This function takes a job url and generates a dataframe of
    all results. 

    returns: pandas dataframe
    """
    records = []
    start = 0

    while True:
        print("Requesting: ", url)
        response = requests.get(url)

        print("Repsonse Code: ", response.status_code)
        print('\n')

        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('a','tapItem')
        for job in jobs:
            record = get_record(job)
            records.append(record)
            print("Successfully added: ", record['job_title'])
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            start += 10
            url = url[:-2] + str(start)
            delay = randint(1, 10)
            print('\n')
            print(f'Sleeping for {delay} seconds before starting the next request.')
            sleep(delay)
            print('\n')

        except AttributeError:
            break
    
    print("Creating a pandas dataframe...")
    records_df = pd.DataFrame(records)
    print(f"Saving {get_filename(url)}.csv to indeed_results folder")
    filename = get_filename(url)
    records_df.to_csv(f'indeed_results/{filename}.csv', index=False)
    print(f"Successfully saved {get_filename(url)}.csv to indeed_results folder")


def generate_internship_search_term_url(search_term):
    """
    This function takes a search tearm and generates URL to
    search indeed
    """

    base = "https://www.indeed.com/jobs?q="
    stem = "&l=United+States&jt=internship&radius=25"
    term_url_query = "%20".join(search_term.split(" ")) 

    url = f'{base}{term_url_query}{stem}'

    return url


def consolidate_internship_opportunities():
    """
    This function reads all of the csv files in the 'indeed_results' 
    folder and returns a consolidated csv
    """

    indeed_results_csvs = os.listdir('indeed_results')
    dfs = [pd.read_csv(f'indeed_results/{csv_file}') for csv_file in indeed_results_csvs]
    consolidated_df = pd.concat(dfs, axis=0, ignore_index=True)
    consolidated_df.drop_duplicates(inplace=True)
    consolidated_df.to_csv('indeed_results/indeed_new_run.csv')


def get_indeed_internships(start=0):
    """
    This funciton takes no parameters and generates a consolidated
    list of internship opportunites cooresponding to the search terms
    in "indeed_search_terms.txt" in the same folder
    """
    terms = get_search_terms()
    
    for term in terms[start:]:
        url = generate_internship_search_term_url(term)
        try: 
            scrape_indeed_url(url)
        except:
            continue

    consolidate_internship_opportunities()


if __name__ == "__main__":
    get_indeed_internships()

