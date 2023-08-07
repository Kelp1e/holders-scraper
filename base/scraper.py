import time

from cloudscraper import create_scraper
from requests import HTTPError

from exceptions.chains.exceptions import InvalidChain


class BaseScraper:
    def __init__(self):
        self.scraper = create_scraper()

    def request(self, method, url, *args, **kwargs):
        try:
            response = self.scraper.request(method, url, *args, **kwargs)

            response.raise_for_status()

            return response
        except HTTPError as error:
            time_for_sleep = 5
            status_code = error.response.status_code

            if status_code == 400:
                raise InvalidChain()

            if status_code == 404:
                raise InvalidChain()

            if status_code == 429:
                print(f"Sleeping for {time_for_sleep} seconds...", error)

                time.sleep(time_for_sleep)

                return self.request(method, url, *args, **kwargs)

            raise error

    @staticmethod
    def get_percents_of_coins(balance, total_supply):
        return int(balance) / int(total_supply) * 100
