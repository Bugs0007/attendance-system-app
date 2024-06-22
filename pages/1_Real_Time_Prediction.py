import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

st.subheader('Real-Time Attendance System')

# Retrieve the data from Redis Database
with st.spinner('Retrieving Data from Redis DB ...'):
    redis_face_db = face_rec.retrieve_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success("Data successfully retrieved from Redis")

# Time
waitTime = 30  # time in seconds
setTime = time.time()
realtimepred = face_rec.RealTimePred()  # real-time prediction class

# Streamlit webrtc
# Callback function
def video_frame_callback(frame):
    global setTime

    img = frame.to_ndarray(format="bgr24")  # 3 dimension numpy array
    # Perform operations on the array
    pred_img, recognized_faces = realtimepred.face_prediction(img, redis_face_db, 'facial_features', ['Name', 'Role'], thresh=0.5)

    # Save recognized faces to Redis database immediately
    for face in recognized_faces:
        realtimepred.mark_attendance(face)

    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time()  # reset time
        print('Save Data to redis database')

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

webrtc_streamer(
    key="realtimePrediction", 
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
