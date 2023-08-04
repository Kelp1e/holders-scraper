from chains.evm import EVM

evm = EVM()

chain = "ethereum"
contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
page = 1

total_supply = evm.get_total_supply(chain, contract_address)
print(total_supply)
