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
                f"Hi, {st.session_state['first_name']}. It's great to meet you.  \n\n" \
                "Can you tell me a little more about yourself?  Where do you go to school" \
                " and what are you studying?  Also, when do you think you'll graduate?"
            )

            st.title(' ')
            
            form_container = st.container()
            with form_container.form('name_and_education_form'):
                
                # form elements
                first_name = st.text_input('First Name', value=st.session_state['first_name'], key='first_name')
                user_data['first_name'] = first_name

                last_name = st.text_input('Last name', key='last_name')   
                user_data['last_name'] = last_name

                st.markdown('---')
                
                college = st.selectbox('Where do you go to college?', ACCREDITED_COLLEGES, key='college')
                user_data['college'] = college
                
                major = st.selectbox('What is major or focus area of study?', MAJOR, key='major')
                user_data['major'] = major
                
                graduation = st.date_input( "When do you expect to graduate?",
                    value = datetime.date(2022,5,1), 
                    min_value = datetime.date(2022, 1, 1), 
                    key='graduation_year')
                user_data['graduation'] = graduation.strftime("%m-%d-%Y")

                # spacing
                st.subheader('')
                
                # button 
                send_button = st.form_submit_button('Send')
    

    if send_button:
        utils.uppdate_user_data_json(user_data)
        form_container.empty()
        page.empty()
        

        return 'demographic_info_form'