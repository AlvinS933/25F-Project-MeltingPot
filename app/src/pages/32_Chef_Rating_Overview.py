import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

try:
    rURL = 'http://web-api:4000/da/chefs/ratings-overview'
    r = requests.get(rURL)
    chefsJSON = r.json() if r.status_code == 200 else []
except:
    chefsJSON = []
    st.write('# ERROR! CANNOT GET CHEF RATING DATA!')

st.title("Chef Rating Overview")

for c in chefsJSON:
    name = str(c["username"])
    avg = str(c["avgRating"])
    count = str(c["numRatings"])
    bTxt = name + " - Avg Rating: " + avg + " (" + count + " ratings)"
    st.button(bTxt, use_container_width=True)