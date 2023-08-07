from chains.sol import SOL

sol = SOL()

response = sol.get_token_metadata("ATZERmcPfopS9vGqw9kxqRj9Bmdi3Z268nHXkGsMa3Pf")
print(response, response.status_code, response.json())
