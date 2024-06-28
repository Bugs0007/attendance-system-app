import streamlit as st
from auth import authenticate
from pages.Real_Time_Prediction import run_realtime_prediction_page
from pages.Registration_form import run_register_page
from pages.Report import run_report_page
import face_rec

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# Set page configuration
#st.set_page_config(page_title='Attendance System', layout='wide')

# Check if the user is authenticated
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    authenticate()
else:
    page_selection = st.sidebar.radio('Select a page:', ['Real-Time Prediction', 'Registration Form', 'Attendance Report'])

    if page_selection == 'Real-Time Prediction':
        run_realtime_prediction_page(face_rec)
    elif page_selection == 'Registration Form':
        run_register_page(face_rec)
    elif page_selection == 'Attendance Report':
        run_report_page(face_rec)

    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.experimental_rerun()
