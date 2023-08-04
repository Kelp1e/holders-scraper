from chains.evm import EVM

evm = EVM()

chain = "ethereum"
contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"

response = evm.get_token_metadata(chain, contract_address)
print(response.json())