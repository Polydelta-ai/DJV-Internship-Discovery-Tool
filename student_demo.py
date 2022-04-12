# Load necessary libraries and functions
from __future__ import annotations
from turtle import right
from typing import overload
import streamlit as st
from streamlit_lottie import st_lottie


import json
import datetime
import time
import pandas as pd
import sys
import plotly.express as px
import plotly.graph_objects as go
import webbrowser
import subprocess
from PIL import Image

import config
from lotties.characters import Character
from utils import calculate_df_distances_and_location_tags, generate_recommendation_data, load_session, load_samples, load_user_data, update_recommendations, update_session, update_user_data, app_setup
from utils import unique_key, decode_emoji, get_major_family, show_location_tag, explain_recommendation 

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR, LOCATIONS, ETHNICITIES, _major_df, STATES

# Load session state and user data json
STATE = load_session()
USER_DATA = load_user_data()    

app_setup(STATE)

character_object = Character(STATE.get("character","nia"))        
   

# Launch page serves as a placeholder to setup app and load model
if STATE['visible_section'] == 'launch':
    start = st.button('start', key=unique_key())
    if start:
        st.write('lets go!')
        STATE['visible_section'] = 'welcome'
        update_session(STATE)
        update_user_data(USER_DATA)
        st.experimental_rerun()


# Welcome page greets user and takes their name
if STATE['visible_section'] == 'welcome':
    
    left_margin, content_box, welcome_lottie, right_margin = st.columns([1,2,3,1])

    with content_box:
        st.title(' ')
        st.title(' ')
        st.title(' ')
        st.title('Explore internships in conservation')
        st.subheader('Ready to get started?')
        st.title(' ')
        st.title(' ')
        first_name = st.text_input("", placeholder = "Type your first name here...", key='first_name')
        start = st.button('Let\'s go!', key="start")
            
            
        if start:
            STATE['visible_section'] = 'basic_info'
            STATE['character'] = 'nia'
            USER_DATA['first_name'] = first_name

            update_session(STATE)
            update_user_data(USER_DATA)
            st.experimental_rerun()
        
        
        with welcome_lottie:
            st_lottie(config.WELCOME_LOTTIE) # Lottie File


# Basic info page gathers info about the user
if STATE['visible_section'] == 'basic_info':
    
    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)

    with lottie:
        st_lottie(character_object.greeting(), key=unique_key())
        
    with content:

        character_object.say(
            f"Hi, {USER_DATA['first_name']}. It's great to meet you.  \n\n" \
            "Can you tell me a little more about yourself?  Where do you go to school" \
            " and what are you studying?  Also, when do you think you'll graduate?"
        )

        st.title(' ')
        
        form_container = st.container()
        with form_container.form('name_and_education_form'):
            
            # form elements
            first_name = st.text_input('First Name', value=USER_DATA['first_name'], key='first_name')
            USER_DATA['first_name'] = first_name

            last_name = st.text_input('Last name', key='last_name')   
            USER_DATA['last_name'] = last_name

            location = st.selectbox('Where do you live?', LOCATIONS, key='user_location')
            USER_DATA['user_location'] = location           

            st.markdown('---')
            
            college = st.selectbox('Where do you go to college?', ACCREDITED_COLLEGES, key='college')
            USER_DATA['college'] = college
            
            major = st.selectbox('What is major or focus area of study?', MAJOR, key='major')
            USER_DATA['major'] = major
            USER_DATA['major_family'] = get_major_family(major)
            
            graduation = st.date_input( "When do you expect to graduate?",
                value = datetime.date(2022,5,1), 
                min_value = datetime.date(2022, 1, 1), 
                key='graduation_year')
            USER_DATA['graduation'] = graduation.strftime("%m-%d-%Y")

            # spacing
            st.subheader('')
            
            # button 
            send_button = st.form_submit_button('Send')


        if send_button:
                STATE['visible_section'] = 'demographic_opt_in'
                
                update_session(STATE)
                update_user_data(USER_DATA)
                st.experimental_rerun()


