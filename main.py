from api.evm import Evm
from api.tron import Tron
from db.database import Database
from db.models import Cryptocurrency


def main():
    db = Database()
    evm = Evm()
    tron = Tron()

    for slug_name, market_id, contracts in db.get_data(Cryptocurrency, "slug_name", "marketcap_id", "contracts"):
        if contracts:
            for contract in contracts:
                chain = contract.get("network")
                contract_address = contract.get("address")
                print(evm._get_correct_chain(chain))


if __name__ == '__main__':
    main()
