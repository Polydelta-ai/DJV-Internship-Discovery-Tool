# APPLICATION PAGE CONFIG
# consumed by app_builder _app_config method
# (st.set_page_config documentation)

import json
from turtle import left, right

PAGE_TITLE = None
PAGE_ICON = None
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE="collapsed"
MENU_ITEMS = None 

LATEST_MODEL = 'model/model_artifacts/model_run-2022-03-17_12-15AM.parquet'
SIM_THRESHOLD = 0.4

# LOGO CONFIG
LOGO_PATH = 'assets/djv-logo-48.png'

logo_percentage = 0.2

logo_margins = 1
_logo_column = 1
_non_logo_column = int( _logo_column // logo_percentage)

LOGO_COLUMNS = [logo_margins, _logo_column, _non_logo_column, logo_margins]


# PAGE AND CONTENT CONFIG

left_margin = 0.5
lottie_columns = 1
content_columns = 3
right_margin = 0.5

LAYOUT_COLUMNS = [left_margin, lottie_columns, content_columns, right_margin]
CALC_COLUMNS = [left_margin, 4, right_margin]
JD_LAYOUT_COLUMNS = [3,1,1,1]

RESULT_HEADER_COLUMNS = [left_margin, 1.25, 2.75, right_margin]
INVERSE_RESULT_HEADER_COLUMNS = [left_margin, 2.75, 1.25, right_margin]

# Debugging options
SHOW_DATA = True #If true, print out the st.session_state data to the terminal


# Welcome Lottie
with open(f'lotties/welcome_lottie.json') as f:
    WELCOME_LOTTIE = json.load(f)
    
