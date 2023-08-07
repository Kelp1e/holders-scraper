from chains.sol import SOL

sol = SOL()

holders = sol.get_holders("ATZERmcPfopS9vGqw9kxqRj9Bmdi3Z268nHXkGsMa3Pf", 1)
print(holders)
