import json
import os

from dotenv import load_dotenv

load_dotenv()

LIMITS = json.loads(os.getenv("LIMITS"))


class Limits:
    def __init__(self):
        self.top_500 = LIMITS[0]
        self.from_500_to_2500 = LIMITS[1]
        self.over_2500 = LIMITS[2]

    def get_limit(self, market_id):
        if market_id < 500:
            return self.top_500

        if 500 <= market_id < 2500:
            return self.from_500_to_2500

        return self.over_2500
