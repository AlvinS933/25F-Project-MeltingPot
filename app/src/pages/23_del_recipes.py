import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title("Recipe Deletion Tool")
st.write("(Be Careful. Deletion is Permanent!)")

num = st.number_input("Enter a Recipe ID", min_value=0, value=0, step=1)

if st.button('DELETE.', 
             type='primary',
             use_container_width=True):
    cURL = 'http://web-api:4000/r/recipes/' + str(num)
    c_response = requests.delete(cURL)
    st.switch_page('pages/00_Recipe_Creator_Home.py')