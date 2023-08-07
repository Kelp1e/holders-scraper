from chains.sol import SOL

sol = SOL()

response = sol.get_holders_response("ATZERmcPfopS9vGqw9kxqRj9Bmdi3Z268nHXkGsMa3Pf")
print(response.json())
