from holders.holders import Holder, Holders

h1 = Holder("aBc", "5", "btc")
h2 = Holder("Abc", "10", "eth")
h3 = Holder("bca", "10", "pol")

print(Holders([h1, h2, h3], 100))
