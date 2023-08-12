from typing import List, Tuple, Dict

from chains.btc import BTC
from chains.evm import EVM
from chains.sol import SOL
from chains.trx import TRX

from db.database import Database
from db.models import Cryptocurrency

from exceptions.chains import InvalidChain

from holders.holders import Holders

# Types
DataFromCryptocurrencies = List[Tuple[str, List[Dict[str, str]], int]]


# [("bitcoin", [], 1), ("ethereum", [{}, {}, {}], 2), (), (), ()]


def main():
    btc: BTC = BTC()  # HTML: BitInfoCharts
    evm: EVM = EVM()  # REST API: ChainBase
    sol: SOL = SOL()  # REST API: SolScan
    trx: TRX = TRX()  # REST API: Tron, TronScan

    db: Database = Database()  # SQLAlchemy

    data_from_cryptocurrencies: DataFromCryptocurrencies = db.get_data(
        Cryptocurrency, "slug_name", "contracts", "marketcap_id"
    )

    for slug_name, contracts, market_id in data_from_cryptocurrencies:
        info = f"[{market_id}]: {slug_name}"  # [1]: bitcoin

        # Get multi total supply to calculate correct percents
        multi_total_supply = 0

        try:
            btc_total_supply = btc.get_total_supply(slug_name)
            multi_total_supply += btc_total_supply
        except InvalidChain:
            for contract in contracts:
                chain = contract.get("network")
                contract_address = contract.get("address")

                try:
                    evm_multi_total_supply = evm.get_total_supply(chain, contract_address)
                    multi_total_supply += evm_multi_total_supply
                except InvalidChain:
                    try:
                        sol_total_supply = sol.get_total_supply(contract_address)
                        multi_total_supply += sol_total_supply
                    except InvalidChain:
                        try:
                            trx_total_supply = trx.get_total_supply(contract_address)
                            multi_total_supply += trx_total_supply
                        except InvalidChain:
                            continue

        print(info, multi_total_supply)


if __name__ == '__main__':
    main()
