import pandas as pd
import numpy as np

def get_coordinates(num_passos = 50):
    # Define as coordenadas iniciais (latitude e longitude) dentro do Crystal Palace Park
    latitude_inicial = 51.420833  # 51°25'15"N
    longitude_inicial = -0.070000  # 0°04'12"W

    # Gerar 50 passos aleatórios (simulando uma caminhada)
    tamanho_passo = 0.004  # Ajuste o tamanho do passo conforme necessário

    # Gerar passos aleatórios para latitude e longitude
    passos_latitude = np.random.uniform(-tamanho_passo, tamanho_passo, num_passos)
    passos_longitude = np.random.uniform(-tamanho_passo, tamanho_passo, num_passos)

    # Inicializar listas vazias para armazenar as coordenadas
    lista_latitude = [latitude_inicial]
    lista_longitude = [longitude_inicial]

    # Gerar as coordenadas
    for i in range(num_passos):
        nova_latitude = lista_latitude[-1] + passos_latitude[i]
        nova_longitude = lista_longitude[-1] + passos_longitude[i]
        lista_latitude.append(nova_latitude)
        lista_longitude.append(nova_longitude)


    lista_latitude.pop(0)
    lista_longitude.pop(0)

    

    # Criar um DataFrame com as coordenadas
    df_coordenadas = pd.DataFrame({
        'latitude': lista_latitude,
        'longitude': lista_longitude
    })

    return df_coordenadas

