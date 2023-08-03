class Holders:
    def __init__(self, holders=None):
        self.holders = self.__compress(holders) if holders else []

    @staticmethod
    def __compress(holders):
        address_dict = {}

        if not holders:
            return

        for holder in holders:
            address = holder.address

            if address in address_dict:
                address_dict[address].balance += holder.balance
                address_dict[address].percents_of_coins += holder.percents_of_coins
            else:
                address_dict[address] = Holder(address, holder.balance, holder.percents_of_coins)

        return list(address_dict.values())

    def append(self, holder):
        if isinstance(holder, Holder):
            self.holders.append(holder)
            self.holders = self.__compress(self.holders)
        else:
            raise TypeError("Only objects of type Holder can be appended.")

    def extend(self, holders):
        if isinstance(holders, Holders):
            self.holders.extend(holders)
            self.holders = self.__compress(self.holders)
        else:
            raise TypeError("Only objects of type Holders can be extended.")

    def __iter__(self):
        return iter(self.holders)

    def __contains__(self, item):
        return item in self.holders

    def __len__(self):
        return len(self.holders)

    def __getitem__(self, item):
        return self.holders[item]

    def __setitem__(self, key, value):
        self.holders[key] = value

    def __str__(self):
        return f"Holders({self.holders})"

    def __repr__(self):
        return f"Holders({self.holders})"


class Holder:
    def __init__(self, address, balance, percents_of_coins):
        self.address = address.lower()
        self.balance = int(balance)
        self.percents_of_coins = float(percents_of_coins)

    def __hash__(self):
        return hash(self.address)

    def __eq__(self, other):
        if isinstance(other, Holder):
            return self.address == other.address

        return self.address == str(other).lower()

    def __dict__(self):
        return {
            'address': self.address,
            'balance': self.balance,
            'percents_of_coins': self.percents_of_coins
        }

    def __str__(self):
        return f"Holder(address={self.address}, balance={self.balance}, percents_of_coins={self.percents_of_coins})"

    def __repr__(self):
        return f"Holder(address={self.address}, balance={self.balance}, percents_of_coins={self.percents_of_coins})"
