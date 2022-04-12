import streamlit as st
import streamlit.components.v1 as components

from PIL import Image
import pandas as pd
import os
import sys
import json
from random import randint, sample
import pickle

import geopy.distance
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


import config
from appdata.multiselect_validation import _major_df


def show_user_session_data(on):
    if on:
        print(f"Location: {st.session_state['location']}")
        for key, value in st.session_state.items():
            print(key,": ", value)
        print('\n\n\n')
        

def unique_key():
    """
    This fucntion creates a unique key for to distinguish one button from another.
    """
    with open('student_demo-state.json', 'r') as json_file:
        STATE = json.loads(json_file.read())
        count = STATE.get('count', 0)
        count += 1

    STATE['count'] = count
    with open('student_demo-state.json', 'w') as json_file:
        json.dump(STATE, json_file)
    
    return count


def get_sim_list(x):
    """
    This function creates a list of similar internships based on the SIM_THRESHOLD.
    """
    sim_list = x[x>config.SIM_THRESHOLD].index.to_list()
    sim_list = [int(weight.replace('W-','')) for weight in sim_list]
    return sim_list


def get_sample_internship_list(df, verbose=False):
    """
    This function returns a list of sample internships for the user to grade. The function will create a list of 
    internships that will allow the information_threshold to be met in the shortest number of iterations.
    """
    df = df.copy()
    df['scored'] = False
    total_internships = len(df)
    sample_iloc = None

    sample_list = []

    information_threshold = 0.75
    information = 0.0 
    
    iterations = 0
    max_iterations = 50
    
    def update_score(x, sample_iloc):
        if sample_iloc in list(x.sim_list):
            return True
        else:
            return x.scored


    while information < information_threshold and iterations < max_iterations :
        search_df = df[df['scored'] == False]
        if len(df[df['scored'] == False]):
            sample_iloc = search_df[search_df.sim_count == search_df.sim_count.max()].iloc[0].name
        sample_iloc = int(sample_iloc)
        
        
        sample_list.append(sample_iloc)
        df['scored'] = df.apply(lambda x: update_score(x, sample_iloc), axis=1)

        scored = len(df[df['scored'] == True])
        information = scored / total_internships
        iterations += 1
        
        if verbose: print(f'Information: {information * 100:.2f}%\nIterations: {iterations}\n\n')


    return sample_list


