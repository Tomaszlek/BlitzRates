import sqlite3


################# Creating tables #####################
def create_rates_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kursy_walut
                      (data TEXT, nazwa TEXT, kod TEXT, kurs REAL)''')
    conn.commit()


def create_gold_rate_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kurs_zlota
                          (data TEXT, kurs REAL)''')
    conn.commit()


################# Getting data ##########################
def get_currency_data(currency_code):
    conn = sqlite3.connect('kursy_walut.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT data, kurs FROM kursy_walut 
                      WHERE kod = ? ORDER BY data''', (currency_code,))
    rows = cursor.fetchall()
    conn.close()

    return rows


def get_gold_data():
    conn = sqlite3.connect('kursy_walut.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT data, kurs FROM kurs_zlota
                           ORDER BY data''')
    rows = cursor.fetchall()
    conn.close()

    return rows


################ Inserting data ########################
def insert_currency_rates_into_database(conn, rates):
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM kursy_walut''')

    for rate in rates:
        cursor.execute('''INSERT INTO kursy_walut (data, nazwa, kod, kurs)
                        VALUES (?, ?, ?, ?)''', (rate.date, rate.name, rate.code, rate.rate))

    conn.commit()


def insert_gold_rate_into_database(conn, gold_rate):
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM kurs_zlota''')

    for rate in gold_rate:
        cursor.execute('''INSERT INTO kurs_zlota (data, kurs)
                        VALUES (?, ?)''', (rate.date, rate.rate))

    conn.commit()


def get_unique_currencies(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT nazwa, kod FROM kursy_walut''')

    unique_currency_codes = cursor.fetchall()
    conn.commit()

    return unique_currency_codes
