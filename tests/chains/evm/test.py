from chains.evm import EVM

market_id = 1
multi_total_supply = 1000000

chain = "ethereum"
contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"

page = 1

evm = EVM()

print("get_correct_chain:", evm.get_correct_chain(chain=chain))
print("get_chain_id:", evm.get_chain_id(chain=chain))
print("get_token_metadata:", evm.get_token_metadata(chain=chain, contract_address=contract_address))
print("get_total_supply:", evm.get_total_supply(chain=chain, contract_address=contract_address))
print("get_holders_response:", evm.get_holders_response(chain=chain, contract_address=contract_address, page=page))
print("get_holders_data:", evm.get_holders_data(chain=chain, contract_address=contract_address, page=page))

# Get holders
print("get_holders", evm.get_holders(
    chain=chain, contract_address=contract_address, market_id=market_id, multi_total_supply=multi_total_supply
))