def app_setup(state):
    """
    This function (1) builds the required data frames for the user session including
    (a) a blank recommendation data frame that stores personalized recommendations for each internship
    as the user annotates sample internships
    (b) a list of sample internships that are dependent on the recommendation_df['sim_list'], which in turn
    is derived from the similarity theshold set in the config file.
    """
    if state['visible_section'] == 'launch':
        print('System: Generating new recommendations data frame')
        df = pd.read_parquet(config.LATEST_MODEL)
        data = pd.DataFrame(columns = ['iloc', 'overall_interest', 'job_title_fit','job_description_fit','distance_fit'])
        data.to_csv('student_demo-user_annotations.csv', index=False)
        sim_df = df[[c for c in df.columns.to_list() if "W" in c]]
        keep_columns = [
            'job_title',
            'full_job_description',
            'company_name',
            'company_location',
            'source',
            'job_link',
            'states',
            'coordinates',
            
            ]

        recommendations_df = df[keep_columns]
        recommendations_df['U-overall_interest'] = -1
        recommendations_df['U-job_title_fit'] = -1
        recommendations_df['U-job_description_fit'] = -1
        recommendations_df['U-distance_fit'] = 'Not Scored'
        recommendations_df['U-state_preference'] = 'Not Scored'
        recommendations_df['M-overall_interest'] = -1
        recommendations_df['M-job_title_fit'] = -1
        recommendations_df['M-job_description_fit'] = -1
        recommendations_df['M-distance_fit'] = 'Not Scored'
        recommendations_df['M-state_preference'] = 'Not Scored'
        recommendations_df['similar_count'] = sim_df.apply(lambda x: x[x > 0.4].count(), axis = 1)
        recommendations_df['sim_list'] = sim_df.apply(lambda x: get_sim_list(x), axis=1)
        recommendations_df['X-job_title'] = 'No Example Internship'
        recommendations_df['X-company_name'] = 'No Example Internship'
        recommendations_df['X-company_location'] = 'No Example Internship'

        recommendations_df.to_parquet('recommendations_df.parquet')

        families = [f for f in df.columns.to_list() if "family" in f]
        new_df = df[families]
        new_df['sim_count'] = recommendations_df['similar_count'] 
        new_df['sim_list'] = recommendations_df['sim_list']

        family_dfs = dict(
            business = new_df[new_df['LR_business_education_family'] == True][['sim_count','sim_list']],
            science = new_df[new_df['LR_science_education_family'] == True][['sim_count','sim_list']],
            engineering = new_df[new_df['LR_engineering_education_family'] == True][['sim_count','sim_list']],
            unspecified = new_df[new_df['unspecified_education_family'] == True][['sim_count','sim_list']],
        )
    
        internship_samples = {}
        for key, value in family_dfs.items():
            internship_lists = get_sample_internship_list(value)
            internship_samples[key] = recommendations_df.iloc[internship_lists, :6].to_dict()
        
        with open(f'sample_internship_list.json', 'w') as json_file:
            json.dump(internship_samples, json_file)


        STATE = load_session()
        STATE['sample_internship'] = get_sample_internship()
        update_session(STATE)

        print('System: New recommendation data frame successfully created')        


    st.set_page_config(
        page_title = config.PAGE_TITLE, 
        page_icon = config.PAGE_ICON, 
        layout = config.LAYOUT, # "wide" or "centered" 
        initial_sidebar_state = config.INITIAL_SIDEBAR_STATE, 
        menu_items = config.MENU_ITEMS)
    hide_st_style = """
            <style>
            #MainMenu {visibilty: hidden;}
            footer {visibility: hidden;}
            </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    if state['visible_section'] != 'user_results':
        left_margin, logo_area, other, right_margin = st.columns(config.LOGO_COLUMNS)
        logo = Image.open(config.LOGO_PATH)
        logo_area.image(logo)
        st.title(' ')

    
def load_session():
    """
    This fucntion loads the session state from the student demo state json.
    """
    with open('student_demo-state.json', 'r') as json_file:
        STATE = json.loads(json_file.read())
    return STATE


def update_session(state):
    """
    This function updates the session state in the student demo state json.
    """
    with open('student_demo-state.json', 'w') as json_file:
        json.dump(state, json_file)


def load_user_data():
    """
    This function loads the user data from the student demo user data json.
    """
    with open('student_demo-user_data.json', 'r') as json_file:
        STATE = json.loads(json_file.read())
    return STATE


def update_user_data(state):
    """
    This function updates the user data in the student demo user data json.
    """
    with open('student_demo-user_data.json', 'w') as json_file:
        json.dump(state, json_file)


def decode_emoji(emoji):
    """
    This function decodes the emojis into a numerical score.
    """
    emoji_list = ['😕','🤔','🙂','🤩']
    score = emoji_list.index(emoji)
    return score


def encode_emoji(score):
    """
    This function encodes a numerical score to an emoji.
    """
    emoji_list = ['😕','🤔','🙂','🤩']
    emoji = emoji_list[score]
    return emoji


def get_sample_internship():
    """
    This function reads in the 'recommendations_df.parquet' and returns an iloc for a sample internship.
    """
    df = pd.read_parquet('recommendations_df.parquet')
    df = df[df['M-overall_interest'] < 0 ]
    iloc = df[df.similar_count == df.similar_count.max()].iloc[0].name
    return int(iloc)


def assign_annotation(x, current_user_annotation_iloc, column_name, user_annotations, df):
    """
    This function assigns the user annotations to the opportunities in the recommendations_df.
    """
    default = x[f'M-{column_name}']
    recommendation_df_current_row_similarity_list = df.sim_list.iloc[x.name]

    if current_user_annotation_iloc in recommendation_df_current_row_similarity_list:
        user_annotation = user_annotations[user_annotations['iloc'] == current_user_annotation_iloc]
        return user_annotation[column_name].to_list()[0]

    return default


def mark_sample_internship(x, current_user_annotation_iloc, column_name, user_annotations, df):
    """
    This function marks the sample internship once the user has given it a rating.
    """
    default = x[f"X-{column_name}"]
    recommendation_df_current_row_similarity_list = df.sim_list.iloc[x.name]

    if current_user_annotation_iloc in recommendation_df_current_row_similarity_list:
        user_annotation = user_annotations[user_annotations['iloc'] == current_user_annotation_iloc]
        return user_annotation[column_name].to_list()[0]

    return default


def update_recommendations():
    """
    This function loads in the user_annotations_df and the recommendations_df. Then the functions applies 
    the assign_annotations function to the remaining similar opportunities.
    """
    user_annotations = pd.read_csv('student_demo-user_annotations.csv')
    df = pd.read_parquet('recommendations_df.parquet')
    for i in range(len(user_annotations)):
        iloc = user_annotations['iloc'].iloc[i]
                
        df.at[iloc, 'U-overall_interest'] = user_annotations['overall_interest'].iloc[i]
        df.at[iloc, 'U-job_title_fit'] = user_annotations['job_title_fit'].iloc[i]
        df.at[iloc, 'U-job_description_fit'] = user_annotations['job_description_fit'].iloc[i]
        df.at[iloc, 'U-distance_fit'] = user_annotations['distance_fit'].iloc[i]
        df.at[iloc, 'U-state_preference'] = user_annotations['state_preference'].iloc[i]

        df['M-overall_interest'] = df.apply(lambda x: assign_annotation(x, iloc, 'overall_interest', user_annotations, df), axis = 1)
        df['M-job_title_fit'] = df.apply(lambda x: assign_annotation(x, iloc, 'job_title_fit', user_annotations, df), axis = 1)
        df['M-job_description_fit'] = df.apply(lambda x: assign_annotation(x, iloc, 'job_description_fit', user_annotations, df), axis = 1)
        df['M-distance_fit'] = df.apply(lambda x: assign_annotation(x, iloc, 'distance_fit', user_annotations, df), axis = 1)
        df['M-state_preference'] = df.apply(lambda x: assign_annotation(x, iloc, 'state_preference', user_annotations, df), axis = 1)

        df['X-job_title'] = df.apply(lambda x: mark_sample_internship(x, iloc, 'job_title', user_annotations, df), axis = 1)
        df['X-company_name'] = df.apply(lambda x: mark_sample_internship(x, iloc, 'company_name', user_annotations, df), axis = 1)
        df['X-company_location'] = df.apply(lambda x: mark_sample_internship(x, iloc, 'company_location', user_annotations, df), axis = 1)

    df.to_parquet('recommendations_df.parquet')
    
    
def get_lat(location, city_df):
    """
    This function calculates the latitude for a location.
    """
    lat = city_df[city_df['location'] == location].lat
    return lat


def get_long(location, city_df):
    """
    This function calculates the longitude for a location.
    """
    long = city_df[city_df['location'] == location].lng
    return long


def calculate_distance_long_lat(location1, location2):
    """
    This function calculates the distance between two locations.
    """
    coords_1 = get_long_lat(location1, cities, city_data)
    coords_2 = get_long_lat(location2, cities, city_data)
    distance = geopy.distance.distance(coords_1, coords_2).miles
    return distance


def get_major_family(major):
    """
    This function returns the major family for an indicated major.
    """
    user_major_df = _major_df[_major_df.title == major]
    user_major_family = user_major_df.family.iloc[0]

    return user_major_family


def load_samples():
    """
    This function loads the sample_internship_list json.
    """
    with open('sample_internship_list.json', 'r') as json_file:
        samples_dict = json.loads(json_file.read())

    return samples_dict


def generate_recommendation_data():
    """
    This function generates the user recommendations. First it loads the recommendations_df, the latest model, 
    and all of the user data. Then it filters for all internships with a score greater than 1. Next, the function
    creates a df of the states the opportunities are in and how many opportunities are there. The function then creates
    a df of all the possible internships the user may be interested in based off of the major family and the grade the
    user gave a similar internship. After, the function creates a recommendations_data_source df from the 'source' column
    of the scored_major_family_internships df. Finally, the function creates a top_recs df by sorting the scored
    internships by 'M-overall_interest', 'location_tag', 'M-distance_fit', and 'M-job_title_fit'.
    """
    rdf = pd.read_parquet('recommendations_df.parquet')
    df = pd.read_parquet(config.LATEST_MODEL)
    USER_DATA = load_user_data()

    recommendations = rdf[rdf['M-overall_interest'] > 1]
    
    map_states = recommendations.states.value_counts()
    map_states.name='# of internships'
    map_states.to_csv('recommendations_map.csv')
    
    check_column = [col for col in df.columns.to_list() if USER_DATA['major_family'].lower() in col][0]
    major_family_ilocs = df[df[check_column]==True].index.to_list()
    scored_major_family_internships = rdf.iloc[major_family_ilocs]
    
    ld = scored_major_family_internships['M-overall_interest'].value_counts()
    numerator = ld[ld.index > 0].sum()
    denominator = len(scored_major_family_internships)
    interesting_user_opportunities = pd.Series([numerator, denominator], index=['Suggested','Other'], name='opportunities_distribution')
    interesting_user_opportunities.to_csv('recommendations_interesting_opportunities.csv', index=False)

    recommendations_data_source = scored_major_family_internships.source.value_counts()
    recommendations_data_source.name= 'Data Sources'
    recommendations_data_source.rename(index={'usa_jobs':'USA Jobs','tamu':"Texas A&M",'indeed':'Indeed.com'}, inplace=True)
    recommendations_data_source.to_csv('recommendations_data_source.csv')

    top_recs = rdf.sort_values(by=['M-overall_interest', 'location_tag', 'M-distance_fit', 'M-job_title_fit'], ascending=False)
    top_recs = top_recs[top_recs['M-overall_interest'] > 0]
    top_recs = top_recs[top_recs['M-distance_fit'] == "It's Okay"]
    top_recs = top_recs[~top_recs['full_job_description'].str.contains('Paraguay')]
    top_recs.to_csv('top_recs.csv', index=False)


def local_css(file_name):
    """
    This function opens a local .css file.
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def calculate_distance(user_location, internship_location, city_coordinate_mapper):
    """
    This function calculates the distance from the user indicated location to the internship location.
    """
    user_coords = city_coordinate_mapper[user_location]
    internship_coords = city_coordinate_mapper[internship_location]
    distance = geopy.distance.distance(user_coords, internship_coords).miles
    return distance


