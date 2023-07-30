import os

from dotenv import load_dotenv

from base.base_scraper import BaseScraper

load_dotenv()

TRON_API_KEY = os.getenv("TRON_API_KEY")


class Tron(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_holders(self, contract_address: str, page: int):
        url = f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens"

        headers = {
            "accept": "application/json",
            "TRON-PRO-API-KEY": TRON_API_KEY,
            "limit": "200",
            "page": str(page)
        }

        response = self.request("get", url, headers=headers)

        return response

    def get_holders_data(self, contract_address: str, market_id: str or int):
        holders_data = []

        pages = self.__get_pages(market_id)

        for page in range(1, pages + 1):
            response = self.get_holders(contract_address, page)

            if response:
                holders_data.extend(response.json().get("data"))

        return holders_data

    @staticmethod
    def __get_pages(market_id: str or int):
        # TODO
        if market_id > 0:
            return 1
