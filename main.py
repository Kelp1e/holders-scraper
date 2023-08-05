from chains.btc import BTC
from chains.evm import EVM
from chains.trx import TRX
from db.database import Database
from db.models import Cryptocurrency
from exceptions.chains.exceptions import InvalidChain


def main():
    # 1. Need to find trx total amount to calculate percents of coins
    # 2. Solana

    btc = BTC()
    evm = EVM()
    trx = TRX()
    db = Database()

    data_from_cryptocurrencies = db.get_data(Cryptocurrency, "slug_name", "contracts", "marketcap_id")[17:]
    i = 1
    for slug_name, contracts, market_id in data_from_cryptocurrencies:
        print(slug_name, i)
        if contracts:
            for contract in contracts:
                chain = contract.get("network")
                contract_address = contract.get("address")

                try:
                    holders = evm.get_holders(chain, contract_address, market_id)
                    print("evm", len(holders))
                except InvalidChain:
                    try:
                        holders = trx.get_holders(contract_address, market_id)
                        print("trx", len(holders))
                    except InvalidChain:
                        print("invalid chain API")
        else:
            try:
                holders = btc.get_holders(slug_name, market_id)
                print("btc", len(holders))
            except InvalidChain:
                print("invalid chain HTML")

        i += 1


if __name__ == '__main__':
    main()
