import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Create your new recipe, {st.session_state['first_name']}.")

if st.button('Example button.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')