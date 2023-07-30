from utils.db import create_table, insert_data

bitcoin = create_table("0bitcoin")
insert_data(bitcoin, {"address": "address1234567890", "balance": 100_000_000, "percents_of_coins": 3.21})
