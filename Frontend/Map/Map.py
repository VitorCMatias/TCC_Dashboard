import folium
import matplotlib.pyplot as plt
import pandas as pd


class GPS:
    """
    Módulo responsável por construir os objetos de Mapa na dashboard principal, e gerenciar os dados presentes nele.
    
    :param initial_position: Tupla com as coordenadas iniciais do mapa.
    :param zoom: Zoom do mapa.
    """
    def __init__(self, initial_position: tuple, zoom: int = 15):
        self.position = initial_position
        self.map = folium.Map(location=self.position, zoom_start=zoom, tiles="Cartodb Positron")

        self.figure = folium.FeatureGroup(name="Car Position")

    def get_map(self) -> folium.Map:
        """
        Retorna o mapa de coordenadas de um objeto de Mapa.

        :return: Objeto de Mapa
        """
        return self.map

    def position_update(self, coordinate: tuple) -> folium.map.FeatureGroup:
        """
        Função para atualizar a posição do mapa

        :param coordinate: Tupla com os valores das coordenadas do carro.
        :return: Canva com a posição do carro.
        """

        car_current_position = folium.FeatureGroup(name='Current Position')
        car_current_position.add_child(
            folium.CircleMarker
            (
                location=coordinate,
                radius=5,
                color='#808080',
                fill=True,
                fill_opacity=1,
                fill_color='#ffc72c'
            )
        )
        self.position = coordinate

        return car_current_position

    def get_position(self) -> tuple:
        return self.position

    def heat_map(self, car_data:pd.DataFrame, latitude:str='latitude', longitude:str='longitude', speed:str='speed') -> folium.map.FeatureGroup:
        """
        Cria um mapa de calor utilizando as posições do veículo.

        :param car_data: Dataframe com as posições antigas do carro e o parametro para mapa de calor.
        :param latitude: Nome da coluna com as latitudes do carro no dataframe.
        :param longitude: Nome da coluna com as longitudes do carro no dataframe.
        :param speed: Nome da coluna com as velocidades do carro no dataframe.
        :return: canva com as posições antigas do carro, pintadas de acordo com a velocidade, quanto mais quente a cor
         mais rápido o carro estava.
        """

        heatmap = folium.FeatureGroup(name="Position")


        for lat, lon,velocity in zip(car_data[latitude].values, car_data[longitude].values,car_data[speed].values):
            heatmap.add_child(
                folium.CircleMarker
                (
                    location=(lat,lon),
                    radius=3,
                    opacity=0.7,
                    color=velocity_to_color(velocity),
                    fill=True,
                    fill_opacity=0.7,
                )
            )

        return heatmap

def velocity_to_color(value: float, upper_bound: float = 51.0) -> str:
    """
    Mapeia um valor informado em uma escala de cor hexadecimal

    :param value: O valor que será mapeado em código de cor.
    :param upper_bound: O valor máximo do intervalo que será normalizado para uma escala de 255.
    :return: Retorna o código de cores do valor inserido no parâmetro.
    """
    normalized_value = value / upper_bound
    colormap = plt.get_cmap("jet") # coolwarm
    rgb_color = colormap(normalized_value)
    hex_color = '#%02x%02x%02x' % (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

    return hex_color
