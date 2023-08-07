class InvalidChain(Exception):
    def __init__(self):
        super().__init__("Invalid chain")
