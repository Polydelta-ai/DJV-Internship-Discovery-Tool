import streamlit as st
from streamlit_lottie import st_lottie
import datetime
import time

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR, ETHNICITIES


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
            
            character_object.say(f"Awesome! How do you identify?")
            
            st. title('')
            with st.form(key='identity_form'):
                gender = st.text_input('My gender pronouns are...', placeholder='Type your gender pronouns here.', key='gender')
                user_data['gender'] = gender

                race = st.multiselect("I identify my ethnicity as...", default = None, options = ETHNICITIES)
                user_data['race'] = race[0] if len(race) == 1 else ", ".join(race)

                lgbqtia = st.radio('... a part of the LGBQTIA+ community', ['I am', 'I am not', 'I prefer not to say whether I am'], key='lgbqtia' )
                user_data['lgbqtia'] = lgbqtia

                send = st.form_submit_button(label="Send", help=None, on_click=None, args=None, kwargs=None)
            
            if send:
                utils.uppdate_user_data_json(user_data)
                page.empty()
                return 'resume_and_transcript'
    
