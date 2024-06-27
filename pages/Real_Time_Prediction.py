import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import time

def run_realtime_prediction_page(face_rec):
    st.subheader('Real-Time Attendance System')

    # Retrieve the data from Redis Database
    with st.spinner('Retrieving Data from Redis DB ...'):
        redis_face_db = face_rec.retrieve_data(name='academy:register')
        st.dataframe(redis_face_db)

    st.success("Data successfully retrieved from Redis")

    # Time settings
    waitTime = 5  # time in seconds
    setTime = time.time()
    realtimepred = face_rec.RealTimePred()  # real-time prediction class

    # Real-Time Prediction
    def video_frame_callback(frame):
        nonlocal setTime

        img = frame.to_ndarray(format="bgr24")  # 3-dimensional numpy array
        pred_img = realtimepred.face_prediction(img, redis_face_db, 'facial_features', ['Name', 'Role'], thresh=0.5)

        timenow = time.time()
        difftime = timenow - setTime
        if difftime >= waitTime:
            realtimepred.saveLogs_redis()
            setTime = time.time()  # reset time
            print('Save Data to redis database')

        return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

    webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
                    rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                    })
