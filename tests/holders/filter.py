from holders.holders import Holder, Holders

holders = Holders([
    Holder("123", "100", "2.0", "btc"),
    Holder("234", "123", "2.0", "btc"),
    Holder("345", "234", "2.0", "pol"),
    Holder("456", "345", "2.0", "pol"),
    Holder("567", "456", "2.0", "avax"),
    Holder("678", "567", "2.0", "avax"),
])
print(holders)
