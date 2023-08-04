from chains.btc import BTC

btc = BTC()

holders = btc.get_holders("bitcoin", 1)
print(holders)
