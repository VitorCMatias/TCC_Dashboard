import streamlit as st
from streamlit_folium import st_folium
import time
from Map import GPS
import pandas as pd
from Mock import Mock
from Plot.Plot import bar_plot, line_plot


def calculate_acceleration(df: pd.DataFrame, time_colum: str = 'timestamp', speed_solum: str = 'speed') -> pd.DataFrame:
    """
    Calcula a aceleração a partir de um DataFrame contendo valores de velocidade.

    @param df: Um DataFrame com as colunas 'timestamp', 'speed'.
    @param time_colum:  Coluna do dataframe contendo os valores de tempo.
    @param speed_solum: Coluna do dataframe contendo os valores de velocidade.
    @return: O dataframe original contendo as colunas de aceleração adicionadas a ele.
    """

    df[time_colum] = pd.to_datetime(df[time_colum])
    df['time_interval_s'] = (df[time_colum] - df[time_colum].shift(1)).dt.total_seconds()
    df['acceleration'] = (df[speed_solum] - df[speed_solum].shift(1)) / df['time_interval_s']

    df.drop(columns=['time_interval_s'], inplace=True)
    df.dropna(subset=['acceleration'], inplace=True)

    return df


def get_position(df):
    position = df[['latitude', 'longitude']].apply(tuple, axis=1)
    return position.iloc[0]


st.cache_data.clear()

mock = Mock()
mock.add()

positions = mock.get_previous_positions()
query_car_current_position = mock.get_current_position()
speed_sample = mock.get_sample_speed()

car_current_position = get_position(query_car_current_position)


car_map = GPS((-6.22444, 106.867111),zoom=10)

st_data = st_folium(
    car_map.get_map(),
    feature_group_to_add=[car_map.heat_map(positions), car_map.position_update(car_current_position)],
    height=400,
    width=700*2,
)

df_acelletation = calculate_acceleration(speed_sample)

st.plotly_chart(
    bar_plot(df_acelletation, 'timestamp', 'speed', title='Velocidade em km/h', unit_of_measurement='km/h'),
    use_container_width=True)

st.plotly_chart(
    bar_plot(df_acelletation, 'timestamp', 'acceleration', title='Aceleração em km/h²'),
    use_container_width=True)

st.plotly_chart(
    line_plot(df_acelletation, 'timestamp', 'speed', y2='acceleration'),
    use_container_width=True)



st.dataframe(df_acelletation)

auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
