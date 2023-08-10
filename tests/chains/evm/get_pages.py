from chains.evm import EVM

evm = EVM()
print(evm.get_pages(100))
print(evm.get_pages(600))
print(evm.get_pages(2600))