import time

from cloudscraper import create_scraper
from requests import HTTPError


class BaseScraper:
    def __init__(self):
        self.scraper = create_scraper()

    def request(self, request_type: str, url: str, **kwargs):
        try:
            response = self.scraper.request(request_type, url, **kwargs)

            response.raise_for_status()

            return response
        except HTTPError as error:
            status_code = error.response.status_code

            if status_code == 429:
                print(error)
                time.sleep(10)

                return self.request(request_type, url, **kwargs)
            if status_code == 400:
                print(error)

                return

            raise error

    @staticmethod
    def _get_correct_chain(chain: str):
        lower_chain = chain.lower()

        if lower_chain == "binance coin":
            return "bsc"

        if lower_chain == "arbitrum":
            return "arbitrum-one"

        return lower_chain

    @staticmethod
    def get_percents_of_coins(total_amount, balance):
        result = int(balance) / int(total_amount) * 100

        return result
