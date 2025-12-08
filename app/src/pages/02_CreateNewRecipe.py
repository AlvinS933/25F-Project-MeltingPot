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
    rURL = 'http://web-api:4000/r/recipes/maxID'
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET USER DATA!')

generatedID = str(int(userJSON[0]["MaxID"]) + 1)

st.title("Create New Recipe")
st.write("### New ID: " + generatedID)

in1 = st.text_input("Name")
in2 = st.text_input("Description")
in3 = st.text_area(
    "Recipe Steps:",
    height=200,   # make the box taller
    placeholder="Write your steps here..."
)
in4 = st.slider(
    "Difficulty",   # Label
    min_value=1,          # Start
    max_value=5,          # End
    value=3               # Default position
)

if st.button('Example button.', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/30_About.py')