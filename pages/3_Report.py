# import pandas as pd
# import streamlit as st
# from Home import face_rec
# import datetime



# # from auth import authenticator

# # st.set_page_config(page_title='Reporting',layout='wide')
# st.subheader('Reporting')

# # if st.session_state['authentication_status']:
# #     authenticator.logout('Logout', 'sidebar', key='unique_key')

# # Retrive logs data and show in Report.py
# # extract data from redis list
# name = 'attendance:logs'
# def load_logs(name,end=-1):
#     logs_list = face_rec.r.lrange(name,start=0,end=end) # extract all data from the redis database
#     return logs_list

# # tabs to show the info
# tab1, tab2, tab3 = st.tabs(['Registered Data','Logs','Attendance Report'])

# with tab1:
#     if st.button('Refresh Data'):
#         # Retrive the data from Redis Database
#         with st.spinner('Retriving Data from Redis DB ...'):
#             redis_face_db = face_rec.retrive_data(name='academy:register')
#             st.dataframe(redis_face_db[['Name','Role']])

# with tab2:
#     if st.button('Refresh Logs'):
#         st.write(load_logs(name=name))


# with tab3:
#     st.subheader('Attendance Report')

#     # load logs into attribute logs_list
#     logs_list = load_logs(name=name)

#     # step -1: convert the logs that in list of bytes into list of string
#     convert_byte_to_string = lambda x: x.decode('utf-8')
#     logs_list_string = list(map(convert_byte_to_string, logs_list))

#     # step -2: split string by @ and create nested list
#     split_string = lambda x: x.split('@')
#     logs_nested_list = list(map(split_string, logs_list_string))
#     # convert nested list info into dataframe

#     logs_df = pd.DataFrame(logs_nested_list, columns= ['Name','Role','Timestamp'])

#     # Step -3 Time based Analysis or Report
#     #logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
#     logs_df['Timestamp'] = logs_df['Timestamp'].apply(lambda x: x.split('.')[0])
#     logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
#     logs_df['Date'] = logs_df['Timestamp'].dt.date

#     # step -3.1 : Cal. Intime and Outtime
#     # In time: At which person is first detected in that day (min Timestamp of the date)
#     # Out time: At which person is last detected in that day (Max Timestamp of the date)

#     report_df = logs_df.groupby(by=['Date','Name','Role']).agg(
#         In_time = pd.NamedAgg('Timestamp','min'), # in time 
#         Out_time = pd.NamedAgg('Timestamp','max') # out time
#     ).reset_index()

#     report_df['In_time']  = pd.to_datetime(report_df['In_time'])
#     report_df['Out_time']  = pd.to_datetime(report_df['Out_time'])

#     report_df['Duration'] = report_df['Out_time'] - report_df['In_time']

#     # Step 4: Marking Person is Present or Absent
#     all_dates = report_df['Date'].unique()
#     name_role = report_df[['Name','Role']].drop_duplicates().values.tolist()

#     date_name_rol_zip = []
#     for dt in all_dates:
#         for name, role in name_role:
#             date_name_rol_zip.append([dt, name, role])

#     date_name_rol_zip_df = pd.DataFrame(date_name_rol_zip, columns=['Date','Name','Role'])
#     # left join with report_df

#     date_name_rol_zip_df = pd.merge(date_name_rol_zip_df, report_df, how='left',on=['Date','Name','Role'])

#     # Duration
#     # Hours
#     date_name_rol_zip_df['Duration_seconds'] = date_name_rol_zip_df['Duration'].dt.seconds
#     date_name_rol_zip_df['Duration_hours'] = date_name_rol_zip_df['Duration_seconds'] / (60*60)

#     def status_marker(x):

#         if pd.Series(x).isnull().all():
#             return 'Absent'
        
#         elif x >= 0 and x < 0.001:
#             return 'Absent (Less than 1 hr)'
        
#         elif x >= 0.001 :
#             return 'Present'
        
#     date_name_rol_zip_df['Status'] = date_name_rol_zip_df['Duration_hours'].apply(status_marker)

#     # tab
#     t1, t2 = st.tabs(['Complete Report','Filter Report'])

#     with t1:
#         st.subheader('Complete Report')
#         st.dataframe(date_name_rol_zip_df)

#     with t2:
#         st.subheader('Search Records')

#         # Date

#         date_in = str(st.date_input('Filter Date', datetime.datetime.now().date()))
        
#         # Filter the person names
#         name_list = date_name_rol_zip_df['Name'].unique().tolist()
#         name_in = st.selectbox('Select Name', ['ALL']+name_list)

#         # Filter Teachers or Students (role)
#         role_list = date_name_rol_zip_df['Role'].unique().tolist()
#         role_in = st.selectbox('Select Role', ['ALL']+role_list)

#         # Filter the duration

#         duration_in = st.slider('Filter the duration in hours greater than ', 0, 15, 6)

#         # Status
#         status_list = date_name_rol_zip_df['Status'].unique().tolist()
#         status_in = st.multiselect('Select the Status', ['ALL']+status_list) # return 

#         if st.button('Submit'):
#             date_name_rol_zip_df['Date'] = date_name_rol_zip_df['Date'].astype(str)

#             # filter date
#             filter_df = date_name_rol_zip_df.query(f'Date == "{date_in}"')

