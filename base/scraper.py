import math
import time

from cloudscraper import create_scraper
from requests.exceptions import HTTPError, ConnectionError, ChunkedEncodingError

from base.limits import Limits
from exceptions.chains import InvalidChain


class BaseScraper(Limits):
    def __init__(self):
        super().__init__()
        self.scraper = create_scraper()

    def request(self, method, url, *args, **kwargs):
        try:
            response = self.scraper.request(method, url, *args, **kwargs)

            response.raise_for_status()

            return response
        except HTTPError as error:
            status_code = error.response.status_code

            if status_code in [400, 404]:
                raise InvalidChain()

            if status_code == 429:
                time.sleep(5)

                return self.request(method, url, *args, **kwargs)

            raise error
        except (ConnectionError, ChunkedEncodingError):
            return self.request(method, url, *args, **kwargs)

    def get_pages(self, market_id, limit):
        if market_id < 500:
            return math.ceil(self.top_500 / limit)

        if 500 <= market_id < 2500:
            return math.ceil(self.from_500_to_2500 / limit)

        return math.ceil(self.over_2500 / limit)

    @staticmethod
    def get_percents_of_coins(balance, total_supply):
        return int(balance) / int(total_supply) * 100
