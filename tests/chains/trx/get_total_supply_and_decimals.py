from chains.trx import TRX

trx = TRX()

total_supply, decimals = trx.get_total_supply_and_decimals("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
print(total_supply, decimals, type(total_supply))
