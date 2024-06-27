
# import streamlit as st
# from Home import face_rec
# from streamlit_webrtc import webrtc_streamer
# import av
# import time
# def run_realtime_prediction_page():
# # from auth import authenticator

# # st.set_page_config(page_title='Predictions')
# st.subheader('Real-Time Attendance System')

# # Retrive the data from Redis Database
# with st.spinner('Retriving Data from Redis DB ...'):
#     redis_face_db = face_rec.retrive_data(name='academy:register')
#     st.dataframe(redis_face_db)

# st.success("Data sucessfully retrived from Redis")

# # time
# waitTime = 5 # time in sec
# setTime = time.time()
# realtimepred = face_rec.RealTimePred() # real time prediction class

# # Real Time Prediction
# # streamlit webrtc
# # callback function
# def video_frame_callback(frame):
#     global setTime

#     img = frame.to_ndarray(format="bgr24") # 3 dimension numpy array
#     # operation that you can perform on the array
#     pred_img = realtimepred.face_prediction(img,redis_face_db,
#                                         'facial_features',['Name','Role'],thresh=0.5)

#     timenow = time.time()
#     difftime = timenow - setTime
#     if difftime >= waitTime:
#         realtimepred.saveLogs_redis()
#         setTime = time.time() # reset time
#         print('Save Data to redis database')


#     return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


# webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
# rtc_configuration={
#         "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
#     }
# )
import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time

def run_realtime_prediction_page():
    st.subheader('Real-Time Attendance System')

    # Retrieve the data from Redis Database
    with st.spinner('Retrieving Data from Redis DB ...'):
        redis_face_db = face_rec.retrive_data(name='academy:register')
        st.dataframe(redis_face_db)

    st.success("Data successfully retrieved from Redis")

    # Initialize variables for real-time prediction
    waitTime = 5  # time in seconds
    setTime = time.time()
    realtimepred = face_rec.RealTimePred()  # Assuming RealTimePred is defined in face_rec

    # Define the callback function for webrtc_streamer
    def video_frame_callback(frame):
        nonlocal setTime

        img = frame.to_ndarray(format="bgr24")  # Convert frame to numpy array (bgr24 format)
        
        # Perform face prediction using the real-time prediction class
        pred_img = realtimepred.face_prediction(img, redis_face_db,
                                                'facial_features', ['Name', 'Role'], thresh=0.5)

        # Manage time for saving logs periodically
        timenow = time.time()
        difftime = timenow - setTime
        if difftime >= waitTime:
            realtimepred.saveLogs_redis()
            setTime = time.time()  # Reset time for next interval
            print('Saved Data to redis database')

        # Return processed image as av.VideoFrame for webrtc_streamer
        return av.VideoFrame.from_ndarray(pred_img, format="bgr24")

    # Initialize webrtc_streamer with defined callback function and RTC configuration
    webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback,
                    rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                    })


