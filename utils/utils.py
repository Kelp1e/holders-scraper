class Utils:
    @staticmethod
    def get_from(contract, *args):
        return [contract.get(arg) for arg in args]
