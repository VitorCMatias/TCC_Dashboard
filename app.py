import numpy as np
import streamlit as st
from streamlit_folium import st_folium
import time
from Map import GPS
import plotly.express as px
import pandas as pd
from Mock import Mock


def calculate_acceleration(df: pd.DataFrame) -> pd.Series:
    """
    Calculates acceleration from a DataFrame containing speed values.

    Args:
        df (pd.DataFrame): A DataFrame with columns 'timestamp', 'speed' (in km/h).

    Returns:
        pd.Series: A Series containing acceleration values (in km/h^2).
    """
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['time_interval_s'] = (df['timestamp'] - df['timestamp'].shift(1)).dt.total_seconds()
    df['acceleration'] = (df['speed'] - df['speed'].shift(1)) / df['time_interval_s']

    return df



def get_position(df):
    position = df[['latitude', 'longitude']].apply(tuple, axis=1)
    return position.iloc[0]



st.cache_data.clear()

mock = Mock()
mock.add()

positions = mock.get_previous_positions()
query_car_current_position = mock.get_current_position()

car_map = GPS((-6.22444, 106.867111))
car_current_position = get_position(query_car_current_position)


st_data = st_folium(
    car_map.get_map(),
    feature_group_to_add=[car_map.heat_map(positions), car_map.position_update(car_current_position)],
    height=400,
    width=700,
)

speed_sample = mock.get_sample_speed()

mean_velocity = np.mean(speed_sample['speed'])
fig = px.bar(speed_sample, x='timestamp', y='speed', title='Speed')
fig.add_hline(y=mean_velocity, line_dash='dot', annotation_text=f'{mean_velocity:.2f}km/h', annotation_position='top right')


st.plotly_chart(fig, use_container_width=True)

fig_acel = px.bar(calculate_acceleration(speed_sample), x='timestamp', y='acceleration', title='acceleration')

st.plotly_chart(fig_acel, use_container_width=True)

st.dataframe( mock.get_all())

auto_refresh = True
refresh_frequency = 2
if auto_refresh:
    time.sleep(refresh_frequency)
    st.rerun()
