import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Vedsu Techonolgy", page_icon="📧")

import eventpage
# import calender

st.header("Event Calender")

with st.container():

#Load configuration from YAML file
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize the authenticator
    authenticator =Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    col1, col2 = st.columns(2)

    name, authentication_status, usernamer = authenticator.login('Login', 'main')

    if authentication_status:

        with col1:
            authenticator.logout('Logout', 'main')
        
        with col2:
            st.markdown(f'Welcome - <span style="color: orange;">*{name}*</span>', unsafe_allow_html=True)
        eventpage.main()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status ==None:
        st.warning('Please enter your username and password')
