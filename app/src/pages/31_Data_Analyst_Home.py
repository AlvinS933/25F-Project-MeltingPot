import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')


SideBarLinks()

try:
    aID = st.session_state['analyst_id']
    rURL = 'http://web-api:4000/da/analysts/' + str(aID)
    analyst_response = requests.get(rURL)
    analystJSON = analyst_response.json() if analyst_response.status_code == 200 else []
except:
    analystJSON = []
    st.write('# ERROR! CANNOT GET DATA ANALYST DATA!')

st.title(f"Welcome to the Data Analyst Menu.")




if st.button('Chef Rating Overview',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/10_ChefRatingOverview.py')


if st.button('Popular Recipe Categories',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/11_PopularCategories.py')


if st.button('Trend Graphs & Monthly Comparison',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/12_TrendGraphs.py')


if st.button('User Rating Explorer',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/13_UserRatingExplorer.py')