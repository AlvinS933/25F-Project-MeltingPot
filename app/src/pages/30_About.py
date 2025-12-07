import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    MeltingPot allows users to share recipes and ingredients for any culinary processes and ideas. This enables others to follow along with the necessary steps and ultimately rate them on a scale. 
    MeltingPot, as implied in its name, will provide a space for people of different cultures to come together, exchanging culinary delights. A recipe contains many helpful information such as ingredients, measurements, procedures, steps, images, ratings, and feedback, to recreate the dish. In order to establish a network of cooking ideas, it is essential that we manage and present the information in a way that is easy to understand and navigate. 

    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
