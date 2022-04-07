# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time
import sys

# Creating data dictionary for scraped data
data_dictionary = {
    'Job Number': [],
    'Job Name': [],
    'Org Name': [], 
    'Location': [],
    'Date Posted': [],
    'job_url': [],
    }

# Set total number of pages on TAMU Job Board
total_pages = 8

# Loop through each page and scrape data for each list in data dictionary
def tamu_scraper(total_pages=total_pages):
    for i in range(total_pages):

        site= f"https://wfscjobs.tamu.edu/page/{i}/?job_category=internships"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page)

        anchors = soup.findAll(class_='job-listing-link')
        for a in anchors:

            job_number = a.find(class_= "job-number").text
            data_dictionary['Job Number'].append(job_number)

            job_name = a.find('h3').text
            data_dictionary['Job Name'].append(job_name)

            org_name = a.find(class_= "job-agency").text
            data_dictionary['Org Name'].append(org_name)

            location = a.find('p', class_= "job-location location").text
            data_dictionary['Location'].append(location)

            date_posted = a.find(class_= "job-posted-date").text
            data_dictionary['Date Posted'].append(date_posted)

            job_url = a['href']
            data_dictionary['job_url'].append(job_url)
    return data_dictionary

# Run function
if __name__ == "__main__":

    # Create dataframe from data dictionary
    df = pd.DataFrame(tamu_scraper())

    # Clean 'Job Number' and 'Date Posted' columns
    df['Job Number'] = df['Job Number'].replace('Job: ', "", regex=True)
    df['Date Posted'] = df['Date Posted'].replace('Posted: ', "", regex=True)

    # Save dataframe to CSV
    df.to_csv('TAMU_results/tamu_jobs.csv', index=False)