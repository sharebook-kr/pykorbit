import requests
import time
import csv


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
        """
        가상 화폐에 관련된 제약 조건을 얻어오는 메서드
        :return:
        """
        url = "https://api.korbit.co.kr/v1/constants"
        r = requests.get(url)
        contents = r.json()
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

    def get_current_price(self, currency="btc_krw"):
        """
        최종 체결 가격을 얻어오는 메서드
        :param currency: etc_krw/eth_krw/xrp_krw/bch_krw
        :return: price
        """
        payload = {"currency_pair": currency}
        url = "https://api.korbit.co.kr/v1/ticker"
        r = requests.get(url, params=payload)
        contents = r.json()
        price = contents['last']
        return float(price)

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

        current_price = self.get_current_price(currency)
        min_order = self._get_min_order(currency)
        expected_quantity = expenditure / current_price

        if expected_quantity < min_order:
            print(min_order, "이상만 가능합니다.")

        self._buy(currency, "market", 0, 0, expenditure)

    def _buy(self, currency, order_type, price, coin_amount, fiat_amount):
        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "type": order_type,
                "price": price,
                "coin_amount": coin_amount,
                "fiat_amount": fiat_amount,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/buy"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents

    def _sell(self, currency, type, price, coin_amount):
        nonce = str(int(time.time()))
        headers = {"Authorization": "Bearer " + self.access_token}
        data = {"currency_pair": currency,
                "type": type,
                "price": price,
                "coin_amount": coin_amount,
                "nonce": nonce}

        url = "https://api.korbit.co.kr/v1/user/orders/sell"
        r = requests.post(url, headers=headers, data=data)
        contents = r.json()
        return contents


if __name__ == "__main__":
    email = "your-email@gmail.com"
    password = "your-password"
    korbit = Korbit(email, password)
    korbit.buy_market_order("etc_krw", 9800)
