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
korbit = pykorbit.Korbit("your-email@gmail.com", "your-pass-word", "key", "secret")
korbit.buy_market_order("ETC", 9800)
korbit.buy_limit_order("ETC", 30000, 0.1)
korbit.sell_limit_order("ETC", 45000, 0.28)
korbit.sell_market_order("ETC", 0.1)

# 주문 취소 
korbit.cancel_order("BTC", 9000)
korbit.cancel_order("BTC", [1000, 10001])

# 지갑 잔고 조회
korbit.get_balances()
```

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
