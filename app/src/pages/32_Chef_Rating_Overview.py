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

st.subheader("Chefs With High Average Ratings")

for c in chefsJSON:
    if "rating_group" in c and c["rating_group"] == "High":
        name = str(c["username"])
        avg = str(c["avg_rating"])
        count = str(c["rating_count"])
        bTxt = name + " - Avg Rating: " + avg + " (" + count + " ratings)"
        st.button(bTxt, use_container_width=True)

st.subheader("Chefs With Consistently Poor Ratings")

for c in chefsJSON:
    if "rating_group" in c and c["rating_group"] == "Low":
        name = str(c["username"])
        avg = str(c["avg_rating"])
        count = str(c["rating_count"])
        bTxt = name + " - Avg Rating: " + avg + " (" + count + " ratings)"
        st.button(bTxt, use_container_width=True)