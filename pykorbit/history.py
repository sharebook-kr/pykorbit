import requests
import datetime
import pandas as pd


def get_daily_ohlc(symbol="BTC", start=None, end=None, period=None):
    '''
    :param symbol: BTC/ETH/BCH/ETC
    :param start: 2018-01-01
    :param end: 2018-03-01
    :param period: 5 days
    :return:
    '''
    try:
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
    except:
        start = datetime.datetime(2013, 9, 4)

    try:
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
    except:
        end = datetime.datetime.now() - datetime.timedelta(days=2)

    end += datetime.timedelta(days=1)
    delta = end - start
    timestamp = int(end.timestamp())

    if isinstance(period, int):
        limit = period
    else:
        limit = delta.days

    payload = {"fsym": symbol,
               "tsym": "KRW",
               "e": "Korbit",
               "limit": limit-1,
               "toTs": timestamp}

    try:
        url = "https://min-api.cryptocompare.com/data/histoday"
        r = requests.get(url, params=payload)
        content = r.json()
    except:
        content = None

    if content is not None:
        date_list = [datetime.datetime.fromtimestamp(x['time']) for x in content['Data']]
        df = pd.DataFrame(content['Data'], columns=['open', 'high', 'low', 'close'], index=date_list)
        return df
    else:
        return None


if __name__ == "__main__":
    print(get_daily_ohlc("BTC", start="2018-02-01", end="2018-02-03"))
    print(get_daily_ohlc("BTC", period=5))
    print(get_daily_ohlc("BTC", end="2018-02-03", period=5))
