# korbit-api
Python Wrapper for Korbit API

## Installation
```sh
pip install pykorbit
```

## Basic Usage
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

copy the keys.csv file into the current directory
