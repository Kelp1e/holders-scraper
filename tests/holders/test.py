from holders.holders import Holder, Holders

h1 = Holder("aBc", "5", "btc")
h2 = Holder("Abc", "10", "eth")
h3 = Holder("bca", "20", "pol")

holders1 = Holders([h1, h2, h3], 100, 1)
print(holders1)

holders2 = Holders(holders1, 200, 1)
print(holders2)


