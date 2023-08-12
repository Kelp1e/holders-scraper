from base.limits import Limits
from exceptions.holders import InvalidAddress, InvalidHoldersList


class Holder:
    def __init__(self, address, balance, chain):
        self.address = address
        self.balance = balance
        self.percents_of_coins = None
        self.chains = chain

    # Address property
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise InvalidAddress(value)

        self._address = value.lower()

    # Balance property
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = int(float(value))

    # Chains property
    @property
    def chains(self):
        return self._chains

    @chains.setter
    def chains(self, value):
        self._chains = {value: {"a": self.balance}}

    # Validators
    def __validate_holder(self, other):
        if not isinstance(other, Holder):
            raise TypeError(
                "Can only perform operation with another Holder object"
            )

        if self.address != other.address:
            raise ValueError(
                f"Cannot perform operation with Holders having different addresses: [{self.address}, {other.address}]"
            )

    # Add operations
    def __iadd__(self, other):
        self.__validate_holder(other)

        self.balance += other.balance
        self.chains.update(other.chains)

        return self

    # Strings to display data
    def __str__(self):
        return f"Holder(" \
               f"address={self.address}, " \
               f"balance={self.balance}, " \
               f"percents_of_coins={self.percents_of_coins}, " \
               f"chains={self.chains})"

    def __repr__(self):
        return f"Holder(" \
               f"address={self.address}, " \
               f"balance={self.balance}, " \
               f"percents_of_coins={self.percents_of_coins}, " \
               f"chains={self.chains})"


class Holders(Limits):
    def __init__(self, holders, total_supply, market_id):
        # Don't change the location of the attributes
        super().__init__()
        self.total_supply = total_supply
        self.market_id = market_id
        self.holders = holders

    # Holders property
    @property
    def holders(self):
        return self._holders

    @holders.setter
    def holders(self, holders_list):
        if not all(isinstance(holder, Holder) for holder in holders_list):
            raise InvalidHoldersList()

        # Compress the same addresses
        self._holders = self.compress(holders_list)

        # Calculate percents_of_coins for holder
        for holder in self._holders:
            holder.percents_of_coins = round(float(holder.balance / self.total_supply * 100), 3)

        # Filter by balance and get correct size
        self._holders = self.filter_by_balance()[:self.get_limit(self.market_id)]

    # Total supply property
    @property
    def total_supply(self):
        return self._total_supply

    @total_supply.setter
    def total_supply(self, value):
        self._total_supply = int(value)

    # Market id property
    @property
    def market_id(self):
        return self._market_id

    @market_id.setter
    def market_id(self, value):
        self._market_id = int(value)

    # For iterations in loop
    def __iter__(self):
        return iter(self.holders)

    # Strings to display data
    def __str__(self):
        return f"Holders[{len(self.holders)}][{self.holders}]"

    def __repr__(self):
        return f"Holders[{len(self.holders)}][{self.holders}]"

    # Utils
    @staticmethod
    def compress(holders_list):
        addresses_dict = {}

        for holder in holders_list:
            address = holder.address

            if address in addresses_dict:
                addresses_dict[address] += holder
            else:
                addresses_dict[address] = holder

        return list(addresses_dict.values())

    # Filter by balance
    def filter_by_balance(self):
        sorted_holders = sorted(self.holders, key=lambda holder: holder.balance, reverse=True)

        return sorted_holders