# Demographic opt in page asks user if they want to enter demographic info
if STATE['visible_section'] == 'demographic_opt_in':

    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
        
    with lottie:
        st_lottie(character_object.still(), key=unique_key())

    with content:
        
        character_object.say(
        f"Wow, {USER_DATA['major'].lower()} at {USER_DATA['college'].title()}?   " \
        "Sounds exciting!"
        )

        st.title(' ')
        time.sleep(0.5)
        
        character_object.say(
            f"Sometimes there are internship opportunities targeted at students" \
            " from certain backgrounds.  \n\n" \
            " Do you want to check out these opportunities in addition to general internships?"
        )
        
        st.title(' ')

        with st.expander('My Response', expanded=True):
            yes = st.button("Sure, let's do it!")
            no = st.button("No, thanks.")
        
        if yes:
            STATE['visible_section'] = 'demographic_info'
            update_session(STATE)
            update_user_data(USER_DATA)
            st.experimental_rerun()

        if no:
            STATE['visible_section'] = 'resume_and_transcript'
            update_session(STATE)
            update_user_data(USER_DATA)
            st.experimental_rerun()


# Demographic info page gathers the user's demographic info
if STATE['visible_section'] == 'demographic_info':

    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
    
    with lottie:
        st_lottie(character_object.still(), key=unique_key())
    
    with content:
        character_object.say(f"Awesome! How do you identify?")
        st. title('')

        with st.form(key='identity_form'):
            gender = st.text_input('My gender pronouns are...', placeholder='Type your gender pronouns here.', key='gender')
            USER_DATA['gender'] = gender

            race = st.multiselect("I identify my ethnicity as...", default = None, options = ETHNICITIES)
            USER_DATA['race'] = race[0] if len(race) == 1 else ", ".join(race)

            lgbqtia = st.radio('... a part of the LGBQTIA+ community', ['I am', 'I am not', 'I prefer not to say whether I am'], key='lgbqtia' )
            USER_DATA['lgbqtia'] = lgbqtia

            send_button = st.form_submit_button(label="Send", help=None, on_click=None, args=None, kwargs=None)

        if send_button:
            STATE['visible_section'] = 'resume_and_transcript'
                
            update_session(STATE)
            update_user_data(USER_DATA)
            st.experimental_rerun()


# Resume and transcript page asks the user to upload their resume and/or transcript 
if STATE['visible_section'] == 'resume_and_transcript':

    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
    
    with lottie:
        st_lottie(character_object.still(), key=unique_key())

    with content:

        if USER_DATA.get('gender'):
            character_object.say(f"Thanks, {USER_DATA['first_name']}!   I'll keep this in mind as we explore internship opportunities." )
        
        else: 
            character_object.say(f"OK, no worries {USER_DATA['first_name']}!   If you change your mind, we can always discuss this later." )

        st.title(' ')

        
        character_object.say(
            f"If you have a resume or your transcript from {USER_DATA['college']} handy, upload and share them with me so I can use them " \
            "to help find the best matches for you. "
        )

        st.title(' ')

       
        with st.form('resume_and_transcript_form'):
            
            # Question text
            st.write("I have...")
            
            # Checkboxes
            resume = st.file_uploader('Upload your resume here', type = ['png','jpg', 'docx', 'doc', 'pdf'])
            USER_DATA['resume'] = resume

            transcript = st.file_uploader('Upload your transcript here', type = ['png','jpg', 'docx', 'doc', 'pdf'])
            USER_DATA['transcript'] = transcript

            neither_checkbox = st.checkbox('neither.', key='No Files')
            USER_DATA['neither_checkbox'] = neither_checkbox
            

            if resume is not None:
                with open("appdata/user_files/resume.gif", "wb") as f:  #update as appropriate
                    f.write(resume.getbuffer())
        
            
            if transcript is not None:
                with open("appdata/user_files/transcript.svg", "wb") as f: #update as appropriate
                    f.write(transcript.getbuffer())
            
            
            # utils.uppdate_user_data_json(user_data)
            submitted = st.form_submit_button('Send')

        
    
    if submitted: 
        STATE['visible_section'] = 'user_annotations'
                
        update_session(STATE)
        update_user_data(USER_DATA)
        st.experimental_rerun()


