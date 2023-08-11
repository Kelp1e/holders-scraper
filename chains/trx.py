from typing import List, Dict

from requests import Response

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain

# Types
HolderData = List[Dict[str, str]]


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

    def get_holders_response(self, contract_address: str, fingerprint: str = "") -> Response:
        url: str = f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens"

        headers: dict = {
            "accept": "application/json",
            "fingerprint": fingerprint
        }

        response: Response = self.request("get", url, headers=headers)

        return response

    def get_holders_data(self, contract_address: str, market_id: int):
        # TODO HOLDERS DATA
        pages: int = self.get_pages(market_id, self.limit)

        fingerprint: str = ""

        holders_data: HolderData = []

        for page in range(1, pages + 1):
            response: Response = self.get_holders_response(contract_address, fingerprint)

            data: list = response.json().get("data")
            metadata: dict = response.json().get("meta")

            holders_data.extend(data)

            fingerprint: str = metadata.get("fingerprint")

        return holders_data
