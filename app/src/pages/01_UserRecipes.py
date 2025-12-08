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
    st.write("trying to request " + rURL)
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET USER DATA!')

st.title(f"Welcome Political Strategist, {st.session_state['first_name']}.")

st.write(userJSON)

if st.button('Example button.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')