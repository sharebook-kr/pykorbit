import requests
import time
import csv


def get_current_price(currency="btc_krw"):
    """
    최종 체결 가격을 얻어오는 메서드
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :return: price
    """
    payload = {"currency_pair": currency}
    url = "https://api.korbit.co.kr/v1/ticker"
    r = requests.get(url, params=payload)
    contents = r.json()
    price = contents['last']
    return float(price)


def get_market_detail(currency="btc_krw"):
    """
    시장 현황 상세정보를 얻어오는 메서드
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :return: (24시간저가, 24시간고가, 최종체결가격, 거래량)
    """
    payload = {"currency_pair": currency}
    url = "https://api.korbit.co.kr/v1/ticker/detailed"
    r = requests.get(url, params=payload)
    contents = r.json()

    low  = contents['low']
    high = contents['high']
    last = contents['last']
    volume = contents['volume']
    return float(low), float(high), float(last), float(volume)


def get_transaction_data(currency="btc_krw", interval="day"):
    """
    최근 1분/최근 1시간/최근 1일의 체결 데이터를 요청
    :param currency: btc_krw/bch_krw/btg_krw/eth_krw/etc_krw/xrp_krw
    :param interval: minute/hour/day
    :return:
    """
    payload = {"currency_pair": currency, "time": interval}
    url = "https://api.korbit.co.kr/v1/transactions"
    r = requests.get(url, params=payload)
    contents = r.json()
    return contents


def get_constants():
    """
    가상 화폐에 관련된 제약 조건을 얻어오는 메서드
    :return: Dict
    """
    url = "https://api.korbit.co.kr/v1/constants"
    r = requests.get(url)
    contents = r.json()
    return contents


