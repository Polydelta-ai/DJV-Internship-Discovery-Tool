import streamlit as st
import config
import plotly.graph_objects as go
import json

import random
from PIL import Image
import pandas as pd

from utils import unique_key


def app_setup():
    """
    This function sets the page configurations and style.
    """    
    st.set_page_config(
        page_title = config.PAGE_TITLE, 
        page_icon = config.PAGE_ICON, 
        layout = config.LAYOUT, # "wide" or "centered" 
        initial_sidebar_state = config.INITIAL_SIDEBAR_STATE, 
        menu_items = config.MENU_ITEMS)
    
    hide_st_style = """
            <style>
            #MainMenu {visibilty: hidden;}
            footer {visibility: hidden;}
            </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    

    left_margin, logo_area, other, right_margin = st.columns(config.LOGO_COLUMNS)
    logo = Image.open(config.LOGO_PATH)
    left_margin.image(logo)
    st.title(' ')

    
def internship_posting(post, STATE):
    """
    This function creates the campaign section of the page. Sets the opportunities, talent pool, and metrics for each
    internship. Also, loads in the applicants excel file with info on each applicant.
    """    
    job, talent_pool, views, likes, applications = st.columns([4,1,1,1,1])
    job.title(' ')
    job.subheader(f'**{post.job_title}**')
    talent_pool.metric(label="Talent Pool", value=f'{post.talent_pool:,.0f}', delta=random.randint(-350,350))
    views.metric(label="Views", value=int(post.views), delta=random.randint(1, post.views))
    # print(type(int(post.views)))
    likes.metric(label="Likes", value=int(post.likes), delta=random.randint(-15, post.likes))
    # print(type(post.likes))
    applications.metric(label="Applications", value=int(post.applications), delta=random.randint(1, post.applications))

    recommendations = st.expander('Campaign Details:')
    with recommendations:

        campaigns, margin, prospects = st.columns([1,0.25,4])
        with campaigns:
            st.write(' ')
            st.write(' ')
            st.markdown('<p style="color:#D77B3B; font-weight:bold">ACTIVE JOB POSTS</p>',
                unsafe_allow_html=True)
            active_campaigns = post.active_campaigns.split(', ')
            for active_campaign in active_campaigns:
                active_campaign = active_campaign.strip('[').strip(']').strip("'")
                st.markdown(f'[{active_campaign}](test.com)')

            st.title(' ')
            st.markdown('<p style="color:#D77B3B; font-weight:bold">BROADEN TALENT POOL</p>',
                unsafe_allow_html=True)
            st.write(' ')
            st.write(f'Automatically create a new internship post for **{post.job_title}** that leverages DJV internship explorer insights to broaden your tool pool.')
            st.write(' ')
            st.info(
                "**DJV Talent**:  \n" \
                "Creating a new job posting for a broader audience will generate **365** additional impressions within the DJV Talent Pool")
            st.button('Generate new job post', unique_key())
        

            st.title(' ')
            st.markdown('<p style="color:#D77B3B; font-weight:bold">FOCUS TALENT POOL</p>',
                unsafe_allow_html=True)
            st.write(' ')
            st.write(f'Automatically create a new internship post for **{post.job_title}** that leverages DJV internship explorer insights to focus your tool pool.')
            st.write(' ')
            st.info(
                "**DJV Talent**:  \n" \
                "Creating a new job posting for a more focused audience may better engage the **225** best candidates based on major, location and demographic background.")
            st.button('Generate new job post', key=unique_key())

        with prospects:
            st.write(' ')
            st.write(' ')
            st.markdown('<p style="color:#D77B3B; font-weight:bold">TALENT POOL</p>',
                unsafe_allow_html=True)
            df = pd.read_excel(f'org_data/{post.file}')
            st.table(df)
            

    st.markdown('----')


def pipeline_fig(campaign_data):
    """
    This function creates the Pipeline section for the page. Sets up the graph that displays the different
    pipelines the user may have.
    """
    top_labels = ['Strong Fit', 'Moderate Fit', 'Potential Fit']

    colors = ['rgba(199, 82, 0, 0.8)', 'rgba(255, 105, 0, 0.8)',
            'rgba(255, 137, 55, 0.8)',]

    x_data = campaign_data['x']
    y_data = campaign_data['y']

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(241, 241, 241)',  # Background around chart
        plot_bgcolor='rgb(241, 241, 241)',   # Background around graph
        margin=dict(l=120, r=10, t=80, b=80),
        showlegend=False,
        height = 675 # change the height
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                        color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial', size=14,
                                        color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                            color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='Arial', size=14,
                                                color='rgb(248, 248, 255)'),
                                        showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='Arial', size=14,
                                                    color='rgb(67, 67, 67)'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)

    return fig


def load_session():
    """
    This function loads the session state.
    """
    with open('od_state.json', 'r') as json_file:
        STATE = json.loads(json_file.read())
    return STATE


def update_session(state):
    """
    This function updates the session state.
    """
    with open('od_state.json', 'w') as json_file:
        json.dump(state, json_file)