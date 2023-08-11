class InvalidHoldersList(Exception):
    def __init__(self):
        super().__init__("Holders should contain only objects of type Holder.")


class InvalidAddress(Exception):
    def __init__(self, address):
        super().__init__(f"Holder must have an address. Address: {address}")
