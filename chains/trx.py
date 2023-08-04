import os
import random

from dotenv import load_dotenv

from base.scraper import BaseScraper
from holders.holders import Holder, Holders

load_dotenv()

TRON_API_KEYS = os.getenv("TRON_API_KEYS").split()


class TRX(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_holders_response(self, url):
        tron_api_key = random.choice(TRON_API_KEYS)

        headers = {
            "accept": "application/json",
            "TRON-PRO-API-KEY": tron_api_key,
        }

        response = self.request("get", url, headers=headers)

        return response

    # Recursive
    def get_holders_data(self, url, pages, depth=1):
        if depth > pages:
            return []

        response = self.get_holders_response(url)

        if response.status_code == 200:
            json = response.json()
            result = json["data"]
            next_page_url = json["meta"]["links"]["next"]

            result.extend(self.get_holders_data(next_page_url, pages, depth + 1))

            return result
        else:
            return []

    def get_holders(self, contract_address, market_id):
        url = self.get_url(contract_address)

        pages = self.__get_pages(market_id)

        holders_data = self.get_holders_data(url, pages)

        holders = Holders([self.get_holder(obj) for obj in holders_data])

        return holders

    @staticmethod
    def get_url(contract_address):
        return f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens?limit=200"

    @staticmethod
    def get_holder(obj):
        address = list(obj.keys())[0]
        balance = list(obj.values())[0]
        percents_of_coins = 0  # TODO

        holder = Holder(address, balance, percents_of_coins)

        return holder

    @staticmethod
    def __get_pages(market_id):
        # TODO
        market_id = int(market_id)

        if market_id > 0:
            return 5
