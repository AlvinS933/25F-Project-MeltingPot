import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

try:
    uID = st.session_state['user_id']
    rURL = 'http://web-api:4000/u/users/' + str(uID)
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []

st.title(f"Welcome to the Creator Menu, {st.session_state['first_name']}.")

if st.button('My Recipies', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')

if st.button('Create New Recipie', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')

if st.button('My Collections', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')

if st.button('Create New Collection', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')
