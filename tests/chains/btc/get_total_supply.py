from chains.btc import BTC

btc = BTC()

response = btc.get_total_supply("bitcoin")
print(response)
