import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About MeltingPot")

st.markdown(
    """
    MeltingPot allows users to rate & share recipes from around the world.
    Users can follow your instructions, and rate the end result on a five-star scale. 
    MeltingPot, as implied in its name, will provide a space for people of different cultures to come together, exchanging culinary delights.
    Recipies contain helpful information such as ingredients, measurements, procedures, images, ratings, and reviews.
    Any recipie or user account that does not follow terms of service may be deleted by an administrator at any time.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
