import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Top 5 Most Popular Categories')

try:
    rURL = 'http://web-api:4000/cat/categories/top'
    response = requests.get(rURL)
    chefsJSON = response.json() if response.status_code == 200 else []
except:
    chefsJSON = []
    st.write('ERROR! CANNOT GET CHEF RATING DATA!')

for c in chefsJSON:
    st.write(str(c["name"]) + ", # of Recipes: " + str(c["RecipeCount"]))