import os
import random

from dotenv import load_dotenv

from base.base_scraper import BaseScraper
from exceptions.holders_not_found import HoldersNotFoundError
from holders.holders import Holder, Holders

load_dotenv()

TRON_API_KEYS = os.getenv("TRON_API_KEYS").split()


class Tron(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_holders(self, contract_address: str, page: int):
        url = f"https://api.trongrid.io/v1/contracts/{contract_address}/tokens"

        tron_api_key = random.choice(TRON_API_KEYS)

        params = {
            "limit": "200",
            "page": page
        }

        headers = {
            "accept": "application/json",
            "TRON-PRO-API-KEY": tron_api_key,
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders_data(self, contract_address: str, market_id: str or int):
        holders_data = Holders()

        pages = self.__get_pages(market_id)

        for page in range(1, pages + 1):
            response = self.get_holders(contract_address, page)

            if not response:
                break

            data = response.json().get("data")

            if not data:
                break

            for obj in data:
                address = list(obj.keys())[0]
                balance = list(obj.values())[0]
                percents_of_coins = 0

                holder = Holder(address, balance, percents_of_coins)

                holders_data.append(holder)

        return holders_data

    def get_extra_holders(self, contracts, market_id):
        holders_data = Holders()

        for contract in contracts:
            contract_address = contract.get("address")

            holders = self.get_holders_data(contract_address, market_id)

            if not holders:
                continue

            print(holders)
            holders_data.extend(holders)

        return holders_data

    def load_holders_data_by_contract(self, contract: dict, slug_name: str, market_id: str or id):
        contract_address = contract.get("address")

        holders = self.get_holders_data(contract_address, market_id)

        if not holders:
            raise HoldersNotFoundError

        table = self.create_table(slug_name)

        for holder in holders:
            self.insert_data(table, holder)

    def get_token_metadata(self, contract_address: str):
        # TODO
        pass

    @staticmethod
    def __get_pages(market_id: str or int):
        market_id = int(market_id)

        if market_id > 0:
            return 5
