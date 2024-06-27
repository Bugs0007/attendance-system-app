import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import numpy as np

def run_register_page(face_rec):
    st.subheader('Registration Form')

    # Initialize registration form
    registration_form = face_rec.RegistrationForm()

    # Function to collect facial embedding
    def video_callback_func(frame):
        img = frame.to_ndarray(format='bgr24')  # 3-dimensional numpy array
        reg_img, embedding = registration_form.get_embedding(img)

        # Save embedding data to a local file
        if embedding is not None:
            with open('face_embedding.txt', mode='ab') as f:
                np.savetxt(f, embedding)

        return av.VideoFrame.from_ndarray(reg_img, format='bgr24')

    # Display registration form with webcam streamer
    with st.container(border=True):
        name = st.text_input(label='Name', placeholder='Enter First name and Last name')
        role = 'Student'

        course = st.selectbox(label='Select Course', placeholder='Select Course',
                              options=('Computer Science', 'Electrical', 'Electronics'))
        year_level = st.selectbox(label='Year Level', placeholder='Year Level',
                                  options=('I - First Year', 'II - Second Year', 'III - Third Year', 'IV - Fourth Year'))
        address = st.text_area(label='Address', placeholder='Enter your address')
        contact = st.text_input(label='Contact Number', placeholder='Enter your contact number')
        email = st.text_input(label='Email', placeholder='Enter Email Address')

        st.write('Click on Start button to collect your face samples')
        with st.expander('Instructions'):
            st.caption('1. Give different expressions to capture your face details.')
            st.caption('2. Click on stop after getting 200 samples.')

        webrtc_streamer(key='registration', video_frame_callback=video_callback_func,
                        rtc_configuration={
                            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                        })

    # Save data to Redis database upon submission
    if st.button('Submit'):
        return_val = registration_form.save_data_in_redis_db(name, role)
        if return_val:
            st.success(f"{name} registered successfully")
        elif return_val == 'name_false':
            st.error('Please enter the name: Name cannot be empty or contain only spaces')
        elif return_val == 'file_false':
            st.error('face_embedding.txt is not found. Please refresh the page and execute again.')
