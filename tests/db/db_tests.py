from db.database import Database
from holders.holders import Holder

db = Database()
holder = Holder("123", "550", "1.00")

table = db.create_table("test")
db.insert_data(table, holder)
