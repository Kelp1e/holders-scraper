from chains.evm import EVM

evm = EVM()

chain = "ethereum"
contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
page = 1

holders_data = evm.get_holders_data(chain, contract_address, page)
print(holders_data)
