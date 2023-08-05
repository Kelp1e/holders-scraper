from chains.trx import TRX
from exceptions.chains.exceptions import InvalidChain

trx = TRX()

contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
market_id = 1

holders = trx.get_holders(contract_address, market_id)
print(holders)
