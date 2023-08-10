from chains.btc import BTC

btc = BTC()
market_id = 500

holders = btc.get_holders("bitcoin", market_id).filter_by_balance(market_id)
print(holders)
