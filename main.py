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
    sol = SOL()  # REST API: SolScan
    trx = TRX()  # REST API: Tron, TronScan

    db = Database()  # SQLAlchemy

    data_from_cryptocurrencies = db.get_data(Cryptocurrency, "slug_name", "contracts", "marketcap_id")
    # data_from_cryptocurrencies: [("bitcoin", [], 1), ("ethereum", [{}, {}, {}], 2), (), (), ()]

    for slug_name, contracts, market_id in data_from_cryptocurrencies:
        info = f"[{market_id}]: {slug_name}"


if __name__ == '__main__':
    while True:
        main()
