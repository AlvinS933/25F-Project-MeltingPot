import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

try:
    admin_id = st.session_state['admin_id']
    rURL = f"http://web-api:4000/u/admins/{admin_id}"  
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET USER DATA!')

st.title(f"Welcome administrator, {st.session_state['first_name']}.")

#st.write(userJSON["bio"])

if st.button('View User Reports',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/25_user_reports.py')

if st.button('View Recipe Reports',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_recipe_reports.py')

if st.button('Delete Recipes',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_del_recipes.py')

