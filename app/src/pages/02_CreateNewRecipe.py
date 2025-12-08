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

try:
    rURL = 'http://web-api:4000/cat/categories'
    cat_response = requests.get(rURL)
    catJSON = cat_response.json() if cat_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET CAT DATA!')

generatedID = str(int(userJSON[0]["MaxID"]) + 1)

cats = []
for c in catJSON:
    cats.append(c["name"] + ":" + str(c["catID"]))

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

in5 = st.selectbox(
    "Category:",
    cats
)

if st.button('Create', 
             type='primary',
             use_container_width=True):
    package = {
        "recipeID": generatedID,
        "userID": uID,
        "catID": in5.split(":")[1],
        "name": in1,
        "description": in2,
        "steps": in3,
        "picture": "",
        "difficulty": in4
    }
    cURL = 'http://web-api:4000/r/recipes'
    c_response = requests.post(cURL, json=package)
    st.switch_page('pages/00_Recipe_Creator_Home.py')
