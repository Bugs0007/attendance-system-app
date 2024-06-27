#import streamlit as st
#from auth import authenticate
#import face_rec  # Assuming face_rec is a module or function defined elsewhere

## Check if the user is authenticated
#if 'authenticated' not in st.session_state:
 #   st.session_state['authenticated'] = False

#if not st.session_state['authenticated']:
 #   authenticate()
#else:
 #   st.set_page_config(page_title='Attendance System', layout='wide')

  #  with st.spinner("Initializing face recognition components"):
    #    # Importing face_rec here assumes it's correctly defined and accessible
   #     st.header('Attendance System using Face Recognition')
     #   st.success('Model loaded successfully')
      #  st.success('Redis db successfully connected')

    #if st.sidebar.button("Logout"):
     #   st.session_state['authenticated'] = False
      #  st.experimental_rerun()
import streamlit as st
from auth import authenticate
from Home import face_rec
from 1_Real_Time_Prediction import run_realtime_prediction_page
from 2_Registration_Form import run_register_page
from 3_Report import run_report_page

# Check if the user is authenticated
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    authenticate()
else:
    st.set_page_config(page_title='Attendance System', layout='wide')

    # Sidebar navigation
    page_selection = st.sidebar.radio('Navigation', ['Real-Time Prediction', 'Registration Form', 'Attendance Reporting'])

    if page_selection == 'Real-Time Prediction':
        run_realtime_prediction_page(face_rec)
    elif page_selection == 'Registration Form':
        run_register_page(face_rec)
    elif page_selection == 'Attendance Reporting':
        run_report_page(face_rec)
