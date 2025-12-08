import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()



try:
    rID = st.session_state["selected_recipe_id"]
    uID = st.session_state['user_id']
    rURL = 'http://web-api:4000/r/recipes/' + str(rID)
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



cats = []
for c in catJSON:
    cats.append(c["name"] + ":" + str(c["catID"]))

st.title("Edit Recipe")
st.write("### ID: " + rID)

in1 = st.text_input("Name", value=userJSON["name"])
in2 = st.text_input("Description", value=userJSON["description"])
in3 = st.text_area(
    "Recipe Steps:",
    height=200,   # make the box taller
    placeholder="Write your steps here...",
    value=userJSON["steps"]
)
in4 = st.slider(
    "Difficulty",   # Label
    min_value=1,          # Start
    max_value=5,          # End
    value=userJSON["difficulty"]
)

in5 = st.selectbox(
    "Category:",
    cats
)

if st.button('Edit', 
             type='primary',
             use_container_width=True):
    package = {
        "catID": in5.split(":")[1],
        "name": in1,
        "description": in2,
        "steps": in3,
        "picture": "",
        "difficulty": in4
    }
    cURL = 'http://web-api:4000/r/recipes/' + str(rID)
    c_response = requests.put(cURL, json=package)
    st.switch_page('pages/00_Recipe_Creator_Home.py')

if st.button('Delete', 
             type='primary',
             use_container_width=True):
    cURL = 'http://web-api:4000/r/recipes/' + str(rID)
    c_response = requests.delete(cURL)
    st.switch_page('pages/00_Recipe_Creator_Home.py')
