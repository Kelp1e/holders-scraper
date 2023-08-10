from db.database import Database
from holders.holders import Holder

db = Database()
holder = Holder("1123123123", "550", "1.00", "pol")

table = db.create_table("test")
db.clear_table(table)
db.insert_data(table, holder)
