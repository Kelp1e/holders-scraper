import os
import random

from dotenv import load_dotenv
from requests import HTTPError

from base.scraper import BaseScraper
from exceptions.chains.exceptions import InvalidChain
from holders.holders import Holder, Holders

load_dotenv()

EVM_API_KEYS = os.getenv("EVM_API_KEYS").split()


class EVM(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_token_metadata(self, chain, contract_address):
        url = "https://api.chainbase.online/v1/token/metadata"

        chain_id = self.get_chain_id(chain)

        params = {
            "chain_id": chain_id,
            "contract_address": contract_address,
        }

        headers = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_total_supply(self, chain, contract_address):
        try:
            response = self.get_token_metadata(chain, contract_address)

            data = response.json().get("data")

            total_supply = data.get("total_supply")

            return total_supply
        except AttributeError:
            raise InvalidChain()

    def get_holders_response(self, chain, contract_address, page):
        url = "https://api.chainbase.online/v1/token/top-holders"

        chain_id = self.get_chain_id(chain)

        params = {
            "chain_id": chain_id,
            "contract_address": contract_address,
            "limit": 100,
            "page": page
        }

        headers = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_holders_data(self, chain, contract_address, page, total_supply):
        holders_data = []

        response = self.get_holders_response(chain, contract_address, page)

        if not response.json().get("data"):
            return Holders()

        for obj in response.json().get("data"):
            holder = self.get_holder(obj, total_supply)

            holders_data.append(holder)

        return Holders(holders_data)

    def get_holders(self, chain, contract_address, market_id):
        holders = []

        pages = self.__get_pages(market_id)

        total_supply = self.get_total_supply(chain, contract_address)

        for page in range(1, pages + 1):
            holders_data = self.get_holders_data(chain, contract_address, page, total_supply)

            holders.extend(holders_data)

        return Holders(holders)

    def get_chain_id(self, chain):
        correct_chain = self.__get_correct_chain(chain)

        chain_id = {
            "ethereum": "1",
            "polygon": "137",
            "bsc": "56",
            "avalanche": "43114",
            "arbitrum-one": "42161",
            "optimism": "10"
        }

        if correct_chain not in chain_id.keys():
            return correct_chain

        return chain_id[correct_chain]

    def get_holder(self, obj, total_supply):
        address = obj.get("wallet_address")
        balance = obj.get("original_amount")
        percents_of_coins = self.get_percents_of_coins(balance, total_supply)

        holder = Holder(address, balance, percents_of_coins)

        return holder

    @staticmethod
    def __get_correct_chain(chain):
        lower_chain = chain.lower()

        if lower_chain == "binance coin":
            return "bsc"

        if lower_chain == "arbitrum":
            return "arbitrum-one"

        return lower_chain

    @staticmethod
    def __get_pages(market_id):
        market_id = int(market_id)

        if market_id <= 500:
            return 10

        if 500 <= market_id <= 2500:
            return 5

        if 2500 <= market_id:
            return 3
