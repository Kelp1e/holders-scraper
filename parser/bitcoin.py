from bs4 import BeautifulSoup
from requests import Response

from base.base_scraper import BaseScraper


class Bitcoin(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_parsed_richest_addresses(self, token: str, page=1):
        response = self.__get_richest_addresses(token, page)
        addresses = self.__parse_richest_addresses(token, response)

        return addresses

    def __get_richest_addresses(self, token: str, page: int):
        url = f"https://bitinfocharts.com/top-100-richest-{token}-addresses-{page}.html"

        response = self.request("get", url, timeout=20)

        return response

    def __parse_richest_addresses(self, token: str, response: Response):
        soup = BeautifulSoup(response.text, "lxml")

        header = soup.find("h1").text.lower()

        if token not in header:
            print(f"Incorrect token name: \"{token}\"")
            return

        tables = soup.find_all("table", {"id": ["tblOne", "tblOne2"]})

        if len(tables) != 2:
            print(f"No richest addresses for \"{token}\"")
            return

        first_table = tables[0]
        second_table = tables[1]

        addresses = []
        addresses.extend(first_table.find("tbody").find_all("tr"))
        addresses.extend(second_table.find_all("tr"))

        return [{
            "address": address.find_all("a")[0].text.replace(".", ""),
            "balance": self.get_correct_balance(address.find_all("td")[2].text),
            "percents_of_coins": self.get_correct_percents_of_coins(address.find_all("td")[3].text)
        } for address in addresses]

    @staticmethod
    def get_correct_balance(string: str):
        start = string.find("$") + 1
        end = string.find(")")

        return int(string[start:end].replace(",", ""))

    @staticmethod
    def get_correct_percents_of_coins(string: str):
        return float(string.replace("%", ""))
