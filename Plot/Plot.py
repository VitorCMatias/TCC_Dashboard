import numpy as np
from plotly import express as px
from plotly.graph_objects import Figure
from typing import Optional

def __add_mean_horizontal_line(fig: Figure, values:list, horizontal_line_annotation:str='', unit_of_measurement:str=''):
    """
    Adiciona uma linha horizontal ao gráfico Plotly Express representando a média dos valores fornecidos.

    @param fig: A figura Plotly Express onde a linha horizontal será adicionada.
    @param values: Uma lista ou array-like contendo os valores para os quais deseja-se calcular a média.
    @param horizontal_line_annotation: Uma string que será adicionada como anotação à linha horizontal,
      geralmente para fornecer contexto sobre o que a linha representa (por exemplo, 'Média', 'Limite', etc.).
      O padrão é uma string vazia.
    @param unit_of_measurement: Uma string que representa a unidade de medida dos valores fornecidos.
      Essa unidade será exibida na anotação da linha horizontal. O padrão é uma string vazia.

    """

    y_mean = np.mean(values)

    fig.add_hline(y=y_mean,
                        line_dash='dot',
                        annotation_text=f'{horizontal_line_annotation} {y_mean:.2f}{unit_of_measurement}',
                        annotation_position='top right',
                        line_color='#989898',
                        opacity=0.5
                        )



def bar_plot(data,
             x: str,
             y: str,
             title: str,
             horizontal_line_annotation: str = '',
             mean_annotation: bool = True,
             unit_of_measurement: str = '')->Figure:
    """
     Gera um gráfico de barras, e informa em uma linha tracejada a média da série fornecida.

     @param data: O conjunto de dados a ser utilizado para gerar o gráfico.
     @param x: O nome da coluna que contém os valores do eixo x.
     @param y: O nome da coluna que contém os valores do eixo y.
     @param title: O título do gráfico.
     @param horizontal_line_annotation: Uma string opcional a ser adicionada à anotação da linha horizontal.
     @param mean_annotation: Indica se uma linha horizontal representando a média de y deve ser adicionada ao gráfico.
     @param unit_of_measurement: A unidade de medida para ser exibida nas anotações.

    @return: Um objeto Figure contendo o gráfico de barras gerado.
     """


    bar_plot_figure = px.bar(data, x=x, y=y, title=title, color_discrete_sequence=['#ffc72c'])

    if mean_annotation:
        __add_mean_horizontal_line(bar_plot_figure, data[y], horizontal_line_annotation, unit_of_measurement)

    return bar_plot_figure


def line_plot(data,
               x: str,
               y1: str,
               y2: Optional[str],
               title: str = '',
               y1_mean_annotation: bool = True,
               y2_mean_annotation: bool = True,
               unit_of_measurement_y1: str = '',
               unit_of_measurement_y2: str = '')->Figure:

    """
    Gera um gráfico de linha, e informa  a média da série fornecida.

    @param data: O conjunto de dados a ser utilizado para gerar o gráfico.
    @param x: O nome da coluna que contém os valores do eixo x.
    @param y1: O nome da coluna que contém os valores do primeiro eixo y.
    @param y2: O nome da coluna que contém os valores do segundo eixo y.
    @param title: O título do gráfico.
    @param y1_mean_annotation: Uma string opcional a ser adicionada à anotação da linha horizontal de y1.
    @param y2_mean_annotation: Uma string opcional a ser adicionada à anotação da linha horizontal de y2.
    @param mean_annotation: Indica se uma linha horizontal representando a média de y deve ser adicionada ao gráfico.
    @param unit_of_measurement_y1: A unidade de medida para ser exibida nas anotações de y1.
    @param unit_of_measurement_y2: A unidade de medida para ser exibida nas anotações de y2.

    @return: Um objeto Figure contendo o gráfico de barras gerado.
    """
    
    if y2:
        fig = px.line(data, x=x, y=[y1,y2], title=title,markers=True, symbol_map={y1: 'circle-open', y2: 'circle-x'}, color_discrete_map={y1: '#ffc72c', y2: '#808080'})
    else:
        fig = px.line(data, x=x, y=[y1], title=title,markers=True, symbol_map={y1: 'circle-open'}, color_discrete_map={y1: '#ffc72c'})

    if y1_mean_annotation:
        __add_mean_horizontal_line(fig, data[y1], f'média {y1}', unit_of_measurement_y1)

    if y2_mean_annotation:
        __add_mean_horizontal_line(fig, data[y2], f'média {y2}', unit_of_measurement_y2)

    return fig
