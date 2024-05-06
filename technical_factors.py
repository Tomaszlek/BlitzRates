import pandas_ta as ta
import pandas as pd
import database_queries as db


def transform_currency_data_to_pandas(currency_code):
    data = db.get_currency_data(currency_code)
    df = pd.DataFrame(data, columns=['effectiveDate', 'mid'])
    df = df.rename(columns={'effectiveDate': 'Date', 'mid': 'Rate'})

    return df


def transform_gold_data_to_pandas():
    data = db.get_gold_data()
    df = pd.DataFrame(data, columns=['data', 'cena'])
    df = df.rename(columns={'data': 'Date', 'cena': 'Rate'})

    return df


def moving_average(data, period_of_time):
    data['Moving Average'] = ta.sma(data['Rate'], length=period_of_time)
    return data


def relative_strength_index(data, period_of_time):
    data['RSI'] = ta.rsi(data['Rate'], length=period_of_time, append=True)  # RSI (Indeks siły względnej)
    return data


def bollinger_bands(data, period_of_time, std_deviation):
    bands = ta.bbands(data['Rate'], length=period_of_time, std=std_deviation, append=True)
    data['Bollinger Bands Lower'] = bands.iloc[:, 0]  # Kolumna dolnego pasma Bollingera
    data['Bollinger Bands Upper'] = bands.iloc[:, 2]  # Kolumna górnego pasma Bollingera
    return data
