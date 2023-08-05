from requests import HTTPError

from chains.btc import BTC
from chains.evm import EVM
from chains.trx import TRX
from db.database import Database
from holders.holders import Holders


class HolderScraper:
    def __init__(self):
        self.db = Database()
        self.trx = TRX()
        self.evm = EVM()
        self.btc = BTC()

    def get_holders(self, slug_name, contract, market_id):
        pass
