import time

from cloudscraper import create_scraper
from requests import HTTPError


class BaseScraper:
    def __init__(self):
        self.scraper = create_scraper()

    def request(self, request_type, url, **kwargs):
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
            else:
                print("pass:", error)
                pass

    @staticmethod
    def _get_correct_chain(chain):
        lower_chain = chain.lower()

        if lower_chain == "binance coin":
            return "bsc"

        if lower_chain == "arbitrum":
            return "arbitrum-one"

        return lower_chain