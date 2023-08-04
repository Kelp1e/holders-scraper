class InvalidHoldersList(Exception):
    def __init__(self):
        super().__init__("Holders should contain only objects of type Holder.")
