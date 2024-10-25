import time

import streamlit as st
from streamlit_folium import st_folium

from Backend import APIs
from Frontend import GPS, Sidebar, bar_plot, line_plot

# TODO
# - Criar o painel lateral de configuração




st.cache_data.clear()

st.set_page_config(layout='wide',
                   page_title='CAN-Monitor',
                   page_icon=':zap:')

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.html(hide_decoration_bar_style)

st.title('CAN-Monitor Dashboard')
st.write('---')


refresh_frequency = 2
auto_refresh = True

db_data = APIs()
car_map = GPS((-6.22444, 106.867111),zoom=10)

Sidebar.show(auto_refresh,refresh_frequency)
    

positions = db_data.get_previous_positions()
query_car_current_position = db_data.get_current_position()
speed_sample = db_data.get_sample_speed()
car_current_position = db_data.get_position(query_car_current_position)

df_acelletation = db_data.calculate_acceleration(speed_sample)


st_data = st_folium(
    car_map.get_map(),
    feature_group_to_add=[car_map.heat_map(positions), car_map.position_update(car_current_position)],
    height=400,
    width=700*2,
)

st.plotly_chart(
    line_plot(df_acelletation, 'timestamp', 'speed', y2='acceleration', title='Acelração e velocidade'),
    use_container_width=True)

plot1, plot2 = st.columns(2)

with plot1:
    st.plotly_chart(
        bar_plot(df_acelletation, 'timestamp', 'speed', title='Velocidade em km/h', unit_of_measurement='km/h'),
        use_container_width=True)


with plot2:
    st.plotly_chart(
    bar_plot(df_acelletation, 'timestamp', 'acceleration', title='Aceleração em km/h²'),
    use_container_width=True)


st.dataframe(db_data.car_flags().head(1), use_container_width=True,hide_index=True)

all_data = db_data.get_all()
all_data = db_data.calculate_acceleration(all_data)


st.dataframe(all_data,use_container_width=True,hide_index=True)


if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
