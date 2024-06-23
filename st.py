import streamlit as st

import time
from Backend import APIs



st.cache_data.clear()

st.title("GPS Data Dashboard")

backend_data = APIs()
data = backend_data.get_all()
# db_connection = st.connection('mock_data', type='sql',ttl=10)
# data = db_connection.query('SELECT * FROM mock_table')
st.write(data)

auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
