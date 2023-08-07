from chains.btc import BTC
from chains.evm import EVM
from chains.sol import SOL
from chains.trx import TRX
from db.database import Database
from db.models import Cryptocurrency
from exceptions.chains import InvalidChain
from holders.holders import Holders


def main():
    btc = BTC()
    evm = EVM()
    trx = TRX()
    sol = SOL()

    db = Database()

    data_from_cryptocurrencies = db.get_data(Cryptocurrency, "slug_name", "contracts", "marketcap_id")

    for slug_name, contracts, market_id in data_from_cryptocurrencies:
        if contracts:
            holders = []

            for contract in contracts:
                chain = contract.get("network")
                contract_address = contract.get("address")

                try:
                    evm_holders = evm.get_holders(chain, contract_address, market_id)
                    holders.extend(evm_holders)
                except InvalidChain:
                    try:
                        trx_holders = trx.get_holders(contract_address, market_id)
                        holders.extend(trx_holders)
                    except InvalidChain:
                        try:
                            sol_holders = sol.get_holders(contract_address, market_id)
                            holders.extend(sol_holders)
                        except InvalidChain:
                            continue

            if not holders:
                continue

            table = db.create_table(slug_name)
            db.insert_holders(table, Holders(holders).filter_by_balance()[:1000])
        else:
            holders = []

            try:
                btc_holders = btc.get_holders(slug_name, market_id)
                holders.extend(btc_holders)
            except InvalidChain:
                continue

            if not holders:
                continue

            table = db.create_table(slug_name)
            db.insert_holders(table, Holders(holders).filter_by_balance()[:1000])


if __name__ == '__main__':
    main()
