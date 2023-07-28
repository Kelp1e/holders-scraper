import time

from requests import HTTPError


def request(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)

            response.raise_for_status()

            return response
        except HTTPError as error:
            if error.response.status_code == 429:
                print(error)
                time.sleep(10)

                return wrapper(*args, **kwargs)
            else:
                print("pass", error)
                pass

    return wrapper
