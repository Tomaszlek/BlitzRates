class Rate:
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate

    def __getitem__(self, item):
        return getattr(self, item)


class CurrencyRate(Rate):
    def __init__(self, date, name, code, rate):
        super().__init__(date, rate)
        self.name = name
        self.code = code


class GoldRate(Rate):
    def __init__(self, date, rate):
        super().__init__(date, rate)
