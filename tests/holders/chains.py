from holders.holders import Holder, Holders

h1 = Holder("123", "100", 1.0, "trx")
h2 = Holder("123", "200", 2.0, "btc")

holders = Holders([h1, h2])
print(holders)