def location_tag(x, state_preferences_list, state_antipreferences_list):
    """
    This function returns a tag of -1, 0, 1, or 2. A tag of -1 is retunred if the opportunity is located in a state
    that the user indicated they are not interested in. A tag of 1 is returned if the distance between the location
    of the internship is less than 30 miles from the user location. A tag of 2 is returned if the internship is
    located in the same state as the user. Otherwise, a tag of 0 will be returned.
    """
    distance = x.distance
    state = x.states
    
    if state_preferences_list:
        state_preferences_list = list(set(state_preferences_list))
        if state in state_preferences_list: return 2

    if distance < 30: return 1
    
    if state_antipreferences_list:
        state_antipreferences_list = list(set(state_antipreferences_list))
        if state_antipreferences_list: return -1

    return 0


def calculate_df_distances_and_location_tags(df='recs'):
    """
    This function utilizes the city_coordinate_mapper pickle file. The function then creates a 'distance' columns that 
    applies the calculate_distance function to calculate the distance from the user location to the internship location. 
    Next, the function creates a 'location tag' column that uses the location_tag function to apply the tags to each 
    internship opportunity.
    """
    with open('appdata/city_coordinate_mapper.pickle', 'rb') as handle:
        city_coordinate_mapper = pickle.load(handle)
    
    USER_DATA = load_user_data()
    user_location = USER_DATA['user_location']
    state_preferences_list = USER_DATA.get('state_preferences')
    state_antipreferences_list = USER_DATA.get('state_antipreferences')

    if df == "top_recs.csv":
        df = pd.read_csv('top_recs.csv')
        
    else:
        df = pd.read_parquet('recommendations_df.parquet')

    df['distance'] = df.company_location.apply(lambda x: calculate_distance(user_location, x, city_coordinate_mapper))
    df['location_tag'] = df.apply(lambda x: location_tag(x, state_preferences_list, state_antipreferences_list), axis=1)
    

    df.to_parquet('recommendations_df.parquet')


