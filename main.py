from api.evm import Evm
from api.tron import Tron
from db.database import Database
from db.models import Cryptocurrency
from parser.bitcoin import Bitcoin
from scraper.holders_scraper import HoldersScraper


def main():
    # Find total supply for TRON tokens to calculate percents

    db = Database()
    evm = Evm()
    tron = Tron()
    bitcoin = Bitcoin()
    scraper = HoldersScraper()

    tether = db.get_data(Cryptocurrency, "slug_name", "contracts", "marketcap_id")[3]
    extra_holders = scraper.get_extra_holders(tether[0], tether[1], tether[2])
    print(len(extra_holders), extra_holders)


if __name__ == '__main__':
    main()
