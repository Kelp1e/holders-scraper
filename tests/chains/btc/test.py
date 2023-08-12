from chains.btc import BTC

market_id = 666

slug_name = "bitcoin"

btc = BTC()

print("get_holders:", len(btc.get_holders(slug_name, market_id)))
