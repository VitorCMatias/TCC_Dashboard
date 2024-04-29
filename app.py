import streamlit as st
from streamlit_folium import st_folium
from coord import get_coordinates
import time
from Map import GPS
import mock_data
import plotly.express as px
import numpy as np
from DB import mock_table

'''
TODO
    - Tentar usar filas ou pilha ao invés de lista, colocar os dados que chegam em uma fila o primeiro item é a
     localização atual e os demais vão para o heatmap.
'''


def get_position(df):
    position = df[['latitude', 'longitude']].apply(tuple, axis=1)
    return position.iloc[0]

def get_velocity(df):
    return df.speed.item()


def get_date(df):
    return df.gps_datetime


df_front = mock_data.get()

st.cache_data.clear()
conn = st.connection('mock_data', type='sql',ttl=10)


with conn.session as s:
    new_data = mock_table(timestamp=df_front.gps_datetime, latitude=df_front.latitude, longitude=df_front.longitude, speed=df_front.speed)
    s.add(new_data)
    s.commit()

car_map = GPS((-6.22444, 106.867111))

# if 'car_data' not in st.session_state:
#     st.session_state['car_data'] = []

# position = get_position(df_front)
# speed = get_velocity(df_front)
# timestamp = get_date(df_front)

# st.session_state['car_data'].append([timestamp, position, speed])


# car_data = st.session_state['car_data']

query = conn.query('SELECT latitude, longitude, speed FROM mock_table')
q2 = conn.query('SELECT latitude, longitude FROM mock_table WHERE id = (SELECT MAX(id) FROM mock_table)')
position2 = get_position(q2)

# st.write(position2)

st_data = st_folium(
    car_map.get_map(),
    feature_group_to_add=[car_map.heat_map(query), car_map.position_update(position2)],
    height=400,
    width=700,
)
q = conn.query('select timestamp, speed from mock_table')
fig = px.bar(q, x='timestamp', y='speed')

st.plotly_chart(fig, use_container_width=True)


auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