#             # Filter the name
#             if name_in != 'ALL':
#                 filter_df = filter_df.query(f'Name == "{name_in}"')

#             # Filter the ROLE
#             if role_in != 'ALL':
#                 filter_df = filter_df.query(f'Role == "{role_in}"')


#             # Filter the Duration
#             if duration_in > 0:
#                 filter_df = filter_df.query(f'Duration_hours > {duration_in}')


#             # Filter the Status
#             if 'ALL' in status_in:
#                 filter_df = filter_df

#             elif len(status_in) > 0:
#                 filter_df['status_condition'] = filter_df['Status'].apply(lambda x: True if x in status_in else False)
#                 filter_df = filter_df.query(f'status_condition == True')
#                 filter_df.drop(columns='status_condition',inplace=True)

#             else:
#                 filter_df = filter_df


#             st.dataframe(filter_df)


import pandas as pd
import streamlit as st
from Home import face_rec
import datetime

st.set_page_config(layout='wide')
st.subheader('Reporting')

# Retrieve logs data and show in Report.py
name = 'attendance:logs'
def load_logs(name, end=-1):
    logs_list = face_rec.r.lrange(name, start=0, end=end)  # extract all data from the Redis database
    return logs_list

# Retrieve registered data
registered_data = face_rec.retrive_data(name='academy:register')

# All possible combinations of dates, names, and roles
name_role = registered_data[['Name', 'Role']].drop_duplicates()

# Generate dates range based on the existing logs
logs_list = load_logs(name=name)
convert_byte_to_string = lambda x: x.decode('utf-8')
logs_list_string = list(map(convert_byte_to_string, logs_list))
split_string = lambda x: x.split('@')
logs_nested_list = list(map(split_string, logs_list_string))
logs_df = pd.DataFrame(logs_nested_list, columns=['Name', 'Role', 'Timestamp'])
logs_df['Timestamp'] = logs_df['Timestamp'].apply(lambda x: x.split('.')[0])
logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
logs_df['Date'] = logs_df['Timestamp'].dt.date

# All possible dates in the logs
all_dates = pd.date_range(start=logs_df['Date'].min(), end=logs_df['Date'].max(), freq='D').date

# Create a DataFrame with all combinations of dates, names, and roles
date_name_role_zip = []
for dt in all_dates:
    for name, role in name_role.values:
        date_name_role_zip.append([dt, name, role])

date_name_role_zip_df = pd.DataFrame(date_name_role_zip, columns=['Date', 'Name', 'Role'])

# Merge with logs_df to get timestamps and determine presence
merged_df = pd.merge(date_name_role_zip_df, logs_df, how='left', on=['Date', 'Name', 'Role'])

# Function to determine status based on presence in logs
def status_marker(x):
    if pd.Series(x).isnull().all():
        return 'Absent'
    else:
        return 'Present'

# Apply status marker function
merged_df['Status'] = merged_df['Timestamp'].apply(status_marker)

# Pivot the data to have dates as columns and names as rows
pivot_df = merged_df.pivot_table(index=['Name', 'Role'], columns='Date', values='Status', aggfunc='first', fill_value='Absent')

# Reset index to add a serial number column
pivot_df = pivot_df.reset_index()
pivot_df.index += 1  # Start index from 1
pivot_df.index.name = 'Serial No.'

# Display buttons for Attendance Report, Student Search, and Student Filter side by side
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Show Attendance Report'):
        st.dataframe(pivot_df)

with col2:
    if st.button('Student Search'):
        st.subheader('Student Search')
        search_name = st.text_input('Search by Student Name')
        if st.button('Search'):
            if search_name:
                student_data = merged_df[merged_df['Name'].str.contains(search_name, case=False)]
                if not student_data.empty:
                    st.write(f"Attendance details for '{search_name}':")
                    st.dataframe(student_data[['Name', 'Role', 'Date', 'Status']])
                else:
                    st.write(f"No attendance records found for '{search_name}'.")

with col3:
    if st.button('Filter Students'):
        st.subheader('Student Filter')
        date_in = str(st.date_input('Filter Date', datetime.datetime.now().date()))
        name_list = merged_df['Name'].unique().tolist()
        name_in = st.selectbox('Select Name', ['ALL'] + name_list)
        role_list = merged_df['Role'].unique().tolist()
        role_in = st.selectbox('Select Role', ['ALL'] + role_list)
        status_list = ['Absent', 'Present']
        status_in = st.multiselect('Select the Status', ['ALL'] + status_list)

        if st.button('Filter'):
            filter_df = merged_df.copy()
            filter_df['Date'] = filter_df['Date'].astype(str)

            if date_in != 'ALL':
                filter_df = filter_df.query(f'Date == "{date_in}"')

            if name_in != 'ALL':
                filter_df = filter_df.query(f'Name == "{name_in}"')

            if role_in != 'ALL':
                filter_df = filter_df.query(f'Role == "{role_in}"')

            if 'ALL' not in status_in:
                filter_df = filter_df[filter_df['Status'].isin(status_in)]

            filter_pivot_df = filter_df.pivot_table(index=['Name', 'Role'], columns='Date', values='Status', aggfunc='first', fill_value='Absent')
            filter_pivot_df = filter_pivot_df.reset_index()
            filter_pivot_df.index += 1
            filter_pivot_df.index.name = 'Serial No.'

            st.dataframe(filter_pivot_df)








