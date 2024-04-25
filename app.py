import streamlit as st
from streamlit_folium import st_folium
from coord import get_coordinates
import time
from Map import GPS


df_front = get_coordinates(1)
car_map = GPS()

if 'dados' not in st.session_state:
    st.session_state['dados'] = []

st.session_state['dados'].append(df_front.iloc[-1].tolist())

st_data = st_folium(car_map.get_map(), 
    feature_group_to_add= [car_map.heat_map(st.session_state['dados']),car_map.update(df_front)],
    height=400*1.2,
    width=700*1.2,
)

auto_refresh = True
number  = 2
if auto_refresh:
    time.sleep(number)
    st.rerun()