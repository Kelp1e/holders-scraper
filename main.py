import os

from dotenv import load_dotenv
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

# Env
load_dotenv()

TRUE = ("1", "true", "t", "y")

DELETE_RECORDS_WITH_ZERO_PERCENT: bool = (
    os.getenv("DELETE_RECORDS_WITH_ZERO_PERCENT").lower() in TRUE
)

ONE_ITERATION: bool = os.getenv("ONE_ITERATION").lower() in TRUE

# Types
DataFromCryptocurrencies = List[Tuple[int, str, List[Dict[str, str]], int]]
HoldersData = List[Holder]


def get_total_supply_from_contracts(contracts, evm, sol, trx):
    total_supply_from_contracts: float = 0

    for contract in contracts:
        chain: str = contract.get("network")
        contract_address: str = contract.get("address")

        try:
            evm_total_supply: float = evm.get_total_supply(chain, contract_address)
            total_supply_from_contracts += evm_total_supply
        except InvalidChain:
            try:
                sol_total_supply: float = sol.get_total_supply(contract_address)
                total_supply_from_contracts += sol_total_supply
            except InvalidChain:
                try:
                    trx_total_supply: float = trx.get_total_supply(contract_address)
                    total_supply_from_contracts += trx_total_supply
                except InvalidChain:
                    continue

    return total_supply_from_contracts


def get_holders_from_contracts(contracts, market_id, evm, sol, trx) -> HoldersData:
    holders_from_contract: HoldersData = []

    for contract in contracts:
        chain: str = contract.get("network")
        contract_address: str = contract.get("address")

        try:
            evm_holders: HoldersData = evm.get_holders(
                chain, contract_address, market_id
            )
            holders_from_contract.extend(evm_holders)
        except InvalidChain:
            try:
                sol_holders: HoldersData = sol.get_holders(contract_address, market_id)
                holders_from_contract.extend(sol_holders)
            except InvalidChain:
                try:
                    trx_holders: HoldersData = trx.get_holders(
                        contract_address, market_id
                    )
                    holders_from_contract.extend(trx_holders)
                except InvalidChain:
                    continue

    return holders_from_contract


def main() -> None:
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
        multi_total_supply: float = 0

        try:
            btc_total_supply: float = btc.get_total_supply(slug_name)
            multi_total_supply += btc_total_supply

            # For DogeCoin, LiteCoin etc.
            if slug_name in ("dogecoin", "litecoin"):
                total_supply_from_contracts: float = get_total_supply_from_contracts(
                    contracts, evm, sol, trx
                )
                multi_total_supply += total_supply_from_contracts

        except InvalidChain:
            total_supply_from_contracts: float = get_total_supply_from_contracts(
                contracts, evm, sol, trx
            )
            multi_total_supply += total_supply_from_contracts
        # Get holders data
        holders_data: HoldersData = []

        try:
            btc_holders: HoldersData = btc.get_holders(slug_name, market_id)
            holders_data.extend(btc_holders)

            # For DogeCoin, LiteCoin etc.
            if slug_name in ("dogecoin", "litecoin"):
                holders_from_contracts = get_holders_from_contracts(
                    contracts, market_id, evm, sol, trx
                )
                holders_data.extend(holders_from_contracts)

        except InvalidChain:
            holders_from_contracts = get_holders_from_contracts(
                contracts, market_id, evm, sol, trx
            )
            holders_data.extend(holders_from_contracts)

        # Skip if holders_data is clean
        if not holders_data:
            continue

        # Create holders to compress holders and calculate percents of coins
        holders: Holders = Holders(holders_data, multi_total_supply, market_id)

        table: Table = db.create_table(slug_name)  # Create table if not exist
        db.clear_table(table)  # Clear if data exist
        db.insert_holders(table, holders)  # Insert holders

        if DELETE_RECORDS_WITH_ZERO_PERCENT:
            db.delete_records_with_zero_percent(table)

        # Logs after save to db
        print(info)


if __name__ == "__main__":
    if ONE_ITERATION:
        main()
    else:
        while True:
            main()
