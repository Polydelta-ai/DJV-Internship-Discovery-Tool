import streamlit as st
from streamlit_lottie import st_lottie
import datetime
import time

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR


import config
import utils



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
            
            character_object.say(
            f"Wow, {st.session_state['major'].lower()} at {st.session_state['college'].title()}?   " \
            "Sounds exciting!"
            )

            st.title(' ')
            
            character_object.say(
                f"Sometimes there are internship opportunities targeted at students" \
                " from certain backgrounds.  \n\n" \
                " Do you want to check out these opportunities in addition to general internships?"
            )

            st.title(' ')

            with st.expander('My Response', expanded=True):
                yes = st.button("Sure, let's do it!")
                no = st.button("No, thanks.")
            
            st.title(' ')
            
            if yes:
                page.empty()  
                user_data['identity_question'] = "True"     
                utils.uppdate_user_data_json(user_data)
                return "identity_questions"
                

            if no:
                page.empty()
                user_data['identity_question'] = "False"
                utils.uppdate_user_data_json(user_data)
                return 'resume_and_transcript' 