# User annotations page asks the user to grade sample internship opportunities
if STATE['visible_section'] == 'user_annotations':

    samples_dict = load_samples()
    sample_internship_df = pd.DataFrame(samples_dict[USER_DATA['major_family'].lower()])
    STATE['max_annotations'] = STATE.get('max_annotations', len(sample_internship_df))
    
    STATE['annotation_iteration'] = STATE.get('annotation_iteration', 0) # integer representing position
    internship = sample_internship_df.iloc[STATE['annotation_iteration']]

    STATE['annotation_iteration'] += 1


    
    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
    
    with lottie:
        st_lottie(character_object.thinking(), key=unique_key())

    with content:
        st.title(' ')
        character_object.say(
            f"OK {USER_DATA['first_name']}, let me show you a few internships to get" \
            " a sense of your interest"    
        )

    left_margin, job_description_section, user_annotation_section, right_margin = st.columns([0.5,2,2,0.5])

    with job_description_section:
        st.write(f'{internship["company_name"]} | {internship["company_location"]}')    
        st.header(internship["job_title"])

        with st.expander('Full Job Description', expanded=False):
            st.write(internship["full_job_description"].replace(" \n","  \n\n"))

    with user_annotation_section:
        user_annotation_container = st.container()
        with user_annotation_section.form('user_annotation_form', clear_on_submit=True):

            st.header('My Notes')

            st.subheader('Overall Interest')
            
            overall_interest = st.select_slider(
                'How do you feel about the internship overall?',
                options = ['😕','🤔','🙂','🤩'],
                value = '🤔'
            )
            st.title(' ')

            st.subheader('Description Fit')

            job_title_fit = st.select_slider(
                'What do you think about the internship title?',
                options = ['😕','🤔','🙂','🤩'],
                value = '🤔'
            )

            job_description_fit = st.select_slider(
                'What do you think about the internship position description?',
                options = ['😕','🤔','🙂','🤩'],
                value = '🤔'
            )
            st.title(' ')

            st.subheader('Location Fit')
            distance_fit = st.select_slider(
                'What do you think about the distance?',
                options = ['Too close', "It's Okay", "Too far"],
                value = "It's Okay",
            )
                        
            state_preference = st.select_slider(
                f'Are you open to seeing more internship opportunities in {internship.company_location.split(",")[1]}?',
                options = ['No thanks', 'Maybe', 'Sure'],
                value = "Maybe",
            )

            st.title(' ')
            send_button = st.form_submit_button("Ready for the next one!")
            
            if send_button: 
            
                annotation = dict(
                    iloc = internship.name,
                    job_title = internship.job_title,
                    company_name = internship.company_name,
                    company_location = internship.company_location,
                    overall_interest = decode_emoji(overall_interest),
                    job_title_fit = decode_emoji(job_title_fit),
                    job_description_fit = decode_emoji(job_description_fit),
                    distance_fit = distance_fit,
                    state_preference = state_preference,
                )

                data = pd.read_csv('student_demo-user_annotations.csv')
                save_data = pd.Series(annotation)
                save_data = pd.DataFrame(save_data).transpose()
                data = pd.concat([data, save_data])
                data.to_csv('student_demo-user_annotations.csv', index=False)

                if state_preference == 'Sure':
                    state_preference = USER_DATA.get('state_preferences', [])
                    state = internship.company_location.split(",")[1]
                    state = state.strip()
                    state_preference.append(state)
                    USER_DATA['state_preferences'] = state_preference

                if state_preference == 'No thanks':
                    state_antipreference = USER_DATA.get('state_antipreferences', [])
                    state = internship.company_location.split(",")[1]
                    state = state.strip()
                    state_antipreference.append(state)
                    USER_DATA['state_antipreferences'] = state_antipreference

                if STATE['max_annotations'] == STATE['annotation_iteration']: 
                    STATE['visible_section'] = 'user_results_overview'
                
                update_user_data(USER_DATA)
                update_session(STATE)
                st.experimental_rerun()


# Calculating results page serves as a placeholder while the user's recommendations are calculated
if STATE['visible_section'] == 'calculating_results':
   
    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)

    with lottie:
        st_lottie(character_object.thinking(), key=unique_key())
    
    with content:
        st.title(' ')
        character_object.say(
            f"OK {USER_DATA['first_name']}, thanks for checking out those internships. " \
            "Give me a sec to think about some internships that you might like."    
        )


        STATE['visible_section'] = 'results_calculation_complete'
        update_session(STATE)
        st.experimental_rerun()


