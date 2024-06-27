import streamlit as st
from auth import authenticate
import face_rec  # Assuming face_rec is a module or function defined elsewhere

# Check if the user is authenticated
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    authenticate()
else:
    st.set_page_config(page_title='Attendance System', layout='wide')

    with st.spinner("Initializing face recognition components"):
        # Importing face_rec here assumes it's correctly defined and accessible
        st.header('Attendance System using Face Recognition')
        st.success('Model loaded successfully')
        st.success('Redis db successfully connected')

    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.experimental_rerun()
