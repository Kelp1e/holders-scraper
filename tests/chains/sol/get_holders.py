from chains.sol import SOL

sol = SOL()
market_id = 2500

holders = sol.get_holders("ATZERmcPfopS9vGqw9kxqRj9Bmdi3Z268nHXkGsMa3Pf", market_id).filter_by_balance(market_id)
print(holders)
