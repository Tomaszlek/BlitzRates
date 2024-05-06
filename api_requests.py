import requests
from currency_rates import CurrencyRate, GoldRate


def get_currencies_rates():
    all_rates = []

    response = requests.get(f'http://api.nbp.pl/api/exchangerates/tables/A/last/60')
    response_json = response.json()

    date_str = []
    for response_entry in response_json:
        date_str = response_entry['effectiveDate']
        rates_data = response_entry['rates']

        for entry in rates_data:
            rate = CurrencyRate(date_str, entry['currency'], entry['code'], entry['mid'])
            all_rates.append(rate)

    return all_rates


def get_gold_rate():
    gold_rates = []

    response = requests.get(f'http://api.nbp.pl/api/cenyzlota/last/60')
    response_json = response.json()

    for response_entry in response_json:
        gold_rate = GoldRate(response_entry['data'], response_entry['cena'])
        gold_rates.append(gold_rate)

    return gold_rates
