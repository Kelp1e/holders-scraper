from chains.btc import BTC

btc = BTC()

holders = btc.get_holders_data("bitcoin", 1)
print(holders)
