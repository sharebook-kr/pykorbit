# korbit-api
Python Wrapper for Korbit API

## Installation
```sh
pip install pykorbit
pip install --upgrade pykorbit
```

## Public API
Ticker

```python
import pykorbit

pykorbit.get_current_price("BTC")
pykorbit.get_current_price("BCH")
pykorbit.get_current_price("BTG")
pykorbit.get_current_price("ETH")
pykorbit.get_current_price("ETC")
pykorbit.get_current_price("XRP")
```

Detailed Ticker
```python
import pykorbit

pykorbit.get_market_detail("BTC")
pykorbit.get_market_detail("BCH")
pykorbit.get_market_detail("BTG")
pykorbit.get_market_detail("ETH")
pykorbit.get_market_detail("ETC")
pykorbit.get_market_detail("XRP")
```

Transaction
```python
import pykorbit

pykorbit.get_transaction_data("BTC")
pykorbit.get_transaction_data("BCH")
pykorbit.get_transaction_data("BTG")
pykorbit.get_transaction_data("ETH")
pykorbit.get_transaction_data("ETC")
pykorbit.get_transaction_data("XRP")
```

Constant
```python
import pykorbit

pykorbit.get_constants()
```

## Private API
```python
korbit = pykorbit.Korbit("key", "secret")
korbit.buy_market_order("ETC", 9800)
korbit.buy_limit_order("ETC", 30000, 0.1)
korbit.sell_limit_order("ETC", 45000, 0.28)
korbit.sell_market_order("ETC", 0.1)

# 주문 취소
korbit.cancel_order("BTC", 9000)
korbit.cancel_order("BTC", [1000, 10001])

# 지갑 잔고 조회
korbit.get_balances()

# 미체결 주문 내역
korbit.get_open_orders(currency="BTC", offset=0, limit=10)
```

### 참고 사항
가격은 `round(price, 4)`, 수량은 `round(qty, 8)` 등으로 처리하여 소수점 0.9999~를 방지해야 한다. 200.199999처럼 되면 주문 수탁이 거부된다.

## History
```python
print(pykorbit.get_ohlc("BTC", period=5))
print(pykorbit.get_ohlc("BTC", start="2018-02-01", end="2018-02-03"))

# hour
print(get_ohlc(symbol="BTC", timeunit='hour'))
print(get_ohlc(symbol="BTC", timeunit='hour', period=5))

# minute
print(get_ohlc(symbol="BTC", timeunit='minute'))
print(get_ohlc(symbol="BTC", timeunit='minute', period=5))
```


## WebSocket
WebSocket을 이용해서 `현재가`, `호가`, `체결`에 대한 정보를 수신합니다.
- 첫 번째 파라미터에는 수신정보를 입력하며 `ticker`, `orderbook`, `transaction`을 사용할 수 있습니다. 여러 개의 값을 리스트로 전달할 수 있습니다.
- 두 번째 파라미터는 구독할 필터를 설정하며 암호화폐의 티커를 입력합니다. 여러 개의 티커를 리스트로 전달할 수 있습니다.

#### 현재가
다음은 비트코인의 가격 정보를 조회합니다.
```python
from pykorbit import WebSocketManager
wm = WebSocketManager(['ticker'], ['btc_krw'])
```

```text
{'timestamp': 1622464868337, 'event': 'korbit:push-ticker', 'data': {'channel': 'ticker', 'currency_pair': 'btc_krw', 'timestamp': 1622464856589, 'last': '43130000', 'open': '43089000', 'bid': '43187000', 'ask': '43188000', 'low': '41165000', 'high': '43874000', 'volume': '236.72107637', 'change': '41000'}}
{'timestamp': 1622464870608, 'event': 'korbit:push-ticker', 'data': {'channel': 'ticker', 'currency_pair': 'btc_krw', 'timestamp': 1622464856589, 'last': '43130000', 'open': '43089000', 'bid': '43187000', 'ask': '43213000', 'low': '41165000', 'high': '43874000', 'volume': '236.72107637', 'change': '41000'}}
```

다음은 비트코인의 가격 정보를 조회합니다.
```python
wm = WebSocketManager(['ticker'], ['btc_krw', 'eth_krw'])
```
`currency_pair`에 `eth_krw`와 `btc_krw`가 전달된 것을 확인할 수 있습니다.
```text
{'timestamp': 1622465398322, 'event': 'korbit:push-ticker', 'data': {'channel': 'ticker', 'currency_pair': 'btc_krw', 'timestamp': 1622465393535, 'last': '43275000', 'open': '42570000', 'bid': '43276000', 'ask': '43314000', 'low': '41165000', 'high': '43874000', 'volume': '236.74144540', 'change': '705000'}}
{'timestamp': 1622465399124, 'event': 'korbit:push-ticker', 'data': {'channel': 'ticker', 'currency_pair': 'eth_krw', 'timestamp': 1622465391240, 'last': '2974000', 'open': '2860000', 'bid': '2975000', 'ask': '2979000', 'low': '2747000', 'high': '3053000', 'volume': '4473.97921559', 'change': '114000'}}
```

