from chains.sol import SOL

market_id = 1
multi_total_supply = 10000000000000

contract_address = "ATZERmcPfopS9vGqw9kxqRj9Bmdi3Z268nHXkGsMa3Pf"

sol = SOL()

# print("get_token_metadata:", sol.get_token_metadata(contract_address))
# print("get_total_supply:", sol.get_total_supply(contract_address))
# print("get_holders_response:", sol.get_holders_response(contract_address, 1))
# print("get_holders_data:", sol.get_holders_data(contract_address))
print("get_holders:", sol.get_holders(contract_address, market_id))
