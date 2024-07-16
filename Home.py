import streamlit as st
from auth import authenticate  # Ensure this import matches your project structure
import face_rec  # Ensure this import matches your project structure
from pages.Real_Time_Prediction import run_realtime_prediction_page
from pages.Registration_form import run_register_page
from pages.Report import run_report_page

# Apply local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

#Define CSS to center elements
centered_css = """
    <style>
    html, body, .centered-container {
        height: 100%;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .auth-form {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        width: 300px;
        text-align: center;
    }
    </style>
"""


# Display centered CSS
st.markdown(centered_css, unsafe_allow_html=True)

# Authentication logic
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown('<div class="centered-container"><div class="auth-form">', unsafe_allow_html=True)
    st.write("Please authenticate to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):  # Your authentication logic
            st.success("Authenticated successfully")
            st.experimental_rerun()  # Rerun the app to apply the authenticated state
        else:
            st.error("Invalid username or password")
    st.markdown('</div></div>', unsafe_allow_html=True)
else:
    # Your existing Streamlit code
    st.sidebar.title("Navigation")
    menu = ["Real-Time Prediction", "Register", "Report"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    # Add a logout button
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.experimental_rerun()

    if choice == "Real-Time Prediction":
    #     st.title("Attendance System Home")
    #     st.markdown("### Welcome to the Attendance System Application")
    #     st.markdown("""
    #     <div style="background-color: white; padding: 10px; border-radius: 10px;">
    #         <h2>Welcome!</h2>
    #         <p>This is a simple attendance system using face recognition.</p>
    #     </div>
    #     """, unsafe_allow_html=True)
    # elif choice == "Real-Time Prediction":
        st.title("Real-Time Prediction")
        run_realtime_prediction_page(face_rec)
        # Include more content here
    elif choice == "Register":
        st.title("Register")
        run_register_page(face_rec)
        # Include more content here
    elif choice == "Report":
        st.title("Report")
        run_report_page(face_rec)
        # Include more content here


