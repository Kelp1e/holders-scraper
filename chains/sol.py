from base.scraper import BaseScraper
from exceptions.chains import InvalidChain, BalanceLessThanZero
from exceptions.holders import InvalidAddress
from holders.holders import Holder, Holders


class SOL(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit = 50

    def get_token_metadata(self, contract_address):
        url = f"https://api.solscan.io/account"

        params = {
            "address": contract_address
        }

        response = self.request("get", url, params=params)

        if not response.json().get("data"):
            raise InvalidChain()

        return response

    def get_total_supply(self, contract_address):
        response = self.get_token_metadata(contract_address)

        data = response.json().get("data")

        token_info = data.get("tokenInfo")

        if not token_info:
            raise InvalidChain()

        decimals = token_info.get("decimals")
        total_supply = token_info.get("supply")[:-decimals]

        return total_supply

    def get_holders_response(self, contract_address, offset=0):
        url = "https://api.solscan.io/token/holders"

        params = {
            "token": contract_address,
            "offset": offset,
            "size": self.limit
        }

        response = self.request("get", url, params=params)

        if not response.json().get("data"):
            raise InvalidChain()

        return response

    def get_holders_data(self, contract_address, total_supply, offset=0):
        holders_data = []

        response = self.get_holders_response(contract_address, offset)

        for obj in response.json().get("data").get("result"):
            try:
                holder = self.__get_holder(obj, total_supply)
                holders_data.append(holder)
            except InvalidAddress:
                continue
            except BalanceLessThanZero:
                break

        return Holders(holders_data)

    def get_holders(self, contract_address, market_id):
        holders = []

        offset = 0

        pages = self.get_pages(market_id, self.limit)

        total_supply = self.get_total_supply(contract_address)

        for page in range(1, pages + 1):
            holders_data = self.get_holders_data(contract_address, total_supply, offset)

            holders.extend(holders_data)

            offset += 50

        return Holders(holders)

    def __get_holder(self, obj, total_supply):
        decimals = obj.get("decimals")

        address = obj.get("address")
        balance = str(obj.get("amount"))[:-decimals]

        if not balance:
            raise BalanceLessThanZero()

        percents_of_coins = self.get_percents_of_coins(balance, total_supply)

        holder = Holder(address, balance, percents_of_coins, "sol")

        return holder


