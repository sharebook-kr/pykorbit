# korbit-api
Python Wrapper for Korbit API

## Installation
```sh
pip install pykorbit
```

## Public API
Ticker

```python
import pykorbit

pykorbit.get_current_price("btc_krw")
pykorbit.get_current_price("bch_krw")
pykorbit.get_current_price("btg_krw")
pykorbit.get_current_price("eth_krw")
pykorbit.get_current_price("etc_krw")
pykorbit.get_current_price("xrp_krw")
```

Detailed Ticker
```python
import pykorbit

pykorbit.get_market_detail("btc_krw")
pykorbit.get_market_detail("bch_krw")
pykorbit.get_market_detail("btg_krw")
pykorbit.get_market_detail("eth_krw")
pykorbit.get_market_detail("etc_krw")
pykorbit.get_market_detail("xrp_krw")
```

Transaction
```python
import pykorbit

pykorbit.get_transaction_data("btc_krw")
pykorbit.get_transaction_data("bch_krw")
pykorbit.get_transaction_data("btg_krw")
pykorbit.get_transaction_data("eth_krw")
pykorbit.get_transaction_data("etc_krw")
pykorbit.get_transaction_data("xrp_krw")
```

Constant
```python
import pykorbit

pykorbit.get_constants()
```

## Private API
```python
korbit = pykorbit.Korbit("your-email@gmail.com", "your-pass-word", "key", "secret")
korbit.buy_market_order(btc_rkw", 1)
```

## History
```python
print(pykorbit.get_daily_ohlc("BTC", period=5))
print(pykorbit.get_daily_ohlc("BTC", start="2018-02-01", end="2018-02-03")) 
```