class Korbit(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._read_keys_csv()
        self._get_constants()
        self._issue_access_token()

    def _read_keys_csv(self):
        """
        현재 디렉터리에 있는 keys.csv 파일로부터 key와 secret 정보를 읽어오는 메서드
        :return:
        """
        f = open("keys.csv")
        reader = csv.reader(f)
        lines = list(reader)
        f.close()

        self.key = lines[1][0]
        self.secret = lines[1][1]

    def _issue_access_token(self):
        """
        access token을 발급하는 메서드
        :return:
        """
        data = {"client_id": self.key,
                "client_secret": self.secret,
                "grant_type": "password",
                "username": self.email,
                "password": self.password}
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"

        r = requests.post(url, data=data)
        contents = r.json()
        self.access_token = contents['access_token']
        self.refresh_token = contents['refresh_token']

    def renew_access_token(self):
        """
        발급받은 access_token과 refresh_token을 사용해서 access_token을 갱신하는 메서드
        :return:
        """
        data = {"client_id": self.key,
                "client_secret": self.secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token}

        r = requests.post("https://api.korbit.co.kr/v1/oauth2/access_token", data=data)
        contents = r.json()
        self.access_token = contents['access_token']
        self.refresh_token = contents['refresh_token']

    def _get_constants(self):
        contents = get_constants()

        # btc
        self.btc_tick_size = contents['btcTickSize']
        self.btc_max_order = contents['maxBtcOrder']
        self.btc_min_order = contents['minBtcOrder']
        self.btc_max_order_price = contents["maxBtcPrice"]
        self.btc_min_order_price = contents["minBtcPrice"]

        # etc
        self.etc_tick_size = contents['etcTickSize']
        self.etc_max_order = contents['maxEtcOrder']
        self.etc_min_order = contents['minEtcOrder']
        self.etc_max_order_price = contents["maxEtcPrice"]
        self.etc_min_order_price = contents["minEtcPrice"]

        # eth
        self.eth_tick_size = contents['ethTickSize']
        self.eth_max_order = contents['maxEthOrder']
        self.eth_min_order = contents['minEthOrder']
        self.eth_max_order_price = contents["maxEthPrice"]
        self.eth_min_order_price = contents["minEthPrice"]

    def _get_tick_size(self, currency):
        """
        KRW 기준 호가 단위를 리턴하는 메서드
        :param currency: etc_krw/eth_krw/btc_krw/xrp_krw/bch_krw
        :return:
        """
        if currency == "etc_krw":
            return self.etc_tick_size
        elif currency == "eth_krw":
            return self.eth_tick_size
        elif currency == "btc_krw":
            return self.btc_tick_size
        elif currency == "xrp_krw":
            return 1
        elif currency == "bch_krw":
            return 500

    def _get_min_order(self, currency):
        """
        매매 수량 최소 입력 값을 리턴하는 메서드
        :param currency:
        :return:
        """
        if currency == "etc_krw":
            return self.etc_min_order
        elif currency == "eth_krw":
            return self.eth_min_order
        elif currency == "btc_krw":
            return self.btc_min_order
        elif currency == "xrp_krw":
            return 10
        elif currency == "bch_krw":
            return 0.005

    def buy_market_order(self, currency, expenditure):
        """
        시장가로 매수하는 메서드
        :param currency: btc_krw, bch_krw, eth_krw, etc_krw, xrp_krw
        :param expenditure: 지출액
        :return:
        """
        if expenditure < 5000:
            print("5,000 KRW 이상만 주문 가능합니다. ")
            return

        current_price = get_current_price(currency)
        min_order = self._get_min_order(currency)
        expected_quantity = expenditure / current_price

        if expected_quantity < min_order:
            print(min_order, "이상만 가능합니다.")

        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "type": "market",
                "fiat_amount": expenditure,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/buy"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents

    def buy_limit_order(self, currency, price, amount):
        """
        지정가로 매수하는 메서드
        :param currency: btc_krw, bch_krw, eth_krw, etc_krw, xrp_krw
        :param price: 주문가
        :param amount: 매수량
        :return:
        """
        min_order = self._get_min_order(currency)

        if amount < min_order:
            print(min_order, "이상만 가능합니다.")

        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "type": "limit",
                "price": price,
                "coin_amount": amount,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/buy"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents

    def sell_market_order(self, currency, coin_amount):
        """
        시장가 매도
        :param currency:
        :param coin_amount:
        :return:
        """
        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "type": "market",
                "coin_amount": coin_amount,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/sell"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents['orderId'], contents['status'], contents['currencyPair']

    def sell_limit_order(self, currency, price, coin_amount):
        """
        지정가 매도
        :param currency:
        :param price:
        :param coin_amount:
        :return:
        """
        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "type": "limit",
                "price": price,
                "coin_amount": coin_amount,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/sell"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents['orderId'], contents['status'], contents['currencyPair']

    def cancel_order(self, currency, id):
        """
        주문 취소
        :param currency:
        :param id:
        :return:
        """
        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "id": id,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/cancel"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents

    def get_balances(self):
        headers = {"Authorization": "Bearer " + self.access_token}
        url = "https://api.korbit.co.kr/v1/user/balances"
        r = requests.get(url, headers=headers)
        contents = r.json()
        return contents


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
    #print("BTC : ", get_market_detail("btc_krw"))
    #print("BCH : ", get_market_detail("bch_krw"))
    #print("BTG : ", get_market_detail("btg_krw"))
    #print("ETH : ", get_market_detail("eth_krw"))
    #print("ETC : ", get_market_detail("etc_krw"))
    #print("XRP : ", get_market_detail("xrp_krw"))

    #----------------------------------------------------------------------------------------------
    # 체결 내역 (과거 데이터)
    #----------------------------------------------------------------------------------------------
    #print("BTC : ", get_transaction_data("btc_krw", "day"))
    #print("BCH : ", get_transaction_data("bch_krw", "day"))
    #print("BTG : ", get_transaction_data("btg_krw", "day"))
    #print("ETH : ", get_transaction_data("eth_krw", "day"))
    #print("ETC : ", get_transaction_data("etc_krw", "day"))
    #print("XRP : ", get_transaction_data("xrp_krw", "day"))

    #----------------------------------------------------------------------------------------------
    # 제약조건
    #----------------------------------------------------------------------------------------------
    #constants = get_constants()
    #print(len(constants.keys()))

    #----------------------------------------------------------------------------------------------
    # 거래소-회원
    #----------------------------------------------------------------------------------------------
    #email = "your-email@gmail.com"
    #password = "your-password"
    #korbit = Korbit(email, password)
    #korbit.buy_market_order("etc_krw", 9800)
    #korbit.buy_limit_order("etc_krw", 30000, 0.1)

    # 지정가 매도
    #order_id, status, currency = korbit.sell_limit_order("etc_krw", 45000, 0.28)
    #print("지정가 매도", order_id, status, currency)

    # 시장가 매도
    #order_id, status, currency = korbit.sell_market_order("etc_krw", 0.1)
    #print("시장가 매도", order_id, status, currency)

    # 시장가 매수
    #korbit.buy_market_order("btc_krw", 11141)

    # 지정가 매수
    #korbit.buy_limit_order("etc_krw", 30000, 0.1)

    # 주문 취소
    #time.sleep(1)
    #ret = korbit.cancel_order(currency, order_id)
    #print(ret)

    # 지갑 잔고 조회
    #ret = korbit.get_balances()
    #print(ret)

