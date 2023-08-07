from chains.trx import TRX

trx = TRX()

total_supply = trx.get_total_supply("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
print(total_supply)
