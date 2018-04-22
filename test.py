import pykorbit

#-----------------------------------------------------------------------------------------------------------------------
#  Public API
#-----------------------------------------------------------------------------------------------------------------------
print(pykorbit.get_current_price("btc_krw"))
print(pykorbit.get_market_detail("btc_krw"))
print(pykorbit.get_orderbook("btc_krw"))
print(pykorbit.get_transaction_data("btc_krw"))
print(pykorbit.get_constants())

#-----------------------------------------------------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------------------------------------------------
f = open("keys.csv")
lines = f.readlines()
f.close()
key = lines[1].split(',')[0]
secret = lines[1].split(',')[1]
korbit = pykorbit.Korbit("your-email@gmail.com", "your-pass-word", key, secret)

# 주문 제약 조건
print(korbit._get_tick_size("btc_krw"))
print(korbit._get_quantity_min_max("btc_krw"))
print(korbit._get_price_min_max("btc_krw"))

#-----------------------------------------------------------------------------------------------------------------------
# history
#-----------------------------------------------------------------------------------------------------------------------
print(pykorbit.get_daily_ohlc("BTC", start="2018-02-01", end="2018-02-03"))
print(pykorbit.get_daily_ohlc("BTC", period=5))
print(pykorbit.get_daily_ohlc("BTC", end="2018-02-03", period=5))
