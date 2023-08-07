from chains.trx import TRX

trx = TRX()

response = trx.get_token_metadata("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
print(response)
