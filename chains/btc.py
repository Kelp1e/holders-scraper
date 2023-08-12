from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from base.scraper import BaseScraper
from exceptions.chains import InvalidChain
from holders.holders import Holders, Holder


class BTC(BaseScraper):
    def __init__(self):
        super().__init__()
        self.limit = 100

    def get_total_supply(self, slug_name):
        try:
            url = f"https://bitinfocharts.com/{slug_name}/"

            response = self.request("get", url)
        except HTTPError as error:
            if error.response.status_code == 404:
                raise InvalidChain()

            raise error

        if not response.text:
            raise InvalidChain()

        soup = BeautifulSoup(response.text, "lxml")

        header = soup.find("h1").text.lower()

        rich_list = soup.find("h2")

        if slug_name not in header or not rich_list:
            raise InvalidChain()

        table = soup.find("table")

        total_supply = int(table.find_all("tr")[0].find_all("td")[1].text.split()[0].replace(",", ""))

        return total_supply

    def get_holders(self, slug_name, market_id):
        holders = []

        pages = self.get_pages(market_id, self.limit)

        total_supply = self.get_total_supply(slug_name)

        for page in range(1, pages + 1):
            holders_data = self.get_holders_data(slug_name, total_supply, page)

            holders.extend(holders_data)

        return Holders(holders)

    def get_holders_data(self, slug_name: str, total_supply, page=1):
        response = self.__get_richest_addresses(slug_name, page)
        addresses = self.__parse_richest_addresses(slug_name, response, total_supply)

        return addresses

    def __get_richest_addresses(self, slug_name: str, page: int):
        url = f"https://bitinfocharts.com/top-100-richest-{slug_name}-addresses-{page}.html"

        response = self.request("get", url, timeout=30)

        return response

    def __parse_richest_addresses(self, slug_name: str, response, total_supply):
        soup = BeautifulSoup(response.text, "lxml")

        header = soup.find("h1").text.lower()

        if slug_name not in header:
            raise InvalidChain()

        tables = soup.find_all("table", {"id": ["tblOne", "tblOne2"]})

        if len(tables) != 2:
            raise InvalidChain()

        first_table = tables[0]
        second_table = tables[1]

        data = []
        data.extend(first_table.find("tbody").find_all("tr"))
        data.extend(second_table.find_all("tr"))

        return Holders([self.__get_holder(obj, total_supply) for obj in data])

    def __get_holder(self, obj, total_supply):
        address = obj.find_all("a")[0].text.replace(".", "")
        balance = self.get_correct_balance(obj.find_all("td")[2].text)
        percents_of_coins = self.get_percents_of_coins(balance, total_supply)

        holder = Holder(address, balance, percents_of_coins, "btc")

        return holder

    @staticmethod
    def get_correct_balance(string: str):
        return string.split()[0].replace(",", "")

    @staticmethod
    def get_correct_percents_of_coins(string: str):
        return float(string.replace("%", ""))