def show_location_tag(tag_code):
    """
    This function displays a preferred_state or a local tag based on the location_tag given to each internship opportunity.
    """  
    if tag_code == 2:
        preferred_state = st.markdown("""
                <button style="border-radius: 4px; border: 1px solid green; background-color:#B9D2AE; color:#098A35">PREFERRED STATE</button>""", 
                unsafe_allow_html=True)

    elif tag_code == 1:
        local = st.markdown("""
                <button style="border-radius: 4px; border: 1px solid blue; background-color:#C6CBFF; color:#372ACE">LOCAL</button>""", 
                unsafe_allow_html=True)

    else: 
        st.write("")


def explain_recommendation(recommendation):
    """
    This function creates a explanation for each recommendation based on the info that the user input. The explanation
    will incluse the user's major family, the sample opportunity that the user rated, and if the user indicated a 
    preference in that state.
    """
    example_job_title = recommendation['X-job_title']
    example_company_name = recommendation['X-company_name']
    example_company_location = recommendation['X-company_location']

    USER_DATA = load_user_data()
    
    explaination = [
        f"""**About this recommendation**  \n\nYou might be interested in this internship because: \n""" \
        f"""- This might be well suited for {USER_DATA['major_family'].lower()} students \n """ \
        f"""- You indicated that you were interested in the **{example_job_title}** opportunity with {example_company_name} in {example_company_location}
        """
    ]

    if recommendation.location_tag == 2:
        preferred_state = f" \n- You indicated that you are interested in seeing opportunities in {recommendation.states}"
        explaination.append(preferred_state)

    if recommendation.location_tag == 1:
        local = f" \n- You indicated that you are interested in seeing opportunities in {recommendation.states}"
        explaination.append(local)

    explaination = "".join(explaination)

    st.info(explaination)