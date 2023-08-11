class InvalidChain(Exception):
    def __init__(self):
        super().__init__("Invalid chain")


class BalanceLessThanZero(Exception):
    def __init__(self):
        super().__init__("Balance less then 0")


class PageOutOfRange(Exception):
    def __init__(self, chain, contract_address, page):
        super().__init__(f"Page {page} out of range for [chain: {chain},  contract_address: {contract_address}]")


class LimitOutOfRange(Exception):
    def __init__(self, chain, contract_address, limit):
        super().__init__(f"Limit {limit} out of range for [chain: {chain},  contract_address: {contract_address}]")