import streamlit as st
from streamlit_lottie import st_lottie

import config
import utils


def show(character_object):
    

    page = st.empty()
    with page.container():
      
      left_margin, lottie, content, right_margin = st.columns(config.LAYOUT_COLUMNS)
      
      with lottie:
        st_lottie(character_object.greeting(), key=utils.unique_lottie_key())
      
      with content: 
        st.subheader("")
        character_object.say(
          f"Hi!! I\'m {character_object.name.title()}! " \
          "I am virtual assistant at the DJV. It's my job to help students like you " \
          "find internships in the conservation industry.  \n\n"

          "First things first....What's you name?"
          )
        

        st.title('')

        name = st.text_input(
          # "What\'s your first name?", 
          # 'MY RESPONSE:',
          "",
          value = '',
          placeholder= 'Type your first name here....', 
          key='first_name', 
          )

    # page.empty()
    if name != '':
      page.empty()
      print('Print emptying page \n\n')
      location = 'basic_info_form'
      print('Updating Location \n\n')
      
      utils.show_user_session_data(config.SHOW_DATA)
      # return [name], location
      # st.write(location)
      return location