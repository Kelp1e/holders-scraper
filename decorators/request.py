import time

import requests
from urllib3.exceptions import NameResolutionError


def request(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)

            response.raise_for_status()

            return response
        except Exception as error:
            print(error)
            time.sleep(10)

            return wrapper(*args, **kwargs)

    return wrapper
