import pandas as pd
import streamlit as st
from DB import mock_table
import numpy as np

class Mock:
    db_connection = None
    df = pd.read_csv('GPS_info.csv')

    def __init__(self):
        self.db_connection = st.connection('mock_data', type='sql',ttl=10)

    def __mocked_data(self, index: int):
        return self.df.iloc[index]


    def __mock_gps_session_state(self):
        if 'GPS_index' not in st.session_state:
            st.session_state['GPS_index'] = 0


    def __get_mock_gps_session_state(self):
        return st.session_state['GPS_index']


    def __mock_gps_session_state_update(self):
        if st.session_state['GPS_index'] < 4700:
            st.session_state['GPS_index'] = st.session_state['GPS_index'] + 1
        else:
            st.session_state['GPS_index'] = 0

    def add(self):
        self.__mock_gps_session_state()
        data = self.__mocked_data(self.__get_mock_gps_session_state())

        with self.db_connection.session as db_session:
            new_data = mock_table(timestamp=data.gps_datetime, latitude=data.latitude, longitude=data.longitude, speed=data.speed)
            db_session.add(new_data)
            db_session.commit()
    
        self.__mock_gps_session_state_update()

    def get_previous_positions(self):
        return self.db_connection.query('SELECT latitude, longitude, speed FROM mock_table')
        

    def get_current_position(self):
        return self.db_connection.query('SELECT latitude, longitude FROM mock_table WHERE id = (SELECT MAX(id) FROM mock_table)')
    

    def get_sample_speed(self):
        return self.db_connection.query('select timestamp, speed from mock_table')

    def get_all(self):
        return self.db_connection.query('SELECT * FROM mock_table')


    def car_flags(self):
        colunas = ['apps', 'bppc', 'buzzer', 'breaklight', 'inv_break', 
            'botao_partida', 'shutdown1', 'shutdown2', 'shutdown3', 
            'inversor_direito', 'inversor_esquerdo']

        # Gerando valores booleanos aleatórios para cada coluna
        dados = np.random.choice([True, False], size=(10, len(colunas)))

        # Criando o DataFrame
        df = pd.DataFrame(dados, columns=colunas)

        # Exibindo o DataFrame
        return df