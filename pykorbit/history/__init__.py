import requests
import datetime


def get_daily_ohlcv(symbol="BTC", start="", end=""):
    '''

    :param symbol:
    :param start:
    :param end:
    :return:
    '''

    start = datetime.datetime(2016, 1, 1)
    end = datetime.datetime(2018, 3, 31)
    delta = end - start

    timestamp = int(end.timestamp())
    # payload = {"fsym": symbol,
    #            "tsym": "KRW",
    #            "e": "Korbit",
    #            "limit": delta.days,
    #            "toTs": timestamp}

    payload = {"fsym": symbol,
               "tsym": "KRW",
               "e": "Korbit"}

    url = "https://min-api.cryptocompare.com/data/histoday"
    r = requests.get(url, params=payload)
    content = r.json()

    for day_data in content['Data']:
        print(datetime.datetime.fromtimestamp(day_data['time']))


get_daily_ohlcv()


