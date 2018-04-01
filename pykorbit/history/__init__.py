import requests
import datetime
import pandas as pd

def get_daily_ohlc(symbol="BTC", start=None, end=None):
    '''
    :param symbol: BTC/ETH/BCH/ETC
    :param start: 2018-01-01
    :param end: 2018-03-01
    :return:
    '''
    try:
        start = datetime.datetime.strptime(start, "%Y-%m-%d")
    except:
        start = datetime.datetime(2013, 9, 4)

    try:
        end = datetime.datetime.strptime(end, "%Y-%m-%d")
    except:
        end = datetime.datetime.now()

    end += datetime.timedelta(days=1)
    delta = end - start
    timestamp = int(end.timestamp())

    payload = {"fsym": symbol,
               "tsym": "KRW",
               "e": "Korbit",
               "limit": delta.days-1,
               "toTs": timestamp}

    url = "https://min-api.cryptocompare.com/data/histoday"
    r = requests.get(url, params=payload)
    content = r.json()

    date_list = [datetime.datetime.fromtimestamp(x['time']) for x in content['Data']]
    df = pd.DataFrame(content['Data'], columns=['open', 'high', 'low', 'close'], index=date_list)
    return df


if __name__ == "__main__":
    df = get_daily_ohlc("BTC", "2018-02-01", "2018-02-03")
    print(df)


