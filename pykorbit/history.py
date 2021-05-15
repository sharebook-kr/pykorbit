import requests
import datetime
import pandas as pd


def get_ohlc(symbol="BTC", timeunit="day", start=None, end=None, period=None):
    '''
    :param symbol: BTC/ETH/BCH/ETC
    :param timeunit: day/hour/minute
    :param start: 2018-01-01
    :param end: 2018-03-01
    :param period: 5 days
    :return:
    '''
    # HACK
    # - symbol of MED in cryptocompare is MEDIB
    if symbol == "MED":
        symbol = "MEDIB"

    if start == None and end == None:
        end = datetime.datetime.now()
        if period != None:
            assert(period > 0)
            start = end - datetime.timedelta(days=period-1)
        else:
            start = datetime.datetime(2013, 9, 4)
    elif start == None:   # end != None
        end = pd.to_datetime(end)
        if period != None:
            assert(period > 0)
            start = end - datetime.timedelta(days=period-1)
        else:
            start = datetime.datetime(2013, 9, 4)
    elif end == None: # start != None
        start = pd.to_datetime(start)
        if period != None:
            assert(period > 0)
            end = start + datetime.timedelta(days=period-1)
        else:
            end = datetime.datetime.now() #- datetime.timedelta(days=1)
    else:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        if period != None:
            print(f"period is ignored")

    delta = end - start
    limit = min(2000, delta.days)

    payload = {
        "fsym" : symbol,
        "tsym" : "KRW",
        "e"    : "Korbit",
        "limit": limit,
        "toTs" : int(end.timestamp())
    }

    try:
        url = "https://min-api.cryptocompare.com/data/histo" + timeunit
        r = requests.get(url, params=payload)
        content = r.json()
    except:
        content = None

    if content is not None:
        date_list = [datetime.datetime.fromtimestamp(x['time']) for x in content['Data']]
        df = pd.DataFrame(content['Data'], columns=['open', 'high', 'low', 'close'], index=date_list)
        all_zero_cnt = df.all(axis=1).astype(int).sum()
        if all_zero_cnt > 0:
            print(f"INFO: all zero {all_zero_cnt} row(s) are removed in X-axis")
        return df.loc[df.all(axis=1)]
    else:
        return None


if __name__ == "__main__":
    # day
    #print(get_ohlc(symbol="BTC", start="2018-02-01", end="2018-02-03"))
    #print(get_ohlc(symbol="BTC", period=5))
    #print(get_ohlc(symbol="BTC", end="2018-02-03", period=5))

    # hour
    print(get_ohlc(symbol="BTC"))
    print(get_ohlc(symbol="BTC", timeunit='hour'))
    # /print(get_ohlc(symbol="BTC", timeunit='hour', period=5))

    # # minute
    print(get_ohlc(symbol="BTC", timeunit='minute'))
    print(get_ohlc(symbol="BTC", timeunit='minute', period=5))
