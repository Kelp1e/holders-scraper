def get_correct_balance(string: str):
    start = string.find("$") + 1
    end = string.find(")")

    return int(string[start:end].replace(",", ""))


def get_correct_percents_of_coins(string: str):
    return float(string.replace("%", ""))


def get_correct_network_from_db(string: str):
    if string == "Binance Coin":
        return "bsc"


def get_correct_table_name(string: str):
    string_numbers = map(str, range(0, 10))

    if string[0] in string_numbers:
        return f"_{string}"

    return string
