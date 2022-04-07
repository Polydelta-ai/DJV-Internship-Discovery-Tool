import streamlit as st
from streamlit_lottie import st_lottie
import datetime
import time
import json
import os

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR


import config
import utils


JSON_FILE_LOCATION = f"{os.getcwd()}/appdata/user_files/user_data.json"

def show(character_object):
    utils.show_user_session_data(config.SHOW_DATA)
    user_data = utils.sync_userdata(st.session_state)
    

    page = st.empty()

    with page.container():
        left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
      
        with lottie:
            st_lottie(character_object.still(), key=utils.unique_lottie_key())
      
        with content:
            st.title('')
            
            if user_data['identity_question']:
                character_object.say(f"Thanks, {user_data['first_name']}!   I'll keep this in mind as we explore internship opportunities." )
            
            else: 
                character_object.say(f"OK, no worries {user_data['first_name']}!   If you change your mind, we can always discuss this later." )

            st.title(' ')
            
            character_object.say(
                f"If you have a resume or your transcript from {user_data['college']} handy, upload and share them with me so I can use them " \
                "to help find the best matches for you. "
            )

            st.title(' ')

            with st.form('resume_and_transcript_form'):
                
                # Question text
                st.write("I have...")
                
                # Checkboxes
                resume = st.file_uploader('Upload your resume here')
                user_data['resume'] = resume

                transcript = st.file_uploader('Upload your transcript here')
                user_data['transcript'] = transcript

                neither_checkbox = st.checkbox('neither.', key='No Files')
                user_data['neither_checkbox'] = neither_checkbox
                

                if resume is not None:
                    with open("appdata/user_files/resume.gif", "wb") as f:  #update as appropriate
                        f.write(resume.getbuffer())
            
                
                if transcript is not None:
                    with open("appdata/user_files/transcript.svg", "wb") as f: #update as appropriate
                        f.write(transcript.getbuffer())
                
                
                utils.uppdate_user_data_json(user_data)
                submitted = st.form_submit_button('Send')
        
    if submitted:
        page.empty()
        return 'next_placeholder'