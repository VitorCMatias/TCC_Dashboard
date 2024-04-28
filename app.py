import streamlit as st
from streamlit_folium import st_folium
from coord import get_coordinates
import time
from Map import GPS


'''
TODO
    - Aumentar a modularização do Map.py deixar o updade recebendo as coeedenadas x e y ou uma tupla
    - Deixar o mapa de calor recebendo uma lista de tuplas ou das coordenadas e das velocidades
    - Tentar usar filas ou pilha ao invés de lista, colocar os dados que chegam em uma fila o primeiro item é a
     localização atual e os demais vão para o heatmap.
'''

df_front = get_coordinates(1)
car_map = GPS()

if 'car_coordinates' not in st.session_state:
    st.session_state['car_coordinates'] = []

st.session_state['car_coordinates'].append(df_front.iloc[-1].tolist())

st_data = st_folium(
    car_map.get_map(),
    feature_group_to_add=[car_map.heat_map(st.session_state['car_coordinates']), car_map.update(df_front)],
    height=400,
    width=700,
)

auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
