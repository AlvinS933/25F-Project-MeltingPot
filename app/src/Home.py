##################################################
# This is the main/entry-point file for the 
# MeltingPot Recipe Application
##################################################

import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

logger.info("Loading the Home page of the app")
st.title('MeltingPot')
st.write('### Share Your Recipies with the World!')
st.write('\n\n')
st.write('#### Welcome. Please select your user type and login')

# Fetch users from different tables
try:
    users_response = requests.get('http://web-api:4000/u/users')
    users = users_response.json() if users_response.status_code == 200 else []
except:
    users = [{'userID': 1, 'username': 'Pamela Halpert'}, {'userID': 2, 'username': 'John Brown'}, {'userID': 3, 'username': 'Bobby Altman'}]

try:
    admins_response = requests.get('http://web-api:4000/u/admins')
    admins = admins_response.json() if admins_response.status_code == 200 else []
except:
    admins = [{'adminID': 1, 'username': 'Robert'}, {'adminID': 2, 'username': 'Pauly'}, {'adminID': 3, 'username': 'Carly'}]

try:
    analysts_response = requests.get('http://web-api:4000/u/analysts')
    analysts = analysts_response.json() if analysts_response.status_code == 200 else []
except:
    analysts = [{'analystID': 1, 'username': 'Jim Halpert'}, {'analystID': 2, 'username': 'The Lorax'}, {'analystID': 3, 'username': 'Jim Hooper'}]

# Recipe Creator (Regular User)
st.write('#### 👨‍🍳 Recipe Creator')
selected_creator = st.selectbox(
    'Select a Recipe Creator',
    options=[f"{u['username']} (ID: {u['userID']})" for u in users],
    key='creator_select'
)

if st.button("Login as Recipe Creator", type='primary', use_container_width=True):
    user_id = int(selected_creator.split('ID: ')[1].rstrip(')'))
    username = selected_creator.split(' (ID:')[0]
    
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'recipe_creator'
    st.session_state['first_name'] = username.split()[0]
    st.session_state['user_id'] = user_id
    st.session_state['username'] = username
    logger.info(f"Logging in as Recipe Creator: {username}")
    st.switch_page('pages/00_Recipe_Creator_Home.py')

st.write('---')

# Recipe Browser (Regular User)
st.write('#### 🔍 Recipe Browser')
selected_browser = st.selectbox(
    'Select a Recipe Browser',
    options=[f"{u['username']} (ID: {u['userID']})" for u in users],
    key='browser_select'
)

if st.button('Login as Recipe Browser', type='primary', use_container_width=True):
    user_id = int(selected_browser.split('ID: ')[1].rstrip(')'))
    username = selected_browser.split(' (ID:')[0]
    
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'recipe_browser'
    st.session_state['first_name'] = username.split()[0]
    st.session_state['user_id'] = user_id
    st.session_state['username'] = username
    logger.info(f"Logging in as Recipe Browser: {username}")
    st.switch_page('pages/10_Recipe_Browser_Home.py')

st.write('---')

# Data Analyst
st.write('#### 📊 Data Analyst')
selected_analyst = st.selectbox(
    'Select a Data Analyst',
    options=[f"{a['username']} (ID: {a['analystID']})" for a in analysts],
    key='analyst_select'
)

if st.button('Login as Data Analyst', type='primary', use_container_width=True):
    analyst_id = int(selected_analyst.split('ID: ')[1].rstrip(')'))
    username = selected_analyst.split(' (ID:')[0]
    
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'data_analyst'
    st.session_state['first_name'] = username.split()[0]
    st.session_state['analyst_id'] = analyst_id
    st.session_state['username'] = username
    logger.info(f"Logging in as Data Analyst: {username}")
    st.switch_page('pages/30_Data_Analyst_Home.py')

st.write('---')

# System Administrator
st.write('#### 🛡️ System Administrator')
selected_admin = st.selectbox(
    'Select an Administrator',
    options=[f"{a['username']} (ID: {a['adminID']})" for a in admins],
    key='admin_select'
)

if st.button('Login as Administrator', type='primary', use_container_width=True):
    admin_id = int(selected_admin.split('ID: ')[1].rstrip(')'))
    username = selected_admin.split(' (ID:')[0]
    
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = username.split()[0]
    st.session_state['admin_id'] = admin_id
    st.session_state['username'] = username
    logger.info(f"Logging in as Administrator: {username}")
    st.switch_page('pages/20_Admin_Home.py')