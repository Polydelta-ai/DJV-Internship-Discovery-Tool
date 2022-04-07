import streamlit as st
from streamlit_lottie import st_lottie
import datetime
import time

from appdata.multiselect_validation import ACCREDITED_COLLEGES, MAJOR


import config
import utils



def show(character_object):
    utils.show_user_session_data(config.SHOW_DATA)


    st.title('Next Placeholder')
    st_lottie(character_object.greeting(), key=utils.unique_lottie_key())
      
        
