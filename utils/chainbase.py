def get_chain_id(chain):
    chain = chain.lower()

    chain_id = {
        "ethereum": 1,
        "polygon": 137,
        "bsc": 56,
        "avalanche": 43114,
        "arbitrum-one": 42161,
        "optimism": 10
    }

    if chain not in chain_id.keys():
        return

    return chain_id[chain]
