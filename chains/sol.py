from typing import List, Dict, Union

from requests import Response

from base.scraper import BaseScraper
from exceptions.chains import PageOutOfRange, InvalidChain
from exceptions.holders import InvalidAddress
from holders.holders import Holders, Holder

# Types
HoldersData = List[Dict[str, Union[str, int]]]
HoldersList = List[Holder]
HolderResponseObject = Dict[str, Union[str, int]]


class SOL(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit: int = 50

    def get_token_metadata(self, contract_address: str) -> Response:
        url = "https://api.solscan.io/account"

        params: dict = {
            "address": contract_address
        }

        headers: dict = {
            "accept": "application/json"
        }

        response: Response = self.request("get", url, params=params, headers=headers)

        return response

    def get_total_supply(self, contract_address: str) -> int:
        response: Response = self.get_token_metadata(contract_address)

        data: dict = response.json().get("data", {})

        token_info: dict = data.get("tokenInfo")

        if not token_info:
            raise InvalidChain()

        decimals: int = token_info.get("decimals")

        total_supply_with_decimals: str = token_info.get("supply")

        if total_supply_with_decimals == "0":
            raise InvalidChain()

        total_supply: int = int(total_supply_with_decimals[:-decimals])

        return total_supply

    def get_holders_response(self, contract_address: str, offset: int = 0) -> Response:
        url: str = "https://api.solscan.io/token/holders"

        params: dict = {
            "token": contract_address,
            "offset": offset,
            "size": self.limit
        }

        headers: dict = {
            "accept": "application/json"
        }

        response: Response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders_data(self, contract_address: str, offset: int = 0) -> HoldersData:
        response: Response = self.get_holders_response(contract_address, offset)

        data: dict = response.json().get("data")

        if not data:
            raise PageOutOfRange()

        result: HoldersData = data.get("result")

        return result

    def get_holders(self, contract_address: str, market_id: int) -> List[Holder]:
        pages: int = self.get_pages(market_id, self.limit)

        offset: int = 0

        holders_data: HoldersData = []

        for page in range(1, pages + 1):
            try:
                holders_data.extend(self.get_holders_data(contract_address, offset))

                offset += self.limit
            except PageOutOfRange:
                break

        holders: List[Holder] = []

        if not holders_data:
            raise InvalidChain()

        for obj in holders_data:
            try:
                holders.append(self.get_holder(obj))
            except InvalidAddress:
                continue
            except ValueError:
                break

        return holders

    @staticmethod
    def get_holder(obj: HolderResponseObject) -> Holder:
        decimals: int = obj.get("decimals")

        address: str = obj.get("address")

        balance: int = int(str(obj.get("amount"))[:-decimals])

        chain: str = "sol"

        holder: Holder = Holder(address, balance, chain)

        return holder
