from bs4 import BeautifulSoup
from cloudscraper import create_scraper

from db.models import HikuruTokenHolder
from db.setup import create_session
from decorators.request import request
from utils.formatters import get_correct_balance, get_correct_percents_of_coins

session = create_session()
s = session()

scraper = create_scraper()


# Bitcoin Info
@request
def get_richest_addresses(token, page):
    url = f"https://bitinfocharts.com/top-100-richest-{token}-addresses-{page}.html"

    response = scraper.get(url, timeout=15)

    return response


def parse_richest_addresses(token, response):
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
        "balance": get_correct_balance(address.find_all("td")[2].text),
        "percents_of_coins": get_correct_percents_of_coins(address.find_all("td")[3].text)
    } for address in addresses]


def get_parsed_richest_addresses(token, page=1):
    response = get_richest_addresses(token, page)
    addresses = parse_richest_addresses(token, response)

    return addresses


def load_parsed_richest_addresses(token, pages):
    for page in range(1, pages + 1):
        print(f"page: {page} for {token}")
        addresses = get_parsed_richest_addresses(token, page)

        if not addresses:
            return

        for obj in addresses:
            holder = HikuruTokenHolder(
                address=obj.get("address"),
                balance=obj.get("balance"),
                percents_of_coins=obj.get("percents_of_coins")
            )
            s.merge(holder)
            s.commit()


# EtherScan
@request
def get_token_from_search(token):
    url = f"https://etherscan.io/searchHandler?term={token}"

    response = scraper.get(url)

    return response


def get_address_by_token_name(token):
    response = get_token_from_search(token)

    return response.json()[0].get("address")


def main():
    pass


if __name__ == '__main__':
    main()
