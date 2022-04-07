import streamlit as st
from streamlit_lottie import st_lottie
import datetime
import time

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR


import config
import utils



def show(character_object):
    utils.show_user_session_data(config.SHOW_DATA)


    page = st.empty()

    with page.container():
        left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
      
        with lottie:
            st_lottie(character_object.still(), key=utils.unique_lottie_key())
      
        with content:
            st.title('')
            
            
            if st.session_state['identity_question']:
                character_object.say(f"Thanks, {st.session_state['first_name']}!   I'll keep this in mind as we explore internship opportunities." )
            
            if st.session_state['identity_question']:
                character_object.say(f"OK, no worries {st.session_state['first_name']}!   If you change your mind, we can always discuss this later." )

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
                st.session_state['identity_question'] = True     
                return "identity_questions"
                

            if no:
                page.empty()
                st.session_state['identity_question'] = False
                return data, next_location