import folium
import matplotlib.pyplot as plt


class GPS:
    def __init__(self):
        self.map = folium.Map(location=[51.420833, -0.070000], zoom_start=15)
        self.figure = folium.FeatureGroup(name="Car Position")
        self.loc = ()

    def get_map(self):
        return self.map

    def position_update(self, coordinate: tuple):
        self.figure.add_child(
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
        self.loc = coordinate

        return self.figure

    def get_locations(self):
        return self.loc

    def __velocity_to_color(self, value, max_velocity=80):
        normalized_value = value / max_velocity
        colormap = plt.get_cmap("coolwarm")
        rgb_color = colormap(normalized_value)
        hex_color = '#%02x%02x%02x' % (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

        return hex_color

    def heat_map(self, data):
        fig = folium.FeatureGroup(name="Position")

        for i in range(len(data)):
            fig.add_child(
                folium.CircleMarker
                    (
                    location=(data[i][0], data[i][1]),
                    radius=3,
                    opacity=0.7,
                    color=self.__velocity_to_color(data[i][2]),
                    fill=True,
                    fill_opacity=0.7,
                )
            )
        return fig
