from random import randint
import pandas as pd

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import config
from od_utils import app_setup, internship_posting, pipeline_fig, load_session, update_session

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR, LOCATIONS, ETHNICITIES, _major_df, STATES

STATE = load_session()

campaign_data = dict(
    x = [
        [27, 33, 40,],
        [28, 30, 42,],
        [33, 22, 45,],
        ],
    
    y = [
            'New Jersey Biology Students<br><b>266 Students</b>',
            'African American Environmental<br>Policy Students<br><b>788 Students</b>',
            'LGBQTIA+ Conservation Students<br><b>113 Students</b>',
            ]
)

app_setup()



st.markdown('<h2 style="color:#D77B3B">INTERNSHIP POSTINGS</h2>',
    unsafe_allow_html=True)



st.markdown("---")

posts = pd.read_csv('org_data/internship_postings.csv')
posts = posts.astype({
    "talent_pool":"int",
    "views":"int",
    "matches":"int",
    "likes":"int",
    "applications":"int",
    "broaden":"int",
    "focus":"int"
})
internships = [
    'Soil Conservation Technician',
    'Community Conservation Fellow',
    'Assistant Scientist',
]

ilocs = []
for internship in internships:
    if STATE[internship] == 'normal':
        iloc = posts[(posts["add_broaden"] == False) & (posts["add_focus"] == False) & (posts.job_title == internship)].index.values[0]
        ilocs.append(iloc)
    elif STATE[internship] == 'broaden':
        iloc = posts[(posts.add_broaden == True) & (posts.job_title == internship)].index.values[0]
        ilocs.append(iloc)
    else:
        iloc = posts[(posts.add_focus == True) & (posts.job_title == internship)].index.values[0]
        ilocs.append(iloc)

ilocs = list(ilocs)

posts = posts.iloc[ilocs]

for i in range(len(posts)):
    
    

    internship_posting(posts.iloc[i], STATE)
    
    

st.markdown('<h2 style="color:#D77B3B">MY TALENT PIPELINES</h2>',
    unsafe_allow_html=True)

with st.expander('About My Talent Pipelines'):
    st.info(
        '**DJV Talent**  \n'\
        'Your talent pipelines allow you to monitor and engage prospective candidates'\
        'even when you do not yet have a live internship opportunity.  '\
        'These pipelines are built on top of the DJV Talent Pool.' )

form, pipelines = st.columns([1.25,3.75])
with form:
    with st.form('Add Talent Pipeline'):
        st.write("**ADD A NEW TALENT PIPELINE**")
        pipeline_name = st.text_input('New talent pipeline name')
        st.write(' ')
        st.write("**Pipeline Target Sources**")
        job_titles = st.text_input('Job title keywords')
        demograghics = st.multiselect('Demographics', options = ETHNICITIES)
        agree = st.checkbox('LGBQTIA+')
        states = st.multiselect('States', options = STATES)
        colleges = st.multiselect('Academic Institutions', options = ACCREDITED_COLLEGES)

        add = st.form_submit_button('Add')
        if add:
            pipeline_name = pipeline_name + f"<br><b>{randint(100, 300)} Students</b>"
            campaign_data['y'].append(pipeline_name)
            random_strong_fit = randint(20, 35)
            random_moderate_fit = randint(17, 35)
            random_potential =  100 - random_moderate_fit - random_strong_fit
            campaign_data['x'].append([random_strong_fit, random_moderate_fit, random_potential])


fig = pipeline_fig(campaign_data)
pipelines.plotly_chart(fig, use_container_width=True)