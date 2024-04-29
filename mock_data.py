import pandas as pd
import streamlit as st


def mocked_data(index: int):
    df = pd.read_csv('GPS_info.csv')

    return df.iloc[index]


def mock_gps_session_state():
    if 'GPS_index' not in st.session_state:
        st.session_state['GPS_index'] = 0


def get_mock_gps_session_state():
    return st.session_state['GPS_index']


def mock_gps_session_state_update():
    if st.session_state['GPS_index'] < 4700:
        st.session_state['GPS_index'] = st.session_state['GPS_index'] + 1
    else:
        st.session_state['GPS_index'] = 0



def get():

    mock_gps_session_state()
    data = mocked_data(get_mock_gps_session_state())
    mock_gps_session_state_update()

    return data