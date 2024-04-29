import folium
import matplotlib.pyplot as plt


class GPS:
    '''
    Módulo responsável por construir os objetos de Mapa na dashboard principal, e a gerenciar os dados presentes nele.
    '''
    def __init__(self):
        self.position = (51.420833, -0.070000)
        self.map = folium.Map(location=self.position, zoom_start=15)

        self.figure = folium.FeatureGroup(name="Car Position")

    def get_map(self) -> folium.Map:
        return self.map

    def position_update(self, coordinate: tuple) -> folium.map.FeatureGroup:
        '''
        Função para atualizar a posição do mapa

        @param coordinate: Tupla com os valores das coordenadas do carro.
        @return: Canva com a posição do carro.
        '''
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

    def __velocity_to_color(self, value: float, upper_bound: float = 80) -> str:
        '''
        Mapeia um valor informado em uma escala de cor hexadecimal

        @param value: O valor que será mapeado em código de cor.
        @param upper_bound: O valor máximo do intervalo que será normalizado para uma escala de 255.
        @return: Retorna o código de cores do valor inserido no parâmetro.
        '''
        normalized_value = value / upper_bound
        colormap = plt.get_cmap("coolwarm")
        rgb_color = colormap(normalized_value)
        hex_color = '#%02x%02x%02x' % (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

        return hex_color

    def heat_map(self, car_data: list) -> folium.map.FeatureGroup:
        '''
        Cria um mapa de calor utilizando as posições do veículo.

        @param car_data: informações a respeito do carro, uma tupla (latitude, longitude) e a velocidade.
        @return: canva com as posições antigas do carro, pintadas de acordo com a velocidade, quanto mais quente a cor
         mais rápido o carro estava.
        '''

        heatmap = folium.FeatureGroup(name="Position")

        for coordinate, velocity in car_data:
            heatmap.add_child(
                folium.CircleMarker
                (
                    location=coordinate,
                    radius=3,
                    opacity=0.7,
                    color=self.__velocity_to_color(velocity),
                    fill=True,
                    fill_opacity=0.7,
                )
            )

        return heatmap
