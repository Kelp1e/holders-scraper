from chains.btc import BTC

btc = BTC()

print(btc.get_pages(100, 100))
print(btc.get_pages(500, 100))
print(btc.get_pages(2500, 100))
