from exceptions.holders import InvalidHoldersList, InvalidAddress


class Holder:
    def __init__(self, address, balance, percents_of_coins):
        self.address = address
        self.balance = int(balance)
        self.percents_of_coins = float(percents_of_coins)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not value:
            raise InvalidAddress()

        self._address = str(value).lower()

    def __hash__(self):
        return hash(self.address)

    def __dict__(self):
        return {
            "address": self.address,
            "balance": self.balance,
            "percents_of_coins": self.percents_of_coins
        }

    def __str__(self):
        return f"Holder(address={self.address}, balance={self.balance}, percents_of_coins={self.percents_of_coins})"

    def __repr__(self):
        return f"Holder(address={self.address}, balance={self.balance}, percents_of_coins={self.percents_of_coins})"


class Holders:
    def __init__(self, holders=None):
        self.holders = self.compress(holders) if holders else []

    def compress(self, holders):
        if not holders:
            return []

        if not all(isinstance(holder, Holder) for holder in holders):
            raise InvalidHoldersList()

        return self.__compress(holders)

    def append(self, holder):
        if not isinstance(holder, Holder):
            raise InvalidHoldersList()

        self.holders.append(holder)
        self.holders = self.__compress(self.holders)

    def extend(self, holders):
        if not isinstance(holders, Holders):
            raise InvalidHoldersList()

        self.holders.extend(holders)
        self.holders = self.__compress(self.holders)

    def filter_by_balance(self):
        sorted_holders = sorted(self.holders, key=lambda holder: holder.balance, reverse=True)

        return Holders(sorted_holders)

    @staticmethod
    def __compress(holders):
        address_dict = {}

        for holder in holders:
            address = holder.address

            if address in address_dict:
                address_dict[address].balance += holder.balance
                address_dict[address].percents_of_coins += holder.percents_of_coins
            else:
                address_dict[address] = Holder(**holder.__dict__())  # TODO kwargs

        return list(address_dict.values())

    def __getitem__(self, item):
        return self.holders[item]

    def __iter__(self):
        return iter(self.holders)

    def __len__(self):
        return len(self.holders)

    def __str__(self):
        return f"{len(self.holders)} Holders({self.holders})"

    def __repr__(self):
        return f"{len(self.holders)} Holders({self.holders})"
