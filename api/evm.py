import os

from dotenv import load_dotenv

from base.base_scraper import BaseScraper

load_dotenv()

EVM_API_KEY = os.getenv("EVM_API_KEY")


class Evm(BaseScraper):
    def __init__(self):
        super().__init__()
        self.headers = {"accept": "application/json", "x-api-key": EVM_API_KEY}

    def get_token_metadata(self, chain: str, contract_address: str):
        url = "https://api.chainbase.online/v1/token/top-holders"

        params = {
            "chain_id": self.__get_chain_id(chain),
            "contract_address": contract_address
        }

        response = self.request("get", url, params=params, headers=self.headers)

        return response

    def get_holders(self, chain: str, contract_address: str, page: int = 1):
        url = "https://api.chainbase.online/v1/token/top-holders"

        correct_chain = self._get_correct_chain(chain)
        chain_id = self.__get_chain_id(correct_chain)

        params = {
            "chain_id": chain_id,
            "contract_address": contract_address,
            "limit": 100,
            "page": page,
        }

        response = self.request("get", url, params=params, headers=self.headers)

        return response

    def get_holders_data(self, chain: str, contract_address: str, market_id: str or int):
        holders_data = []

        pages = self.__get_pages(market_id)

        for page in range(1, pages + 1):
            response = self.get_holders(chain, contract_address, page)

            if response:
                holders_data.extend(response.json().get("data"))

        return holders_data

    @staticmethod
    def __get_chain_id(chain: str):
        chain_id = {
            "ethereum": "1",
            "polygon": "137",
            "bsc": "56",
            "avalanche": "43114",
            "arbitrum-one": "42161",
            "optimism": "10"
        }

        return chain_id[chain]

    @staticmethod
    def __get_pages(market_id: str or int):
        if market_id <= 500:
            return 10

        if 500 <= market_id <= 2500:
            return 5

        if 2500 <= market_id:
            return 3
