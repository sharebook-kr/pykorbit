import requests


def _call_public_api(url, **kwargs):
    try:
        r = requests.get(url, params=kwargs)
        contents = r.json()
        return contents
    except:
        return None


def get_current_price(currency="btc_krw"):
    """
    최종 체결 가격을 얻어오는 메서드
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :return: price
    """
    url = "https://api.korbit.co.kr/v1/ticker"
    contents = _call_public_api(url, currency_pair=currency)

    if contents is not None:
        price = contents['last']
        return float(price)
    else:
        return None


def get_market_detail(currency="btc_krw"):
    """
    시장 현황 상세정보를 얻어오는 메서드
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :return: (24시간저가, 24시간고가, 최종체결가격, 거래량)
    """
    url = "https://api.korbit.co.kr/v1/ticker/detailed"
    contents = _call_public_api(url, currency_pair=currency)

    if contents is not None:
        low  = contents['low']
        high = contents['high']
        last = contents['last']
        volume = contents['volume']
        return float(low), float(high), float(last), float(volume)
    else:
        return None


def get_orderbook(currency="btc_krw"):
    """
    매수/매도 호가를 얻어오는 메서드
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :return: 매수/매도 호가
    """
    url = "https://api.korbit.co.kr/v1/orderbook"
    contents = _call_public_api(url, currency_pair=currency)
    return contents


def get_transaction_data(currency="btc_krw", interval="day"):
    """
    최근 1분/최근 1시간/최근 1일의 체결 데이터를 요청
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :param interval: minute/hour/day
    :return:
    """
    url = "https://api.korbit.co.kr/v1/transactions"
    contents = _call_public_api(url, currency_pair=currency, time=interval)
    return contents


def get_constants():
    """
    가상 화폐에 관련된 제약 조건을 얻어오는 메서드
    :return: Dict
    """
    url = "https://api.korbit.co.kr/v1/constants"
    contents = _call_public_api(url)
    if contents is not None:
        return contents['exchange']
    else:
        return None


if __name__ == "__main__":
    #----------------------------------------------------------------------------------------------
    # 최종 체결 가격
    #----------------------------------------------------------------------------------------------
    print("BTC : ", get_current_price("btc_krw"))
    #print("BCH : ", get_current_price("bch_krw"))
    #print("BTG : ", get_current_price("btg_krw"))
    #print("ETH : ", get_current_price("eth_krw"))
    #print("ETC : ", get_current_price("etc_krw"))
    #print("XRP : ", get_current_price("xrp_krw"))

    #----------------------------------------------------------------------------------------------
    # 시장 현황 상세정보
    #----------------------------------------------------------------------------------------------
    print("BTC : ", get_market_detail("btc_krw"))
    #print("BCH : ", get_market_detail("bch_krw"))
    #print("BTG : ", get_market_detail("btg_krw"))
    #print("ETH : ", get_market_detail("eth_krw"))
    #print("ETC : ", get_market_detail("etc_krw"))
    #print("XRP : ", get_market_detail("xrp_krw"))

    #----------------------------------------------------------------------------------------------
    # 매수/매도 호가
    #----------------------------------------------------------------------------------------------
    print("BTC : ", get_orderbook("btc_krw"))
    #print("BCH : ", get_orderbook("bch_krw"))
    #print("BTG : ", get_orderbook("btg_krw"))
    #print("ETH : ", get_orderbook("eth_krw"))
    #print("ETC : ", get_orderbook("etc_krw"))
    #print("XRP : ", get_orderbook("xrp_krw"))

    #----------------------------------------------------------------------------------------------
    # 체결 내역 (과거 데이터)
    #----------------------------------------------------------------------------------------------
    print("BTC : ", get_transaction_data("btc_krw", "day"))
    #print("BCH : ", get_transaction_data("bch_krw", "day"))
    #print("BTG : ", get_transaction_data("btg_krw", "day"))
    #print("ETH : ", get_transaction_data("eth_krw", "day"))
    #print("ETC : ", get_transaction_data("etc_krw", "day"))
    #print("XRP : ", get_transaction_data("xrp_krw", "day"))

    #----------------------------------------------------------------------------------------------
    # 제약조건
    #----------------------------------------------------------------------------------------------
    print(get_constants())
