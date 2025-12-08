import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title('Chef Rating Overview')

try:
    rURL = 'http://web-api:4000/da/chefs/average_ratings'
    response = requests.get(rURL)
    chefsJSON = response.json() if response.status_code == 200 else []
except:
    chefsJSON = []
    st.write('ERROR! CANNOT GET CHEF RATING DATA!')

if not chefsJSON:
    st.write('No chef rating data available.')
else:
    for c in chefsJSON:
        name = str(c['username'])
        avg = str(c['avg_rating'])
        count = str(c['rating_count'])
        bTxt = name + ' - Avg Rating: ' + avg + ' (' + count + ' ratings)'
        st.button(bTxt, type='primary', use_container_width=True)