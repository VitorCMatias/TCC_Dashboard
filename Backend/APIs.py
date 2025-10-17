import numpy as np
import pandas as pd
import streamlit as st


class APIs():
    def __init__(self, db_name:str='mock_data'):
        self.db_connection = st.connection(db_name, type='sql',ttl=10)

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
    
    def calculate_acceleration(self, df: pd.DataFrame, time_colum: str = 'timestamp', speed_solum: str = 'speed') -> pd.DataFrame:
        """
        Calcula a aceleração a partir de um DataFrame contendo valores de velocidade.

        :param df: Um DataFrame com as colunas 'timestamp', 'speed'.
        :param time_colum:  Coluna do dataframe contendo os valores de tempo.
        :param speed_solum: Coluna do dataframe contendo os valores de velocidade.
        
        :return: O dataframe original contendo as colunas de aceleração adicionadas a ele.
        """

        df[time_colum] = pd.to_datetime(df[time_colum])
        df['time_interval_s'] = (df[time_colum] - df[time_colum].shift(1)).dt.total_seconds()
        df['acceleration'] = (df[speed_solum] - df[speed_solum].shift(1)) / df['time_interval_s']

        df.drop(columns=['time_interval_s'], inplace=True)
        df.dropna(subset=['acceleration'], inplace=True)

        return df


    def get_position(self, df):
        position = df[['latitude', 'longitude']].apply(tuple, axis=1)
        return position.iloc[0]
