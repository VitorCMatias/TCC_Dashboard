import streamlit as st
from streamlit_folium import st_folium
import time
from Map import GPS
import mock_data
import plotly.express as px
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
db_connection = st.connection('mock_data', type='sql',ttl=10)


with db_connection.session as db_session:
    new_data = mock_table(timestamp=df_front.gps_datetime, latitude=df_front.latitude, longitude=df_front.longitude, speed=df_front.speed)
    db_session.add(new_data)
    db_session.commit()

car_map = GPS((-6.22444, 106.867111))

positions = db_connection.query('SELECT latitude, longitude, speed FROM mock_table')
query_car_current_position = db_connection.query('SELECT latitude, longitude FROM mock_table WHERE id = (SELECT MAX(id) FROM mock_table)')
car_current_position = get_position(query_car_current_position)


st_data = st_folium(
    car_map.get_map(),
    feature_group_to_add=[car_map.heat_map(positions), car_map.position_update(car_current_position)],
    height=400,
    width=700,
)


q = db_connection.query('select timestamp, speed from mock_table')
fig = px.bar(q, x='timestamp', y='speed')

st.plotly_chart(fig, use_container_width=True)


auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
