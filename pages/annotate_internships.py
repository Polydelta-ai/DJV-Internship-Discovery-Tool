import streamlit as st
from streamlit_lottie import st_lottie 

from utils import down_scroll
import utils
import time

import config

@st.cache(suppress_st_warning=True)
def show(character_object, internship):
    left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
    user_responses = 'wait'


    with lottie:
        st_lottie(character_object.thinking(), key=utils.unique_lottie_key())

    with content:
        anchor = f'anchor-{len(st.session_state.anchor_list)}'
        st.session_state.anchor_list.append(anchor)
        st.title('', anchor=anchor)
        down_scroll(anchor)

        character_object.say(
            f"Ok {st.session_state.first_name}, let me show a few internships to get a sense" \
            " of your interest."
        )

        st.title(' ')        

        character_object.say(
            f"Tell me your thoughts about this one..."
        )

        st.title(' ')

        st.write(internship.company_name)    
        st.subheader(internship.job_title)

        with st.expander('Full Job Description', expanded=False):
            st.text(internship.full_job_description)


        with st.expander('My Response', expanded=True):
            yes = st.button("This looks interesting!", key=f"button-{len(st.session_state.anchor_list)}")
            no = st.button("Not for me", key=f"button-{len(st.session_state.anchor_list)}")

        anchor = f'anchor-{len(st.session_state.anchor_list)}'
        st.session_state.anchor_list.append(anchor)
        st.title('', anchor=anchor)
        down_scroll(anchor)


    # user_response = dict(
    #     yes_title = False,
    #     yes_job_description = False,
    #     no_title = False,
    #     no_job_description = False,
    #     no_qualifications = False,
    #     )

    # if yes:
    #     left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)

    #     with lottie:
    #         st_lottie(character_object.thinking(), key=utils.unique_lottie_key())

    #     with content:
    #         anchor = f'anchor-{len(st.session_state.anchor_list)}'
    #         st.session_state.anchor_list.append(anchor)
    #         st.title('', anchor=anchor)
    #         down_scroll(anchor)

    #         character_object.say(
    #             f"Awesome, {st.session_state.first_name}! Can you tell me why you are so" \
    #             " excited about this internship?"
    #         )

    #         st.title(' ')

    
    #         with st.form(f'yes-form-{len(st.session_state.anchor_list)+1}'):
    #             st.write('I really liked...')
    #             user_response["yes_title"] = st.checkbox('The internship title')
    #             user_response["yes_job_description"] = st.checkbox('The job description. It seemed interesting.')
    #             send_button = st.form_submit_button('Send')
        # st.stop()

        # if send_button:
        #     return user_response

    # if no:
    #     left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)

    #     with lottie:
    #         st_lottie(character_object.thinking(), key=utils.unique_lottie_key())

    #     with content:
    #         anchor = f'anchor-{len(st.session_state.anchor_list)}'
    #         st.session_state.anchor_list.append(anchor)
    #         st.title('', anchor=anchor)
    #         down_scroll(anchor)

    #         character_object.say(
    #             f"Got it, {st.session_state.first_name}. What turned you off to this" \
    #             " internship?"
    #         )

    #         st.title(' ')

    
    #         with st.form(f'no-form-{len(st.session_state.anchor_list)+1}'):
    #             st.write('My Response')
    #             user_response["no_title"] = st.checkbox('The internship title was not for me.')
    #             user_response["no_job_description"] = st.checkbox('The job description did not seem like a fit.')
    #             user_response["no_qualifications"] = st.checkbox('I don\'t feel qualified for this internship')
    #             send_button = st.form_submit_button('Send')
            
    #         if send_button:
    #             return user_response

    