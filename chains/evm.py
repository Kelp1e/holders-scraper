import json
import os
import random

from dotenv import load_dotenv
from requests.exceptions import HTTPError

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain, PageOutOfRange, LimitOutOfRange
from holders.holders import Holder, Holders

load_dotenv()

EVM_API_KEYS = json.loads(os.getenv("EVM_API_KEYS"))


class EVM(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit = 100

    def get_token_metadata(self, chain: str, contract_address: str):
        url = "https://api.chainbase.online/v1/token/metadata"

        params = {
            "chain_id": self.get_chain_id(chain),
            "contract_address": contract_address
        }

        headers = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        response = self.request("get", url, params=params, headers=headers)

        return response

    def get_total_supply(self, chain: str, contract_address: str):
        response = self.get_token_metadata(chain, contract_address)

        data = response.json().get("data")

        decimals = data.get("decimals")

        total_supply = data.get("total_supply")[:-decimals]

        return int(total_supply)

    def get_holders_response(self, chain: str, contract_address: str, page):
        url = "https://api.chainbase.online/v1/token/top-holders"

        params = {
            "chain_id": self.get_chain_id(chain),
            "contract_address": contract_address,
            "limit": self.limit,
            "page": page
        }

        headers = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        try:
            response = self.request("get", url, params=params, headers=headers)

            return response
        except HTTPError as error:
            error_message = error.response.json().get("error")

            if error_message == "page out of range":
                raise PageOutOfRange(chain, contract_address, page)

            if error_message == "limit out of range":
                raise LimitOutOfRange(chain, contract_address, self.limit)

            raise error

    def get_holders_data(self, chain: str, contract_address: str, page: int):
        response = self.get_holders_response(chain, contract_address, page)

        data = response.json().get("data")

        holders_data = Holders([self.get_holder(obj) for obj in data])

        return holders_data

    # Utils
    def get_chain_id(self, chain: str):
        correct_chain = self.get_correct_chain(chain)

        chain_id = {
            "ethereum": "1",
            "polygon": "137",
            "bsc": "56",
            "avalanche": "43114",
            "arbitrum-one": "42161",
            "optimism": "10"
        }

        if correct_chain not in chain_id.keys():
            raise InvalidChain()

        return chain_id[correct_chain]

    @staticmethod
    def get_correct_chain(chain: str):
        lower_chain = chain.lower()

        correct_chains = {
            "binance coin": "bsc",
            "arbitrum": "arbitrum-one"
        }

        if lower_chain in correct_chains.keys():
            return correct_chains[lower_chain]

        return lower_chain

    @staticmethod
    def get_holder(obj):
        address = obj.get("wallet_address")
        balance = int(float(obj.get("amount")))

        holder = Holder(address, balance)

        return holder
