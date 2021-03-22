import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def requests_retry_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    s = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


def _call_public_api(url, **kwargs):
    try:
        resp = requests_retry_session().get(url, params=kwargs)
        contents = resp.json()
        return contents
    except Exception as x:
        print("It failed", x.__class__.__name__)
        return None
    else:
        print(resp.status_code)
        return None


def get_current_price(currency="BTC"):
    """
    최종 체결 가격을 얻어오는 메서드
    :param currency: BTC/BCH/BTG/ETH/ETC/XRP
    :return: price
    """
    try:
        currency = currency.lower() + "_krw"
        url = "https://api.korbit.co.kr/v1/ticker"
        contents = _call_public_api(url, currency_pair=currency)

        if contents is not None:
            price = contents['last']
            return float(price)
        else:
            return None
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_market_detail(currency="BTC"):
    """
    시장 현황 상세정보를 얻어오는 메서드
    :param currency: BTC/BCH/BTG/ETH/ETC/XRP
    :return: (24시간저가, 24시간고가, 최종체결가격, 거래량)
    """
    try:
        currency = currency.lower() + "_krw"
        url = "https://api.korbit.co.kr/v1/ticker/detailed"
        contents = _call_public_api(url, currency_pair=currency)

        if contents is not None:
            low  = contents['low']
            high = contents['high']
            last = contents['last']
            volume = contents['volume']
            return float(low), float(high), float(last), float(volume)
        else:
            return None, None, None, None
    except Exception as x:
        print(x.__class__.__name__)
        return None, None, None, None


def get_orderbook(currency="BTC"):
    """
    매수/매도 호가를 얻어오는 메서드
    :param currency: BTC/BCH/BTG/ETH/ETC/XRP
    :return: 매수/매도 호가
    """
    try:
        currency = currency.lower() + "_krw"
        url = "https://api.korbit.co.kr/v1/orderbook"
        contents = _call_public_api(url, currency_pair=currency)
        return contents
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_transaction_data(currency="BTC", interval="day"):
    """
    최근 1분/최근 1시간/최근 1일의 체결 데이터를 요청
    :param currency: BTC/BCH/BTG/ETH/ETC/XRP
    :param interval: minute/hour/day
    :return:
    """
    try:
        currency = currency.lower() + "_krw"
        url = "https://api.korbit.co.kr/v1/transactions"
        contents = _call_public_api(url, currency_pair=currency, time=interval)
        return contents
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_constants():
    """
    가상 화폐에 관련된 제약 조건을 얻어오는 메서드
    :return: Dict
    """
    try:
        url = "https://api.korbit.co.kr/v1/constants"
        contents = _call_public_api(url)
        if contents is not None:
            return contents['exchange']
        else:
            return None
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_tickers():
    try:
        constants = get_constants()
        return [x.split("_")[0].upper() for x in constants.keys()]
    except Exception as x:
        print(x.__class__.__name__)
        return None


if __name__ == "__main__":
    #----------------------------------------------------------------------------------------------
    # 최종 체결 가격
    #----------------------------------------------------------------------------------------------
    #print("BTC : ", get_current_price("BTC"))

    #----------------------------------------------------------------------------------------------
    # 시장 현황 상세정보
    #----------------------------------------------------------------------------------------------
    #print("BTC : ", get_market_detail("BTC"))

    #----------------------------------------------------------------------------------------------
    # 매수/매도 호가
    #----------------------------------------------------------------------------------------------
    #print("BTC : ", get_orderbook("BTC"))

    #----------------------------------------------------------------------------------------------
    # 체결 내역 (과거 데이터)
    #----------------------------------------------------------------------------------------------
    #print("BTC : ", get_transaction_data(currency="BTC", interval="day"))

    #----------------------------------------------------------------------------------------------
    # 제약조건
    #----------------------------------------------------------------------------------------------
    print(get_constants())

    print(get_tickers())
