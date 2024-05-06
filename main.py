import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import sqlite3
import database_queries as db
import api_requests as api
import charts

external_stylesheets = list('style.css')

# Connection with database
conn = sqlite3.connect('kursy_walut.db')

db.create_rates_table(conn)
db.create_gold_rate_table(conn)

# Getting rates from Polish National Bank API
currency_rates = api.get_currencies_rates()
gold_rate = api.get_gold_rate()

db.insert_currency_rates_into_database(conn, currency_rates)
db.insert_gold_rate_into_database(conn, gold_rate)

currency_codes = db.get_unique_currencies(conn)
conn.close()

# Dash initialization
app = dash.Dash(__name__, title='BlitzRates')

options = [{'label': f'{currency_name} ({currency_code})', 'value': currency_code}
           for (currency_name, currency_code) in currency_codes]


app.layout = html.Div([
    html.Link(
                   rel='stylesheet',
                   href='/assets/style.css'
               ),
    html.Img(src='assets/logo.png', className='logo'),
    html.H1('BlitzRates', id='title', style={'display': 'none'}),
    
    html.Div([

        html.Div([
            html.H2('Dostępne waluty ', className='subtitle'),
            dcc.Dropdown(
                id='currency-choice',
                options=options, style={'color': '#FFFFFF'},
                value='USD'
            ),
            html.H2('Dostępne wskaźniki analizy technicznej ', className='subtitle'),
            html.Div([
                html.Label('Średnia krocząca', className='label', id='ma-currency-label'),
                dcc.RadioItems(
                    id='moving-average-currency',
                    options=[
                        {'label': 'Brak', 'value': 0},
                        {'label': '3-dniowa', 'value': 3},
                        {'label': '7-dniowa', 'value': 7},
                        {'label': '14-dniowa', 'value': 14}
                    ],
                    value=0,
                    labelStyle={'display': 'block'}
                ),
                html.Div([
                    html.P("Średnia krocząca to średnia wartość kursu waluty w określonym okresie czasu. "
                           "Może być wykorzystywana do identyfikacji trendów, zwłaszcza gdy jest stosowana z "
                           "różnymi okresami czasowymi."),
                ], className='description', id='ma-currency-description', style={'display': 'none'})
            ], className='radio-container'),

            html.Div(id='technical-indicator-container-currency', children=[
                html.Label('Pozostałe wskaźniki', className='label'),
                dcc.RadioItems(
                    id='technical-indicator-currency',
                    options=[
                        {'label': 'Brak wskaźnika', 'value': ''},
                        {'label': 'RSI', 'value': 'RSI'},
                        {'label': 'Wstęgi Bollingera', 'value': 'Bollinger Bands'}
                    ],
                    value='',
                    labelStyle={'display': 'block'}
                ),
                html.Div([
                    html.P("RSI (Relative Strength Index) to wskaźnik, który mierzy prędkość i zmianę "
                           "zmian cen waluty. Wartości RSI powyżej 70 oznaczają, że waluta jest przekupiona(dobra okazja do sprzedaży), "
                           "podczas gdy wartości poniżej 30 wskazują na niedokupienie(dobra okazja do zakupu)."),
                ], className='description', id='rsi-currency-description', style={'display': 'none'}),
                html.Div([
                    html.P("Wstęgi Bollingera to wskaźnik, który pomaga określić zakres, w którym ceny waluty mogą się "
                           "poruszać i potencjalne poziomy wsparcia i oporu."),
                ], className='description', id='bollinger-currency-description', style={'display': 'none'})
            ])
        ], className='column1'),


        html.Div([
            dcc.Graph(id='currency-rate-chart')
        ], className='column2')

    ], className='row'),


    html.Div([

        html.Div([
            html.H2('Cena złota ', className='subtitle'),
            html.Div([
                html.Label('Średnia krocząca', className='label', id='ma-gold-label'),
                dcc.RadioItems(
                    id='moving-average-gold',
                    options=[
                        {'label': 'Brak', 'value': 0},
                        {'label': '3-dniowa', 'value': 3},
                        {'label': '7-dniowa', 'value': 7},
                        {'label': '14-dniowa', 'value': 14}
                    ],
                    value=0,  # Domyślnie 3-dniowa
                    labelStyle={'display': 'block'}
                ),
                html.Div([
                    html.P("Średnia krocząca dla ceny złota to średnia wartość ceny złota w określonym "
                           "okresie czasu. Może być używana do identyfikacji trendów cen złota, zwłaszcza gdy jest"
                           "wykorzystywana z różnymi przedziałami czasu"),
                ], className='description', id='ma-gold-description', style={'display': 'none'})
            ], className='radio-container'),

            html.Div(id='technical-indicator-container-gold', children=[
                html.Label('Pozostałe wskaźniki', className='label'),
                dcc.RadioItems(
                    id='technical-indicator-gold',
                    options=[
                        {'label': 'Brak wskaźnika', 'value': ''},
                        {'label': 'RSI', 'value': 'RSI'},
                        {'label': 'Wstęgi Bollingera', 'value': 'Bollinger Bands'}
                    ],
                    value='',
                    labelStyle={'display': 'block'}
                ),
                html.Div([
                    html.P("RSI (Relative Strength Index) dla ceny złota to wskaźnik, który mierzy "
                           "prędkość i zmianę zmian cen złota. Wartości RSI powyżej 70 oznaczają, że złoto jest "
                           "przekupione(dobra okazja do sprzedaży, podczas gdy wartości poniżej 30 wskazują na niedokupienie(dobra okazja do zakupu."),
                ], className='description', id='rsi-gold-description', style={'display': 'none'}),
                html.Div([
                    html.P("Wstęgi Bollingera dla ceny złota to wskaźnik, który pomaga określić zakres,"
                           "w którym ceny złota mogą się poruszać i potencjalne poziomy wsparcia i oporu."),
                ], className='description', id='bollinger-gold-description', style={'display': 'none'})
            ])
        ], className='column1'),

        html.Div([
            dcc.Graph(id='gold-rate-chart')
        ], className='column2')

    ], className='row')

], className='container')


