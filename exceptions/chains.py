class InvalidChain(Exception):
    def __init__(self):
        super().__init__("Invalid chain")


class BalanceLessThenZero(Exception):
    def __init__(self):
        super().__init__("Balance less then 0")
