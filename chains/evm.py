import json
import os
import random

from dotenv import load_dotenv

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain, BalanceLessThanZero
from exceptions.holders import InvalidAddress
from holders.holders import Holder, Holders

load_dotenv()

EVM_API_KEYS = json.loads(os.getenv("EVM_API_KEYS"))


class EVM(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit = 100

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

            decimals = data.get("decimals")
            total_supply = data.get("total_supply")[:-decimals]

            return total_supply
        except AttributeError:
            raise InvalidChain()

    def get_holders_response(self, chain, contract_address, page):
        url = "https://api.chainbase.online/v1/token/top-holders"

        chain_id = self.get_chain_id(chain)

        params = {
            "chain_id": chain_id,
            "contract_address": contract_address,
            "limit": self.limit,
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

        chain_for_db = self.__get_chain_for_db(chain)

        response = self.get_holders_response(chain, contract_address, page)

        if not response.json().get("data"):
            return Holders()

        for obj in response.json().get("data"):
            try:
                holder = self.__get_holder(obj, chain_for_db, total_supply)
                holders_data.append(holder)
            except InvalidAddress:
                continue
            except BalanceLessThanZero:
                break

        return Holders(holders_data)

    def get_holders(self, chain, contract_address, market_id):
        holders = []

        pages = self.get_pages(market_id, self.limit)

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

    def __get_holder(self, obj, chain_for_db, total_supply):
        address = obj.get("wallet_address")
        balance = int(float(obj.get("amount")))

        if not balance:
            raise BalanceLessThanZero()

        percents_of_coins = self.get_percents_of_coins(balance, total_supply)

        holder = Holder(address, balance, percents_of_coins, chain_for_db)

        return holder

    @staticmethod
    def __get_correct_chain(chain):
        lower_chain = chain.lower()

        correct_chains = {
            "binance coin": "bsc",
            "arbitrum": "arbitrum-one"
        }

        if lower_chain in correct_chains.keys():
            return correct_chains[lower_chain]

        return lower_chain

    @staticmethod
    def __get_chain_for_db(chain):
        lower_chain = chain.lower()

        chains_for_db = {
            "binance coin": "bsc",
            "arbitrum": "arb",
            "ethereum": "eth",
            "optimism": "opt",
            "avalanche": "avax"
        }

        if lower_chain in chains_for_db.keys():
            return chains_for_db[lower_chain]

        return lower_chain
