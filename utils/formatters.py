def get_correct_balance(string: str):
    start = string.find("$") + 1
    end = string.find(")")

    return int(string[start:end].replace(",", ""))


def get_correct_percents_of_coins(string: str):
    return float(string.replace("%", ""))


