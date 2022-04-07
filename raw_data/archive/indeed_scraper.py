import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

from time import sleep
from random import randint


def get_job_title(job):
    """
    Takes a beautiful soup job object from a list of job_objects returned from:
    jobs = soup.find_all('a','tapItem') 
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
    print("got names etc")


    full_job_post = requests.get(job_link)
    print("Repsonse Code for full_job_post: ", full_job_post.status_code)
    
    try:
        full_job_post = BeautifulSoup(full_job_post.text, 'html.parser')
        full_job_description = full_job_post.find('div', {'id': "jobDescriptionText"}).text

    except:
        full_job_post = "No job post"

    # find the elements
    job_details_section = full_job_post.find('div', {'id': "jobDetailsSection"})
    try:
        job_details = job_details_section.find_all('div', 'jobsearch-JobDescriptionSection-sectionItem')
    except: 
        job_details = ''

    
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


def scrape_indeed_url(url):
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

    return records_df