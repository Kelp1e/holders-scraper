import json
import os
import random
from typing import List, Dict

from dotenv import load_dotenv
from requests import Response
from requests.exceptions import HTTPError

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain, PageOutOfRange, LimitOutOfRange
from holders.holders import Holder, Holders

load_dotenv()

EVM_API_KEYS = json.loads(os.getenv("EVM_API_KEYS"))

# Types
HoldersData = List[Dict[str, str]]
HolderResponseObject = Dict[str, str]


class EVM(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit: int = 100

    def get_token_metadata(self, chain: str, contract_address: str) -> Response:
        url: str = "https://api.chainbase.online/v1/token/metadata"

        params: dict = {
            "chain_id": self.get_chain_id(chain),
            "contract_address": contract_address
        }

        headers: dict = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        response: Response = self.request("get", url, params=params, headers=headers)

        return response

    def get_total_supply(self, chain: str, contract_address: str) -> int:
        response: Response = self.get_token_metadata(chain, contract_address)

        data: dict = response.json().get("data")

        if not data:
            raise InvalidChain()

        decimals: int = data.get("decimals")

        total_supply_with_decimals: str = data.get("total_supply")

        if total_supply_with_decimals == "0":
            raise InvalidChain()

        total_supply: int = int(total_supply_with_decimals[:-decimals])

        return total_supply

    def get_holders_response(self, chain: str, contract_address: str, page: int) -> Response:
        url: str = "https://api.chainbase.online/v1/token/top-holders"

        params: dict = {
            "chain_id": self.get_chain_id(chain),
            "contract_address": contract_address,
            "limit": self.limit,
            "page": page
        }

        headers: dict = {
            "accept": "application/json",
            "x-api-key": random.choice(EVM_API_KEYS)
        }

        try:
            response: Response = self.request("get", url, params=params, headers=headers)

            return response
        except HTTPError as error:
            error_message = error.response.json().get("error")

            if error_message == "page out of range":
                raise PageOutOfRange()

            if error_message == "limit out of range":
                raise LimitOutOfRange(chain, contract_address, self.limit)

            raise error

    def get_holders_data(self, chain: str, contract_address: str, page: int) -> HoldersData:
        response: Response = self.get_holders_response(chain, contract_address, page)

        data: HoldersData = response.json().get("data")

        return data

    def get_holders(self, chain: str, contract_address: str, market_id) -> List[Holder]:
        pages: int = self.get_pages(market_id, self.limit)

        chain_for_db = self.get_correct_chain_for_db(chain)

        holders_data: HoldersData = []

        for page in range(1, pages + 1):
            data = self.get_holders_data(chain, contract_address, page)

            if not data:
                break

            holders_data.extend(data)

        holders: List[Holder] = [self.get_holder(obj, chain_for_db) for obj in holders_data]

        return holders

    # Utils
    def get_chain_id(self, chain: str) -> str:
        correct_chain: str = self.get_correct_chain(chain)

        chain_id: Dict[str, str] = {
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
    def get_correct_chain(chain: str) -> str:
        lower_chain: str = chain.lower()

        correct_chains: dict = {
            "binance coin": "bsc",
            "arbitrum": "arbitrum-one"
        }

        if lower_chain in correct_chains.keys():
            return correct_chains[lower_chain]

        return lower_chain

    @staticmethod
    def get_correct_chain_for_db(chain: str) -> str:
        lower_chain: str = chain.lower()

        chains_for_db: Dict[str, str] = {
            "ethereum": "eth",
            "binance coin": "bsc",
            "avalanche": "avax",
            "arbitrum": "arb",
            "optimism": "opt",
        }

        if lower_chain in chains_for_db.keys():
            return chains_for_db[lower_chain]

        return lower_chain

    @staticmethod
    def get_holder(obj: HolderResponseObject, chain_for_db: str) -> Holder:
        address: str = str(obj.get("wallet_address"))
        balance: int = int(float(obj.get("amount")))
        chain: str = chain_for_db

        holder: Holder = Holder(address, balance, chain)

        return holder
