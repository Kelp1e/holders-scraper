from api.evm import Evm
from api.tron import Tron
from db.database import Database
from parser.bitcoin import Bitcoin
from utils.utils import Utils


def main():
    # Find total supply for TRON tokens to calculate percents

    db = Database()
    evm = Evm()
    tron = Tron()
    bitcoin = Bitcoin()

    utils = Utils()

    # tron_holders = tron.get_holders_data("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", 1)
    # print("tron:", len(tron_holders))

    # evm_holders = evm.get_holders_data("ethereum", "0xdac17f958d2ee523a2206206994597c13d831ec7", 1)
    # print("evm:", len(evm_holders), evm_holders)

    # tether_total_amount = evm.get_total_amount("ethereum", "0xdac17f958d2ee523a2206206994597c13d831ec7")
    # print(tether_total_amount)


if __name__ == '__main__':
    main()
