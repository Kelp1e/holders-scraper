from typing import List, Dict

from requests import Response

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain
from holders.holders import Holders, Holder

# Types
HolderData = List[Dict[str, str]]
HolderObjectResponse = Dict[str, str]


class TRX(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit: int = 200

    def get_token_metadata(self, contract_address: str) -> Response:
        url: str = "https://apilist.tronscanapi.com/api/token_trc20"

        params: dict = {
            "contract": contract_address
        }

        response: Response = self.request("get", url, params=params)

        return response

    def get_total_supply(self, contract_address: str) -> int:
        response: Response = self.get_token_metadata(contract_address)

        trc20_tokens: List[Dict] = response.json().get("trc20_tokens")

        if not trc20_tokens:
            raise InvalidChain()

        token_info: dict = trc20_tokens[0]

        decimals: int = token_info.get("decimals")

        total_supply: int = int(token_info.get("total_supply_with_decimals")[:-decimals])

        return total_supply

    def get_decimals(self, contract_address: str) -> int:
        response: Response = self.get_token_metadata(contract_address)

        trc20_tokens: List[Dict] = response.json().get("trc20_tokens")

        if not trc20_tokens:
            raise InvalidChain()

        token_info: dict = trc20_tokens[0]

        decimals: int = token_info.get("decimals")

        return decimals

    def get_holders_response(self, contract_address: str, fingerprint: str) -> Response:
        url = f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens"

        params = {
            "limit": self.limit,
            "fingerprint": fingerprint # To get the next holders page
        }

        headers: dict = {
            "accept": "application/json",
        }

        response: Response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders_data(self, contract_address: str, market_id: int) -> HolderData:
        pages: int = self.get_pages(market_id, self.limit)

        fingerprint: str = ""  # To get the next holders page

        holder_data: HolderData = []

        for page in range(1, pages + 1):
            response: Response = self.get_holders_response(contract_address, fingerprint)

            data: HolderData = response.json().get("data")
            meta = response.json().get("meta")

            fingerprint: str = meta.get("fingerprint")

            holder_data.extend(data)

        return holder_data

    def get_holders(self, contract_address: str, market_id: int, multi_total_supply: int):
        holders_data: HolderData = self.get_holders_data(contract_address, market_id)

        decimals: int = self.get_decimals(contract_address)

        holders = [self.get_holder(obj, decimals) for obj in holders_data]

        return Holders(holders, multi_total_supply)

    @staticmethod
    def get_holder(obj: Dict[str, str], decimals: int):
        address: str = list(obj.keys())[0]
        balance: int = int(str(list(obj.values())[0])[:-decimals])

        holder: Holder = Holder(address, balance, "trx")

        return holder
