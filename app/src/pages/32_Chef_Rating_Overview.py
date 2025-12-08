import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Chef Rating Overview')

try:
    rURL = 'http://web-api:4000/rat/ratings/topRated'
    response = requests.get(rURL)
    chefsJSON = response.json() if response.status_code == 200 else []
except:
    chefsJSON = []
    st.write('ERROR! CANNOT GET CHEF RATING DATA!')

for c in chefsJSON:
    st.write(str(c["recipeID"]) + " AVG RATING: " + str(c["avgRating"]))