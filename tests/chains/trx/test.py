from chains.trx import TRX

market_id = 1

contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

trx = TRX()

total_supply = trx.get_total_supply(contract_address)

print("get_total_supply:", trx.get_total_supply(contract_address))
# print("get_holders_response:", trx.get_holders_response(contract_address, ""))
# print("get_holders_data:", trx.get_holders_data(contract_address, market_id))
print("get_holders:", trx.get_holders(contract_address, market_id))

