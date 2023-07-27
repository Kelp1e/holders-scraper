from bs4 import BeautifulSoup
from cloudscraper import create_scraper

from decorators.request import request

scraper = create_scraper()


@request
def test():
    crypto_rank = "https://cryptorank.io/active-ico"
    google = "https://google.com"
    response = scraper.get(google, timeout=10)

    return response


@request
def get_richest_addresses(token, page=1):
    url = f"https://bitinfocharts.com/top-100-richest-{token}-addresses-{page}.html"

    response = scraper.get(url, timeout=15)

    return response


def parse_richest_addresses(token, page=1):
    response = get_richest_addresses(token, page)

    soup = BeautifulSoup(response.text, "lxml")

    tables = soup.find_all("table", {"id": ["tblOne", "tblOne2"]})
    first_table = tables[0]
    second_table = tables[1]

    addresses = []
    addresses.extend(first_table.find("tbody").find_all("tr"))
    addresses.extend(second_table.find_all("tr"))

    return [{
        "address": address.find_all("a")[0].text.replace(".", "")
    } for address in addresses]


def main():
    bitcoin = parse_richest_addresses("bitcoin")
    print(bitcoin)


if __name__ == '__main__':
    main()
