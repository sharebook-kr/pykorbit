import requests
import time
from pykorbit.public_api import *
import sys

getframe_expr = 'sys._getframe({}).f_code.co_name'

def _send_post_request(url, headers=None, data=None):
    try:
        resp = requests_retry_session().post(url, headers=headers, data=data)
        contents = resp.json()
        return contents
    except Exception as x:
        print("send post request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None
    else:
        print(resp.status_code)
        return None


def _send_get_request(url, headers=None):
    try:
        resp = requests_retry_session().get(url, headers=headers)
        contents = resp.json()
        return contents
    except Exception as x:
        print("send get request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None
    else:
        print(resp.status_code)
        return None


class Korbit(object):
    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret
        self.constant = None

        self.access_token = None
        self.refresh_token = None
        self.headers = None

        self._issue_access_token()
        self._get_constants()

    def _issue_access_token(self):
        """
        access token을 처음 발급하는 메서드
        :return:
        """
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {
            "client_id": self.key,
            "client_secret": self.secret,
            "grant_type": "client_credentials",
        }

        contents = _send_post_request(url, data=data)

        if isinstance(contents, dict):
            if 'access_token' in contents.keys():
                self.access_token = contents.get('access_token')
                self.refresh_token = contents.get('refresh_token')
            elif 'error' in contents.keys():
                print(contents.get("error_description"))

    def renew_access_token(self):
        """
        발급받은 access_token과 refresh_token을 사용해서 access_token을 갱신하는 메서드
        :return:
        """
        url = "https://api.korbit.co.kr/v1/oauth2/access_token"
        data = {"client_id": self.key,
                "client_secret": self.secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token}

        contents = _send_post_request(url, data=data)

        if isinstance(contents, dict):
            if 'access_token' in contents.keys():
                self.access_token = contents.get('access_token')
                self.refresh_token = contents.get('refresh_token')
            else:
                print("renew_access_token error ", contents)

    def _get_constants(self):
        self.constant = get_constants()

    def _get_tick_size(self, currency="BTC"):
        """
        KRW 기준 호가 단위를 리턴하는 메서드
        :param currency: BTC/BCH/BTG/ETH/ETC/XRP
        :return:
        """
        try:
            if self.constant is not None:
                currency = currency.lower() + "_krw"
                currency_dic = self.constant.get(currency)

                if isinstance(currency_dic, dict):
                    return currency_dic.get("tick_size")
                else:
                    return None
            else:
                return None
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def _get_quantity_min_max(self, currency="BTC"):
        """
        매수/매도 수량 최소 입력값
        :param currency: BTC/BCH/BTG/ETH/ETC/XRP
        :return:
        """
        try:
            if self.constant is not None:
                currency = currency.lower() + "_krw"
                currency_dic = self.constant.get(currency)

                if isinstance(currency_dic, dict):
                    return currency_dic.get("order_min_size"), currency_dic.get("order_max_size")
                else:
                    return None
            else:
                return None
        except Exception as x:
            print(x.__class__.__name__)
            return None


    def _get_price_min_max(self, currency="BTC"):
        """
        최소/최대 주문가 (원화 기준)
        :param currency: BTC/BCH/BTG/ETH/ETC/XRP
        :return:
        """
        try:
            if self.constant is not None:
                currency = currency.lower() + "_krw"
                currency_dic = self.constant.get(currency)

                if isinstance(currency_dic, dict):
                    return currency_dic.get("min_price"), currency_dic.get("max_price")
                else:
                    return None
            else:
                return None
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_headers(self):
        try:
            if self.access_token is not None:
                headers = {"Authorization": "Bearer " + self.access_token}
                return headers
            else:
                print("current access_token is not valid")
                return None
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def buy_market_order(self, currency="BTC", expenditure=None):
        """
        시장가로 매수하는 메서드
        :param currency: BTC/BCH/BTG/ETH/ETC/XRP
        :param expenditure: 지출액
        :return:
        """
        try:
            currency = currency.lower() + "_krw"
            url = "https://api.korbit.co.kr/v1/user/orders/buy"
            headers = self.get_headers()
            data = {"currency_pair": currency,
                    "type": "market",
                    "fiat_amount": expenditure,
                    "nonce": str(int(time.time()))}

            contents = _send_post_request(url, headers=headers, data=data)
            if contents is not None:
                return contents.get('orderId'), contents.get('status'), contents.get('currencyPair')
            else:
                return None, None, None
        except Exception as x:
            print(x.__class__.__name__)
            return None, None, None

    def buy_limit_order(self, currency="BTC", price=10000, amount=1):
        """
        지정가로 매수하는 메서드
        :param currency: BTC/BCH/BTG/ETH/ETC/XRP
        :param price: 주문가
        :param amount: 매수량
        :return:
        """
        try:
            currency = currency.lower() + "_krw"
            url = "https://api.korbit.co.kr/v1/user/orders/buy"
            headers = self.get_headers()
            data = {"currency_pair": currency,
                    "type": "limit",
                    "price": price,
                    "coin_amount": amount,
                    "nonce": str(int(time.time()))}

            contents = _send_post_request(url, headers=headers, data=data)
            if contents is not None:
                return contents.get('orderId'), contents.get('status'), contents.get('currencyPair')
            else:
                return None, None, None
        except Exception as x:
            print(x.__class__.__name__)
            return None, None, None

    def sell_market_order(self, currency="BTC", coin_amount=1):
        """
        시장가 매도
        :param currency: BTC/BCH/BTG/ETH/ETC/XRP
        :param coin_amount:
        :return:
        """
        try:
            currency = currency.lower() + "_krw"
            url = "https://api.korbit.co.kr/v1/user/orders/sell"
            headers = self.get_headers()
            data = {"currency_pair": currency,
                    "type": "market",
                    "coin_amount": coin_amount,
                    "nonce": str(int(time.time()))}

            contents = _send_post_request(url, headers=headers, data=data)
            if contents is not None:
                return contents.get('orderId'), contents.get('status'), contents.get('currencyPair')
            else:
                return None, None, None
        except Exception as x:
            print(x.__class__.__name__)
            return None, None, None

    def sell_limit_order(self, currency="BTC", price=10000, coin_amount=1):
        """
        지정가 매도
        :param currency:
        :param price:
        :param coin_amount:
        :return:
        """
        try:
            currency = currency.lower() + "_krw"
            url = "https://api.korbit.co.kr/v1/user/orders/sell"
            headers = self.get_headers()
            data = {"currency_pair": currency,
                    "type": "limit",
                    "price": price,
                    "coin_amount": coin_amount,
                    "nonce": str(int(time.time()))}

            contents = _send_post_request(url, headers=headers, data=data)
            if contents is not None:
                return contents.get('orderId'), contents.get('status'), contents.get('currencyPair')
            else:
                return None, None, None
        except Exception as x:
            print(x.__class__.__name__)
            return None, None, None

    def cancel_order(self, currency="BTC", id=10000):
        """
        주문 취소
        :param currency:
        :param id:
        :return:
        """
        try:
            currency = currency.lower() + "_krw"
            url = "https://api.korbit.co.kr/v1/user/orders/cancel"
            headers = self.get_headers()
            data = {"currency_pair": currency,
                    "id": id,
                    "nonce": str(int(time.time()))}

            return _send_post_request(url, headers=headers, data=data)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_balances(self):
        url = "https://api.korbit.co.kr/v1/user/balances"
        headers = self.get_headers()
        return _send_get_request(url, headers=headers)

    def get_open_orders(self, currency="BTC", offset=0, limit=10):
        """
        미 체결 주문 내역
        :param currency: "BTC", "ETC", "ETH", "XRP", "BCH", "LTC"
        :param offset: offset
        :param limit: requested number of open orders
        :return:
        """
        url = "https://api.korbit.co.kr/v1/user/orders/open?currency_pair={}&offset={}&limit={}".format(currency.lower() + "_krw", offset, limit)
        headers = self.get_headers()
        return _send_get_request(url, headers=headers)

    def get_orders(self, currency_pair="BTC", status=None, id=None, offset=0, limit=40):
        '''
        거래소 주문 조회
        :param currency_pair: ticker
        :param status: 'unfilled', 'partially_filled', 'filled'
        :param id: 주문 ID or 주문 ID 리스트
        :param offset: 0
        :param limit: 40
        :return:
        '''
        try:
            params = []
            url = "https://api.korbit.co.kr/v1/user/orders?"
            currency_pair = "currency_pair={}".format(currency_pair.lower() + "_krw")
            params.append(currency_pair)

            if isinstance(status, str):
                status = "status={}".format(status)
            elif isinstance(status, list) or isinstance(status, tuple):
                status_list = ["status={}".format(state) for state in status]
                status = "&".join(status_list)
            if status is not None:
                params.append(status)

            if isinstance(id, int):
                id = "id={}".format(id)
            elif isinstance(id, list) or isinstance(id, tuple):
                id_list = ["id={}".format(cur_id) for cur_id in id]
                id = "&".join(id_list)
            if id is not None:
                params.append(id)

            offset = "offset={}".format(offset)
            params.append(offset)

            limit = "limit={}".format(limit)
            params.append(limit)

            url_with_params = url + "&".join(params)
            headers = self.get_headers()
            return _send_get_request(url_with_params, headers=headers)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_transfers(self, currency="KRW", type="all", offset=0, limit=40):
        try:
            url = "https://api.korbit.co.kr/v1/user/transfers?currency={}&type={}&offset={}&limit={}".format(currency, type, offset, limit)
            headers = self.get_headers()
            return _send_get_request(url, headers=headers)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_fee(self, currency="all"):
        try:
            if currency == "all":
                currency_pair = "all"
            else:
                currency_pair = currency.lower() + "_krw"

            url = "https://api.korbit.co.kr/v1/user/volume?currency_pair={}".format(currency_pair)
            headers = self.get_headers()
            return _send_get_request(url, headers=headers)
        except Exception as x:
            print(x.__class__.__name__)
            return None


if __name__ == "__main__":
    with open("korbit.conf") as f:
        email, password, key, secret = (x.strip() for x in f)

    korbit = Korbit(email, password, key, secret)

    # 주문 제약 조건
    #print(korbit._get_tick_size("BTC"))
    #print(korbit._get_quantity_min_max("BTC"))
    #print(korbit._get_price_min_max("BTC"))

    # 매수-시장
    #print("시장가 매수")
    #print(korbit.buy_market_order("ETC", 9800))

    # 매수-지정가
    #print("지정가 매수")
    #print(korbit.buy_limit_order("ETC", 9000, 0.1))

    # 지정가 매도
    # print(korbit.sell_limit_order("ETH", 850000, 0.15267251))

    # 시장가 매도
    #print(korbit.sell_market_order("ETC", 0.1))


    # 주문 취소
    #time.sleep(1)
    #print(korbit.cancel_order("BTC", 9000))
    #print(korbit.cancel_order("BTC", [1000, 10001]))
    #print(ret)

    # 지갑 잔고 조회
    # print(korbit.get_balances())

    # 미 체결 주문 내역
    # time.sleep(1)
    # open_orders = korbit.get_open_orders(currency="ETC", offset=0, limit=2)
    # print(len(open_orders))
    # print(open_orders)

    # 거래소 주문 조회
    orders = korbit.get_orders(currency_pair="BTC")
    print(orders)

    orders = korbit.get_orders(currency_pair="BTC", status=["unfilled", "partially_filled"], id=[900308])
    print(orders)

    # 입출금 내역 조회
    #transfers = korbit.get_transfers()
    #print(len(transfers))
    #print(transfers)

    # 거래량과 거래 수수료
    #fee = korbit.get_fee("BTC")
    #print(fee)