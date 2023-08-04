from db.database import Database
from holders.holders import Holder


def main():
    db = Database()

    holder = Holder(
        address="123",
        balance="1000",
        percents_of_coins="1.20"
    )

    new_table = db.create_table("new_table")
    db.insert_data(new_table, holder)


if __name__ == '__main__':
    main()
