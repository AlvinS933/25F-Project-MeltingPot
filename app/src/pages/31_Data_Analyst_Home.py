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
st.title(f"Welcome data analyst, {st.session_state['first_name']}.")
if st.button('Highest Rated Recipes',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Recipe_Rating_Overview.py')

if st.button('Highest Rated Chefs',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Chef_Highest_Rated.py')

if st.button('Most Popular Categories',
             type='primary',
             use_container_width=True):
    st.switch_page('pages/34_Pop_Cats.py')