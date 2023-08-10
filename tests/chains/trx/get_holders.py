from chains.trx import TRX

trx = TRX()

contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
market_id = 2600

holders = trx.get_holders(contract_address, market_id).filter_by_balance(market_id)
print(holders)
