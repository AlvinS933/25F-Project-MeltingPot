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
    rURL = 'http://web-api:4000/r/recipes/user/' + str(uID)
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET USER DATA!')

st.title("My Recipes")

for r in userJSON:
    bTxt = r["name"] + " - " + r["description"][:25] + "..."
    if st.button(bTxt, 
                type='primary',
                use_container_width=True):
        st.session_state["selected_recipe_id"] = str(r["recipeID"])
        st.switch_page('pages/14_Recipe_Details.py')