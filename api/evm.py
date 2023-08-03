import os
import random
from http.client import BAD_REQUEST

from dotenv import load_dotenv

from base.base_scraper import BaseScraper
from exceptions.holders_not_found import HoldersNotFoundError
from holders.holders import Holder, Holders

load_dotenv()

EVM_API_KEYS = os.getenv("EVM_API_KEYS").split()


class Evm(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_total_amount(self, chain: str, contract_address: str):
        response = self.get_token_metadata(chain, contract_address)

        if not response:
            return

        data = response.json().get("data")

        if not data:
            return

        total_supply = data.get("total_supply")

        return total_supply

    def get_token_metadata(self, chain: str, contract_address: str):
        url = "https://api.chainbase.online/v1/token/metadata"

        params = {
            "chain_id": self.__get_chain_id(chain),
            "contract_address": contract_address
        }

        headers = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders(self, chain: str, contract_address: str, page: int = 1):
        url = "https://api.chainbase.online/v1/token/top-holders"

        chain_id = self.__get_chain_id(chain)

        params = {
            "chain_id": chain_id,
            "contract_address": contract_address,
            "limit": 100,
            "page": page,
        }

        headers = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders_data(self, chain: str, contract_address: str, market_id: str or int):
        holders_data = Holders()

        pages = self.__get_pages(market_id)

        total_amount = self.get_total_amount(chain, contract_address)

        if not total_amount:
            return

        for page in range(1, pages + 1):
            response = self.get_holders(chain, contract_address, page)

            if not response:
                break

            data = response.json().get("data")

            if not data:
                break

            for obj in data:
                address = obj.get("wallet_address")
                balance = obj.get("original_amount")
                percents_of_coins = self.get_percents_of_coins(total_amount, balance)

                holder = Holder(address, balance, percents_of_coins)

                holders_data.append(holder)

        return holders_data

    def get_extra_holders(self, contracts, market_id):
        holders_data = Holders()

        for contract in contracts:
            chain = contract.get("network")
            contract_address = contract.get("address")

            holders = self.get_holders_data(chain, contract_address, market_id)

            if not holders:
                continue

            holders_data.extend(holders)

        return holders_data

    def load_holders_data_by_contract(self, contract: dict, slug_name: str, market_id: str or int):
        chain = contract.get("network")
        contract_address = contract.get("address")

        holders = self.get_holders_data(chain, contract_address, market_id)

        if not holders:
            raise HoldersNotFoundError

        table = self.create_table(slug_name)

        for holder in holders:
            self.insert_data(table, holder)

    def __get_chain_id(self, chain: str):
        correct_chain = self._get_correct_chain(chain)

        chain_id = {
            "ethereum": "1",
            "polygon": "137",
            "bsc": "56",
            "avalanche": "43114",
            "arbitrum-one": "42161",
            "optimism": "10"
        }

        if correct_chain not in chain_id.keys():
            return

        return chain_id[correct_chain]

    @staticmethod
    def __get_pages(market_id: str or int):
        market_id = int(market_id)

        if market_id <= 500:
            return 10

        if 500 <= market_id <= 2500:
            return 5

        if 2500 <= market_id:
            return 3