# Results calculation complete page tells the user their recommendations are ready and transitions them to the next page
if STATE['visible_section'] == 'results_calculation_complete':



    left_margin, content, right_margin = st.columns([1,1,1])
    with content:
        st_lottie(character_object.aha(), key=unique_key())
        

    left_margin, content, right_margin = st.columns([1,4,1])
    with content:
        character_object.say(
            f"Got it!"
        )
    time.sleep(2.5)

    STATE['visible_section'] = "user_results_overview"
    update_session(STATE)
    st.experimental_rerun()


# User results overview page displays the geographic, fit, and source distribution for the user's recommendations
if STATE['visible_section'] == "user_results_overview":

    update_recommendations()
    calculate_df_distances_and_location_tags()
    generate_recommendation_data()

    map_data = pd.read_csv('recommendations_map.csv')
    ld_data = pd.read_csv('recommendations_interesting_opportunities.csv')
    sources_data = pd.read_csv('recommendations_data_source.csv')


    left_margin, content, right_margin = st.columns(config.CALC_COLUMNS)

    with content:
        st.header('Opportunities Overview')

    left_margin, description, content, right_margin = st.columns(config.RESULT_HEADER_COLUMNS)
    with description:
        
        st.title(' ')
        st.subheader('Where the opportunities are:')
        st.write(f"Given your interests in {USER_DATA['major']} and your responses to the sample internships, here's where the opportunties are!")

        state_preference_list = USER_DATA.get('state_preferences', None)
        if state_preference_list:
            state_preference_list = list(set(USER_DATA['state_preferences']))
            if len(state_preference_list) > 1: state_preference_list.insert(-1, 'and')
            state_preferences = " ".join(state_preference_list)
            if len(state_preference_list) > 3:
                state_preferences = state_preferences.replace(' ',', ', len(state_preference_list) - 1)

            st.write(
                f'You indicated that you are interested in seeing internships in {state_preferences}.' \
                f"If you want to update your preferences, you can do that here!")
        
            if "and" in state_preference_list: state_preference_list.remove('and')
            new_state_preferences = st.multiselect('In which states would you like to see internships?', options = STATES, default = state_preference_list)
            USER_DATA['state_preferences'] = new_state_preferences
        

        else:
            new_state_preferences = st.multiselect('Are you interested in exploring internships in any particular states?', options = STATES)
            USER_DATA['state_preferences'] = new_state_preferences


        rerun = st.button('All set!')
        if rerun:
            update_user_data(USER_DATA)
            calculate_df_distances_and_location_tags()
            generate_recommendation_data()
            st.experimental_rerun()

        st.title(' ')
        st.title(' ')
        geography_button = st.button('Show me my recommendations')
        if geography_button:
                STATE['visible_section'] = "user_results"
                update_session(STATE)
                st.experimental_rerun()
    
    with content:
        fig = px.choropleth(map_data, locations=map_data[map_data.columns.tolist()[0]], locationmode="USA-states", color='# of internships', color_continuous_scale="ylorbr",
                 scope="usa")
        # fig = px.choropleth(locations=map_data[map_data.columns.tolist()[0]], locationmode="USA-states", color=map_data['geography_distribution'], scope="usa")
        st.plotly_chart(fig, use_container_width=True)

    
    st.title(' ')
    left_margin, content, margin, description, right_margin = st.columns([0.1,3,0.5,2.5,1])

    with description:
        st.title(' ')
        st.title(' ')
        st.subheader('How the opportunities fit:')
        st.write(f"Given your responses to the {STATE['max_annotations']} opportunities presented, you might find these internships interesting!")
        
        st.title(' ')
        st.title(' ')
        like_button  = st.button('Show me my recommendations', key=unique_key())
        if like_button:
                STATE['visible_section'] = "user_results"
                update_session(STATE)
                st.experimental_rerun()
        
    with content:
        fig = px.pie(ld_data, values='opportunities_distribution', 
        names=['Potential Fit', 'Maybe'], color_discrete_sequence=['DarkOrange','PeachPuff','SandyBrown', 'Orange', 'Peru', 'Sienna']) 
        st.plotly_chart(fig, use_container_width=True)
    
    st.title(' ')

    left_margin, description, content, right_margin = st.columns(config.RESULT_HEADER_COLUMNS)
    with description:
        st.title(' ')
        st.subheader('Look for opportunities:')
        st.write(f"If you are intrested in going to straight to the source for internships, you can check out these sites!")
        
        st.title(' ')
        tamu = st.button('Texas A&M', key=unique_key())
        if tamu: webbrowser.open_new_tab('https://wfscjobs.tamu.edu/?job_category=internships')
        
        usa_jobs = st.button('USA Jobs', key=unique_key())
        if usa_jobs: webbrowser.open_new_tab('https://www.usajobs.gov/Search/Results?hp=student&k=conservation&p=1')
        
        indeed = st.button('Indeed.com', key=unique_key())
        if indeed: webbrowser.open_new_tab('https://www.indeed.com/jobs?q=conservation&jt=internship&vjk=e25c12bfa099e534')

    with content:
        fig = px.bar(
            sources_data, 
            x=sources_data['Data Sources'], 
            y=sources_data[sources_data.columns.to_list()[0]],
            labels={'Unnamed: 0':'Data Sources','Data Sources':'# of Internships', 'usa_jobs':'USA Jobs'},
            color_discrete_sequence=['DarkOrange','PeachPuff','SandyBrown', 'Orange', 'Peru', 'Sienna'],
            orientation= 'h')

        st.plotly_chart(fig, use_container_width=True)


