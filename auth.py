import streamlit as st

# User credentials
credentials = {
    "teacher1": "123"
    "teacher2": "234"
}

def authenticate():
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if email in credentials and credentials[email] == password:
            st.session_state['authenticated'] = True
            st.sidebar.success("Authenticated")
        else:
            st.sidebar.error("Invalid email or password")
