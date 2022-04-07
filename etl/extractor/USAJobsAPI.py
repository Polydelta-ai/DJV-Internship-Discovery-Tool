# Import necessary libraries and files
import requests
import numpy as np
import pandas as pd

from local_config import userAgent, authKey
import pandas as pd


class USA_JOBS_SEARCH:
    """
    This class queries the USA Jobs Search API for specific parameters and parses 
    the results into a tidy pandas dataframe.
    This class uses the requests, pandas, and a local config file to pass API credentials
    Example usage:
    
    # create an USA Jobs Search Object
    internships = USA_JOBS_SEARCH({
        "Keyword": 'Internship',
        "PositionOfferingType": 'Student'
        })
    
    # Attributes
        result.df : pandas dataframe
        results.parameters_dict : dictionary of search parameters
        results.base_url: API base url
    """

    def __init__(self, parameters_dict, userAgent = userAgent, authKey = authKey):
        self.parameters_dict = parameters_dict
        self.headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": userAgent,
            "Authorization-Key": authKey,
            }
        self.base_url = "https://data.usajobs.gov/api/search?ResultsPerPage=500"
        
        self.initial_response = self.get_response_json(self.parameters_dict)
        self.response_number_of_pages = self._get_number_of_pages()
        self.all_api_results = self._get_all_api_results()
        self.df = self._get_parsed_results_df()
        

    def get_response_json(self,parameters):
        response = requests.get(self.base_url, params=parameters, headers=self.headers)
        print(response.url)
        data = response.json()
    
        return data

    def _get_number_of_pages(self):
        return int(self.initial_response['SearchResult']['UserArea']['NumberOfPages']) # returns an intenger

    def _get_all_api_results(self):
        all_api_page_results = []
        for i in range(self.response_number_of_pages):
            parameters = self.parameters_dict
            parameters['Page'] = i + 1
            

            page_results = self.get_response_json(parameters)
            page_results = page_results['SearchResult']['SearchResultItems']
            all_api_page_results.append(page_results)

        all_api_results = []
        for lst in all_api_page_results:
            all_api_results.extend(lst)

        
        all_api_results = [all_api_results[i]['MatchedObjectDescriptor'] for i in range(len(all_api_results))]

        return all_api_results


    def _parse_api_results(self, oppty):
        internship_data = dict(
            usajobs_id = oppty['PositionID'],
            position_title = oppty['PositionTitle'],
            position_uri = oppty['PositionURI'],
            position_apply_uri = oppty['ApplyURI'],
            position_location = oppty['PositionLocationDisplay'],
            organization = oppty['OrganizationName'],
            department = oppty['DepartmentName'],
            qualifications = oppty['QualificationSummary'],
            min_pay = oppty['PositionRemuneration'][0]['MinimumRange'],
            max_pay = oppty['PositionRemuneration'][0]['MaximumRange'],
            pay_type = oppty['PositionRemuneration'][0]['RateIntervalCode'],
            position_offering_type = oppty['PositionOfferingType'][0]['Name'],
            job_category = oppty['JobCategory'][0]['Name'],
            job_summary = oppty['UserArea']['Details']['JobSummary'],
            agency_marketing_statement = oppty['UserArea']['Details']['AgencyMarketingStatement'],
            major_duties = oppty['UserArea']['Details']['MajorDuties'][0],
            education = oppty['UserArea']['Details']['Education'],
            requirements = oppty['UserArea']['Details']['Requirements'],
            evaluation = oppty['UserArea']['Details']['Evaluations'],
            key_requirements = oppty['UserArea']['Details']['KeyRequirements'],
        )
        return internship_data
    
    def _get_parsed_results_df(self):

        parsed_results_dictionary =  [self._parse_api_results(result) for result in self.all_api_results]
        parsed_results_dataframe = pd.DataFrame(parsed_results_dictionary)

        return parsed_results_dataframe

def get_usa_jobs():
    # Execute USA_JOBS_SEARCH class
    internships = USA_JOBS_SEARCH({
        "Keyword": 'student',
        "HiringPath": 'student',
    })


    # Create dataframe from API results
    df = internships.df

    # Filters for position titles
    position_title_filters =[
        "student",
        "volunteer",
        "trainee",
        "internship",
        "intern",
        "environmental",
        "environment"
    ]

    # Filters for position offering types
    position_offering_types_filters = [
        "internships",
        "internship",
    ]

    # Filters for job categories
    job_category_filters = [
        "student",
        "trainee",
    ]

    # Dropping the following position offering types
    drop_from_position_offering_type = [
        'permanent',
        'years',
        'yrs',
        'indefinite',
        '2yrs',
        '3yrS',
        'full-time',
        'full time',
        'more than 1-year',
        '4 year term',
        '3 year',
        'multiple appointment types',
        'regular category position',
    ]

    # Filters for departments
    department_filters = [
        'legislative branch',
        'department of the air force',
        'department of veterans affairs',
        'department of the army',
        'department of health and human services',
        'department of defense',
        'department of the navy',
        'department of education',
        'department of labor',
        'department of justice',
        'department of transportation',
        'judicial branch',
        'department of the treasury',
        'department of homeland security',
    ]

    # Filters for organizations
    organization_filters = [
        'office of the inspector general, usps',
        'securities and exchange commission',
        'national labor relations board',
        'federal deposit insurance corporation',
        'consumer financial protection bureau',
        'development finance corporation (formerly overseas private investment corporation)',
        'office of personnel management',
    ]


    # Filtering for position titles, position offering types, and job category
    df = df[(df.position_title.str.lower().str.contains('|'.join(position_title_filters))) |
        (df.position_offering_type.str.lower().str.contains('|'.join(position_offering_types_filters))) |
        (df.job_category.str.lower().str.contains('|'.join(job_category_filters)))] 
        
    # Filtering for departments
    df = df[~df.department.str.lower().str.contains('|'.join(department_filters))]

    # Filtering for organizations
    df = df[~df.organization.str.lower().str.contains('|'.join(organization_filters), regex= False)]

    # Filtering for position offering type
    df = df[~df.position_offering_type.str.lower().str.contains('|'.join(drop_from_position_offering_type))]


    # Save dataframe as CSV
    df.to_csv('USAJobs_results/usa_jobs_internships.csv', index=False)

if __name__ == "__main__":
    get_usa_jobs()