import os
import random

from dotenv import load_dotenv

from base.base_scraper import BaseScraper

load_dotenv()

TRON_API_KEYS = os.getenv("TRON_API_KEYS").split()


class Tron(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_holders(self, contract_address: str, page: int):
        url = f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens"

        params = {
            "limit": "200",
            "page": page
        }

        headers = {
            "accept": "application/json",
            "TRON-PRO-API-KEY": random.choice(TRON_API_KEYS),
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders_data(self, contract_address: str, market_id: str or int):
        holders_data = []

        pages = self.__get_pages(market_id)

        for page in range(1, pages + 1):
            response = self.get_holders(contract_address, page)

            if response:
                data = response.json().get("data")

                for obj in data:
                    holder = {}

                    address = list(obj.keys())[0]
                    balance = list(obj.values())[0]

                    holder["address"] = address
                    holder["balance"] = balance
                    holder["percents_of_coins"] = 0

                    holders_data.append(holder)

        return holders_data

    def get_token_metadata(self, contract_address):
        pass

    @staticmethod
    def __get_pages(market_id: str or int):
        market_id = int(market_id)

        if market_id > 0:
            return 5
