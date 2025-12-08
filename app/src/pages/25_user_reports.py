import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

try:
    admin_id = st.session_state['admin_id']
    rURL = f"http://web-api:4000/u/admins/ur/{admin_id}"  
    user_response = requests.get(rURL)
    userJSON = user_response.json() if user_response.status_code == 200 else []
except:
    userJSON = []
    st.write('# ERROR! CANNOT GET USER DATA!')

st.title("Your User Reports")

for i in userJSON:
    st.write("User ID: " + str(i["userID"]) + ", REASON: " + i["reason"])

if userJSON == []:
    st.write("You don't have any assigned user reports. :)")