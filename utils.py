import pandas as pd

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