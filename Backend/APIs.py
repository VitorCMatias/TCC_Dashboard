import streamlit as st
import numpy as np
import pandas as pd



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