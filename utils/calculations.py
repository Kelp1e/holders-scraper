class Calculations:
    @staticmethod
    def get_percents_of_coins(token_total_supply, balance):
        result = int(balance) / int(token_total_supply) * 100

        return result

    def __call__(self, token_total_supply, balance, *args, **kwargs):
        return self.get_percents_of_coins(token_total_supply, balance)