# User results page lists the user's recommendations 
if STATE['visible_section'] == "user_results":
     data = pd.read_csv('top_recs.csv')
     data = data.drop_duplicates(subset='job_title')
     csv = data.to_csv(columns=['job_title', 'full_job_description', 'company_name', 'job_link', 'source'], index=False).encode('utf-8')
     recommendations = data.head(10)
    
     with st.sidebar:
        st.subheader('How it works')
        st.write(
                f'The DJV Internships in Conservations Finder gathers hundreds of intenships from across the web and its member organizations.  ' \
                f'The tool then groups similar internships together, learns your preferences the sample internships, and applies your background' \
                f'and preferences to all of the internships to generate recommendations.'
            ) 
        
        st.title(' ')

        st.subheader('Think you made a mistake?')
        st.write('Update your suggested internship opportunities by editing your notes on the sample internships.')
        st.write(' ')
        rerun = st.button('Edit my notes')
        if rerun:
                STATE['visible_section'] = "user_annotations"
                STATE['annotation_iteration'] = 0
                update_session(STATE)
                st.experimental_rerun()

        
        st.subheader('Interested in other locations?')
        st.write('Toggle back to the user results overview page and select the states where you would like to look for an internship.')
        st.write(' ')
        rerun = st.button('Edit my location preferences')
        if rerun:
                STATE['visible_section'] = "user_results_overview"
                update_session(STATE)
                st.experimental_rerun()

        


     left_margin, logo_area, other, right_margin = st.columns(config.LOGO_COLUMNS)
     logo = Image.open(config.LOGO_PATH)
     left_margin.image(logo)
     st.title(' ')


     st.title('Internship Suggestions')
     st.write(f'Based on your {USER_DATA["major"].lower()} major and your notes on the sample internship opportunities, here are some internships you might find interesting!') 
     st.download_button(f'Dowload all {len(data)} results!', csv, file_name='DJV-Internship-Recommendations.csv', mime='text/csv')
     st.title(' ')
     st.markdown('<h2 style="color:#D77B3B">Top Suggested Internships</h2>',
                unsafe_allow_html=True)
     st.markdown('---')
    
     for n in range(len(recommendations)):        
        
        company_name, location = st.columns([7,1])
        with company_name:
            st.caption(f"{recommendations.iloc[n].company_name} | {recommendations.iloc[n].company_location}")

        with location:
            show_location_tag(recommendations.iloc[n].location_tag)
            
            
            
        st.subheader(recommendations.iloc[n].job_title)
        url = recommendations.iloc[n].job_link
        st.markdown("[Link to opportunity](%s)" % url)
        st.title(' ')
        with st.expander('Opportunity Details:'):
            explain_recommendation(recommendations.iloc[n])
            st.title(' ')
            st.subheader('Full Job Description')
            st.write(recommendations.iloc[n].full_job_description)
        st.title(' ')
        st.title(' ')
        st.markdown('---')