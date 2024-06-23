import streamlit as st
import pandas as pd
import time



# @st.cache
# def get_data_from_database():
#     db_connection = st.connection('mock_data', type='sql',ttl=10)
#     data = db_connection.query('SELECT * FROM mock_table')
#     return data


st.cache_data.clear()

st.title("GPS Data Dashboard")


db_connection = st.connection('mock_data', type='sql',ttl=10)
data = db_connection.query('SELECT * FROM mock_table')
# data = get_data_from_database
st.write(data)

auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
