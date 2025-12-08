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
    rURL = 'http://web-api:4000/col/collections/' + str(uID)
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET USER DATA!')

st.title("My Collections")

for c in userJSON:
    if st.button(c["title"], 
                type='primary',
                use_container_width=True):
        st.session_state['select_collect'] = c["collectID"]
        st.switch_page('pages/05_ViewCollection.py')