#### 호가
다음은 비트코인과 이더리움의 호가 정보를 조회합니다.
```python
wm = WebSocketManager(['orderbook'], ['btc_krw', 'eth_krw'])
```

```text
{'timestamp': 1622465474587, 'event': 'korbit:push-orderbook', 'data': {'channel': 'orderbook', 'currency_pair': 'eth_krw', 'timestamp': 1622465474514, 'bids': [{'price': '2979000', 'amount': '6.6956'}, {'price': '2976000', 'amount': '0.00170151'}, {'price': '2975000', 'amount': '4.28'}, {'price': '2972000', 'amount': '4.11'}, {'price': '2971000', 'amount': '0.495'}, {'price': '2968000', 'amount': '13.67'}, {'price': '2967000', 'amount': '2.52780586'}, {'price': '2966000', 'amount': '0.67430883'}, {'price': '2964000', 'amount': '2.53036437'}, {'price': '2960000', 'amount': '0.67567568'}, {'price': '2959000', 'amount': '109.97'}, {'price': '2957000', 'amount': '2.53635441'}, {'price': '2955000', 'amount': '0.10152284'}, {'price': '2954000', 'amount': '0.67704807'}, {'price': '2950000', 'amount': '0.10665491'}], 'asks': [{'price': '2980000', 'amount': '0.5'}, {'price': '2981000', 'amount': '0.5'}, {'price': '2982000', 'amount': '3.5948'}, {'price': '2983000', 'amount': '4.621584'}, {'price': '2984000', 'amount': '3.39'}, {'price': '2985000',
'amount': '0.02501337'}, {'price': '2998000', 'amount': '5.698'},
{'price': '2999000', 'amount': '17.78'}, {'price': '3000000', 'amount': '0.28001441'}, {'price': '3004000', 'amount': '8'}, {'price': '3005000', 'amount': '111.7364927'}, {'price': '3016000', 'amount': '41.17'}, {'price': '3025000', 'amount': '1.17304849'}, {'price': '3029000', 'amount': '0.149775'}, {'price': '3030000', 'amount': '2.60507466'}]}}
{'timestamp': 1622465474623, 'event': 'korbit:push-orderbook', 'data': {'channel': 'orderbook', 'currency_pair': 'eth_krw', 'timestamp': 1622465474565, 'bids': [{'price': '2979000', 'amount': '6.6956'}, {'price': '2976000', 'amount': '0.00170151'}, {'price': '2975000', 'amount': '4.28'}, {'price': '2972000', 'amount': '4.11'}, {'price': '2971000', 'amount': '0.495'}, {'price': '2968000', 'amount': '13.67'}, {'price': '2967000', 'amount': '2.52780586'}, {'price': '2966000', 'amount': '0.67430883'}, {'price': '2964000', 'amount': '2.53036437'}, {'price': '2960000', 'amount': '0.67567568'}, {'price': '2959000', 'amount': '109.97'}, {'price': '2957000', 'amount': '2.53635441'}, {'price': '2955000', 'amount': '0.10152284'}, {'price': '2954000', 'amount': '0.67704807'}, {'price': '2951000', 'amount': '2.54151135'}], 'asks': [{'price': '2980000', 'amount': '0.5'}, {'price': '2981000', 'amount': '0.5'}, {'price': '2982000', 'amount': '3.5948'}, {'price': '2983000', 'amount': '4.621584'}, {'price': '2984000', 'amount': '3.39'}, {'price': '2985000',
'amount': '0.02501337'}, {'price': '2998000', 'amount': '5.698'},
{'price': '2999000', 'amount': '19.18'}, {'price': '3000000', 'amount': '0.28001441'}, {'price': '3004000', 'amount': '8'}, {'price': '3005000', 'amount': '111.7364927'}, {'price': '3016000', 'amount': '41.17'}, {'price': '3025000', 'amount': '1.17304849'}, {'price': '3029000', 'amount': '0.149775'}, {'price': '3030000', 'amount': '2.60507466'}]}}
```

#### 체결
다음은 리플의 체결 정보를 조회합니다.
```python
wm = WebSocketManager(['orderbook'], ['xrp_krw'])
```

```text
{'timestamp': 1622465633612, 'event': 'korbit:push-transaction', 'data': {'channel': 'transaction', 'currency_pair': 'xrp_krw', 'timestamp': 1622465633475, 'price': '1181', 'amount': '1119.712932',
'taker': 'buy'}}
```

#### 통합 조회
한 번에 여러 정보를 조회할 수 있습니다.
```python
wm = WebSocketManager(['transaction', 'ticker'], ['xrp_krw'])
```

```text
{'timestamp': 1622465723455, 'event': 'korbit:push-transaction', 'data': {'channel': 'transaction', 'currency_pair': 'xrp_krw', 'timestamp': 1622465723390, 'price': '1179', 'amount': '384.866301', 'taker': 'sell'}}
{'timestamp': 1622465723556, 'event': 'korbit:push-ticker', 'data': {'channel': 'ticker', 'currency_pair': 'xrp_krw', 'timestamp': 1622465723390, 'last': '1179', 'open': '1052', 'bid': '1179', 'ask': '1181', 'low': '1035', 'high': '1220', 'volume': '10271255.974425', 'change': '127'}}
```
