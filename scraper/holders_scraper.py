from api.evm import Evm
from api.tron import Tron
from db.database import Database
from exceptions.holders_not_found import HoldersNotFoundError
from holders.holders import Holders
from parser.bitcoin import Bitcoin


class HoldersScraper(Database):
    def __init__(self):
        super().__init__()
        self.evm = Evm()
        self.tron = Tron()
        self.bitcoin = Bitcoin()

    def load_holders(self, data):
        pass

    def get_extra_holders(self, slug_name, contracts, market_id):
        holders_data = Holders()

        evm_holders = self.evm.get_extra_holders(contracts, market_id)
        print("evm", len(evm_holders))
        tron_holders = self.tron.get_extra_holders(contracts, market_id)
        print("tron", len(tron_holders))
        bitcoin_holders = self.bitcoin.get_extra_holders(slug_name, market_id)
        print("bitcoin", len(bitcoin_holders))

        # holders_data.extend(evm_holders)
        holders_data.extend(tron_holders)
        holders_data.extend(bitcoin_holders)

        return holders_data
