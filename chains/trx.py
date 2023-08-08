import os
import random

from dotenv import load_dotenv

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain
from exceptions.holders import InvalidAddress
from holders.holders import Holder, Holders

load_dotenv()

TRON_API_KEYS = os.getenv("TRON_API_KEYS").split()


class TRX(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_token_metadata(self, contract_address):
        url = "https://apilist.tronscanapi.com/api/token_trc20"

        params = {
            "contract": contract_address,
        }

        response = self.request("get", url, params)

        return response

    def get_total_supply(self, contract_address):
        response = self.get_token_metadata(contract_address)

        data = response.json()

        trc20_tokens = data.get("trc20_tokens")

        if not trc20_tokens:
            raise InvalidChain()

        total_supply = trc20_tokens[0].get("total_supply_with_decimals")

        return total_supply

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
            try:
                json = response.json()
                result = json["data"]
                next_page_url = json["meta"]["links"]["next"]

                result.extend(self.get_holders_data(next_page_url, pages, depth + 1))

                return result
            except KeyError:
                raise InvalidChain()
        else:
            return []

    def get_holders(self, contract_address, market_id):
        holders = []

        url = self.get_url(contract_address)

        pages = self.__get_pages(market_id)

        total_supply = self.get_total_supply(contract_address)

        holders_data = self.get_holders_data(url, pages)

        for obj in holders_data:
            try:
                holder = self.__get_holder(obj, total_supply)
            except InvalidAddress:
                continue

            holders.append(holder)

        return Holders(holders)

    @staticmethod
    def get_url(contract_address):
        return f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens?limit=200"

    def __get_holder(self, obj, total_supply):
        address = list(obj.keys())[0]
        balance = list(obj.values())[0]
        percents_of_coins = self.get_percents_of_coins(balance, total_supply)

        holder = Holder(address, balance, percents_of_coins, "trx")

        return holder

    @staticmethod
    def __get_pages(market_id):
        # TODO
        market_id = int(market_id)

        if market_id > 0:
            return 5
