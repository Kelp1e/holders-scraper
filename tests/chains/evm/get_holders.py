from chains.evm import EVM

evm = EVM()

chain = "ethereum"
contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
market_id = 1

holders = evm.get_holders(chain, contract_address, market_id)
print(holders)