# Called when choosing another currency
@app.callback(
    Output('currency-rate-chart', 'figure'),
    [Input('currency-choice', 'value')],
    [Input('moving-average-currency', 'value')],
    [Input('technical-indicator-currency', 'value')]
)
def update_currency_chart(currency_code, moving_average_period, indicator):
    return charts.plot_currency_chart(currency_code, moving_average_period, indicator)


@app.callback(
    Output('gold-rate-chart', 'figure'),
    [Input('currency-choice', 'value')],
    [Input('moving-average-gold', 'value')],
    [Input('technical-indicator-gold', 'value')]
)
def update_gold_chart(currency_code, moving_average_period, indicator):
    return charts.plot_gold_chart(moving_average_period, indicator)


@app.callback(
    Output('ma-currency-description', 'style'),
    [Input('moving-average-currency', 'value')]
)
def toggle_ma_currency_description(value):
    if value != 0:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('rsi-currency-description', 'style'),
    [Input('technical-indicator-currency', 'value')]
)
def toggle_rsi_currency_description(value):
    if value == 'RSI':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('bollinger-currency-description', 'style'),
    [Input('technical-indicator-currency', 'value')]
)
def toggle_bollinger_currency_description(value):
    if value == 'Bollinger Bands':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('ma-gold-description', 'style'),
    [Input('moving-average-gold', 'value')]
)
def toggle_ma_gold_description(value):
    if value != 0:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('rsi-gold-description', 'style'),
    [Input('technical-indicator-gold', 'value')]
)
def toggle_rsi_gold_description(value):
    if value == 'RSI':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('bollinger-gold-description', 'style'),
    [Input('technical-indicator-gold', 'value')]
)
def toggle_bollinger_gold_description(value):
    if value == 'Bollinger Bands':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
