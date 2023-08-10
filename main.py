from chains.btc import BTC
from chains.evm import EVM
from chains.sol import SOL
from chains.trx import TRX

from db.database import Database
from db.models import Cryptocurrency

from exceptions.chains import InvalidChain

from holders.holders import Holders


def main():
    btc = BTC()  # HTML: BitInfoCharts
    evm = EVM()  # REST API: ChainBase
    trx = TRX()  # REST API: Tron, TronScan
    sol = SOL()  # REST API: SolScan

    db = Database()  # SQLAlchemy

    data_from_cryptocurrencies = db.get_data(Cryptocurrency, "slug_name", "contracts", "marketcap_id")
    # data_from_cryptocurrencies: [("bitcoin", [], 1), ("ethereum", [{}, {}, {}], 2), (), (), ()]

    for slug_name, contracts, market_id in data_from_cryptocurrencies:
        info = f"[{market_id}]: {slug_name}"

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
            db.clear_table(table)
            db.insert_holders(table, Holders(holders).filter_by_balance(market_id))

            print(info)
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
            db.clear_table(table)
            db.insert_holders(table, Holders(holders).filter_by_balance(market_id))

            print(info)


if __name__ == '__main__':
    while True:
        main()
