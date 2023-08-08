from bs4 import BeautifulSoup

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain
from holders.holders import Holders, Holder


class BTC(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_holders(self, slug_name, market_id):
        holders = []

        pages = self.__get_pages(market_id)

        for page in range(1, pages + 1):
            holders_data = self.get_holders_data(slug_name, page)

            holders.extend(holders_data)

        return Holders(holders)

    def get_holders_data(self, slug_name: str, page=1):
        response = self.__get_richest_addresses(slug_name, page)
        addresses = self.__parse_richest_addresses(slug_name, response)

        return addresses

    def __get_richest_addresses(self, slug_name: str, page: int):
        url = f"https://bitinfocharts.com/top-100-richest-{slug_name}-addresses-{page}.html"

        response = self.request("get", url, timeout=30)

        return response

    def __parse_richest_addresses(self, slug_name: str, response):
        soup = BeautifulSoup(response.text, "lxml")

        header = soup.find("h1").text.lower()

        if slug_name not in header:
            raise InvalidChain()

        tables = soup.find_all("table", {"id": ["tblOne", "tblOne2"]})

        if len(tables) != 2:
            raise InvalidChain()

        first_table = tables[0]
        second_table = tables[1]

        addresses = []
        addresses.extend(first_table.find("tbody").find_all("tr"))
        addresses.extend(second_table.find_all("tr"))

        return Holders([Holder(**{
            "address": address.find_all("a")[0].text.replace(".", ""),
            "balance": self.get_correct_balance(address.find_all("td")[2].text),
            "percents_of_coins": self.get_correct_percents_of_coins(address.find_all("td")[3].text),
            "chains": "btc"
        }) for address in addresses])

    @staticmethod
    def get_correct_balance(string: str):
        start = string.find("$") + 1
        end = string.find(")")

        return int(string[start:end].replace(",", ""))

    @staticmethod
    def get_correct_percents_of_coins(string: str):
        return float(string.replace("%", ""))

    @staticmethod
    def __get_pages(market_id):
        market_id = int(market_id)

        if market_id > 0:
            return 10
