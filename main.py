from sqlalchemy import Table
from typing import List, Tuple, Dict

from chains.btc import BTC
from chains.evm import EVM
from chains.sol import SOL
from chains.trx import TRX

from db.database import Database
from db.models import Cryptocurrency

from exceptions.chains import InvalidChain

from holders.holders import Holders, Holder

# Types
DataFromCryptocurrencies = List[Tuple[int, str, List[Dict[str, str]], int]]
HoldersData = List[Holder]


def main():
    btc: BTC = BTC()  # HTML: BitInfoCharts
    evm: EVM = EVM()  # REST API: ChainBase
    sol: SOL = SOL()  # REST API: SolScan
    trx: TRX = TRX()  # REST API: Tron, TronScan

    db: Database = Database()  # SQLAlchemy

    data_from_cryptocurrencies: DataFromCryptocurrencies = db.get_data(
        Cryptocurrency, "token_id", "slug_name", "contracts", "marketcap_id"
    )

    for token_id, slug_name, contracts, market_id in data_from_cryptocurrencies:
        info: str = f"|token_id: [{token_id}]| |market_id: [{market_id}]| |market_id: [{slug_name}]|"

        # Get multi total supply to calculate correct percents
        multi_total_supply: int = 0

        try:
            btc_total_supply: int = btc.get_total_supply(slug_name)
            multi_total_supply += btc_total_supply
        except InvalidChain:
            for contract in contracts:
                chain: str = contract.get("network")
                contract_address: str = contract.get("address")

                try:
                    evm_multi_total_supply: int = evm.get_total_supply(chain, contract_address)
                    multi_total_supply += evm_multi_total_supply
                except InvalidChain:
                    try:
                        sol_total_supply: int = sol.get_total_supply(contract_address)
                        multi_total_supply += sol_total_supply
                    except InvalidChain:
                        try:
                            trx_total_supply: int = trx.get_total_supply(contract_address)
                            multi_total_supply += trx_total_supply
                        except InvalidChain:
                            continue

        # Get holders data
        holders_data: HoldersData = []

        try:
            btc_holders: HoldersData = btc.get_holders(slug_name, market_id)
            holders_data.extend(btc_holders)
        except InvalidChain:
            for contract in contracts:
                chain: str = contract.get("network")
                contract_address: str = contract.get("address")

                try:
                    evm_holders: HoldersData = evm.get_holders(chain, contract_address, market_id)
                    holders_data.extend(evm_holders)
                except InvalidChain:
                    try:
                        sol_holders: HoldersData = sol.get_holders(contract_address, market_id)
                        holders_data.extend(sol_holders)
                    except InvalidChain:
                        try:
                            trx_holders: HoldersData = trx.get_holders(contract_address, market_id)
                            holders_data.extend(trx_holders)
                        except InvalidChain:
                            continue

        # Skip if holders_data is clean
        if not holders_data:
            continue

        # Create holders to compress holders and calculate percents of coins
        holders: Holders = Holders(holders_data, multi_total_supply, market_id)

        table: Table = db.create_table(slug_name)  # Create table if not exist
        db.clear_table(table)  # Clear if data exist
        db.insert_holders(table, holders)  # Insert holders

        # Logs
        print(info)


if __name__ == '__main__':
    main()
