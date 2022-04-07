import streamlit as st
from streamlit_lottie import st_lottie

import config
import utils

def show():
    
    if st.session_state.page['welcome']:
        left_margin, content_box, welcome_lottie, right_margin = st.columns([1,2,2,1])

        with content_box:
            st.subheader('Explore internships in conservation')
            st.write('Ready to get started?')
            st.text_input("", placeholder = "Type your first name here...", key='first_name')
            start = st.button('Let\'s go!', key="start")
            if start:
                st.session_state.page['welcome'] = not st.session_state.page['welcome']
                st.write(st.session_state.page['welcome'])

        with welcome_lottie:
            st_lottie(config.WELCOME_LOTTIE)

