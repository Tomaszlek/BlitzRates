import plotly.graph_objects as go
import technical_factors as tf


def plot_currency_chart(currency_code, ma_period, indicator):
    currency_df = tf.transform_currency_data_to_pandas(currency_code)

    if indicator == 'RSI':
        currency_df = tf.relative_strength_index(currency_df, ma_period)
    elif indicator == 'Bollinger Bands':
        currency_df = tf.bollinger_bands(currency_df, 20, 2)  # Ustawiamy standardowe odchylenie na 2

    fig = go.Figure()

    if ma_period != 0:
        currency_df = tf.moving_average(currency_df, ma_period)

        fig.add_trace(go.Scatter(x=currency_df['Date'], y=currency_df['Moving Average'],
                             mode='lines', line=dict(dash='dot'), name=f'{ma_period}-dniowa średnia krocząca'))

    if indicator == '':
        fig.add_trace(go.Scatter(x=currency_df['Date'], y=currency_df['Rate'],
                                 mode='lines', marker=dict(color='#4a98d4'), name=f'{currency_code}/PLN'))

        fig.update_layout(xaxis=dict(title='Data'),
                          yaxis=dict(title=f'Kurs({currency_code}/PLN)'),
                          title=f'Kurs ({currency_code}/PLN)',
                          template='plotly_dark',
                          font=dict(
                              family="Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', 'Nimbus Sans Narrow', sans-serif-condensed, sans-serif",
                              size=14)
                          )

    elif indicator == 'RSI':
        fig.add_trace(go.Scatter(x=currency_df['Date'], y=currency_df['RSI'],
                                 mode='lines', marker=dict(color='red'), name=f'RSI'))

        fig.update_layout(xaxis=dict(title='Data'),
                          yaxis=dict(title='RSI'),
                          title=f'RSI dla kursu {currency_code}/PLN',
                          template='plotly_dark',
                          font=dict(
                              family="Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', 'Nimbus Sans Narrow', sans-serif-condensed, sans-serif",
                              size=14)
                          )

    elif indicator == 'Bollinger Bands':
        fig.add_trace(go.Scatter(x=currency_df['Date'], y=currency_df['Rate'],
                                 mode='lines', marker=dict(color='#4a98d4'), name=f'{currency_code}/PLN'))
        fig.add_trace(go.Scatter(x=currency_df['Date'], y=currency_df['Bollinger Bands Upper'],
                                 mode='lines', line=dict(color='#a135c4' , dash = 'dot'), name=f'Górna wstęga Bollingera'))
        fig.add_trace(go.Scatter(x=currency_df['Date'], y=currency_df['Bollinger Bands Lower'],
                                 mode='lines', line=dict(color='orange' , dash = 'dot'), name=f'Dolna wstęga Bollingera'))

        fig.update_layout(xaxis=dict(title='Data'),
                          yaxis=dict(title=f'Kurs({currency_code}/PLN)'),
                          title=f'Kurs ({currency_code}/PLN) ze wstęgami Bollingera',
                          template='plotly_dark',
                          font=dict(
                              family="Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', 'Nimbus Sans Narrow', sans-serif-condensed, sans-serif",
                              size=14)
                          )
    return fig


def plot_gold_chart(ma_period, indicator):
    gold_df = tf.transform_gold_data_to_pandas()

    if indicator == 'RSI':
        gold_df = tf.relative_strength_index(gold_df, ma_period)
    elif indicator == 'Bollinger Bands':
        gold_df = tf.bollinger_bands(gold_df, 20, 2)  # Ustawiamy standardowe odchylenie na 2

    fig = go.Figure()

    if ma_period != 0:
        gold_df = tf.moving_average(gold_df, ma_period)

        fig.add_trace(go.Scatter(x=gold_df['Date'], y=gold_df['Moving Average'],
                             mode='lines', line=dict(color='gold', dash='dot'), name=f'{ma_period}-dniowa średnia krocząca'))

    if indicator == '':
        fig.add_trace(go.Scatter(x=gold_df['Date'], y=gold_df['Rate'],
                                 mode='lines', marker=dict(color='gold'), name='Cena złota za 1 g'))

        fig.update_layout(xaxis=dict(title='Data'),
                          yaxis=dict(title='Kurs złota(1 g)/PLN)'),
                          title=f'Cena złota za 1 g w PLN',
                          template='plotly_dark',
                          font=dict(
                              family="Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', 'Nimbus Sans Narrow', sans-serif-condensed, sans-serif",
                              size=14)
                          )

    elif indicator == 'RSI':
        fig.add_trace(go.Scatter(x=gold_df['Date'], y=gold_df['RSI'],
                                 mode='lines', line=dict(color='red'), name='RSI'))

        fig.update_layout(xaxis=dict(title='Data'),
                          yaxis=dict(title='RSI'),
                          title='RSI dla kursu złota',
                          template='plotly_dark',
                          font=dict(
                              family="Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', 'Nimbus Sans Narrow', sans-serif-condensed, sans-serif",
                              size=14)
                          )

    elif indicator == 'Bollinger Bands':
        fig.add_trace(go.Scatter(x=gold_df['Date'], y=gold_df['Rate'],
                                 mode='lines', line=dict(color='gold'), name='Cena złota za 1 g'))
        fig.add_trace(go.Scatter(x=gold_df['Date'], y=gold_df['Bollinger Bands Upper'],
                                 mode='lines', line=dict(color='#a135c4' , dash = 'dot'), name=f'Górna wstęga Bollingera'))
        fig.add_trace(go.Scatter(x=gold_df['Date'], y=gold_df['Bollinger Bands Lower'],
                                 mode='lines', line=dict(color='orange' , dash = 'dot'), name=f'Dolna wstęga Bollingera'))

        fig.update_layout(xaxis=dict(title='Data'),
                          yaxis=dict(title='Kurs złota(1 g)/PLN)'),
                          title='Cena złota za 1 g ze wstęgami Bollingera',
                          template='plotly_dark',
                          font=dict(
                              family="Bahnschrift, 'DIN Alternate', 'Franklin Gothic Medium', 'Nimbus Sans Narrow', sans-serif-condensed, sans-serif",
                              size=14),
                          )

    return fig
