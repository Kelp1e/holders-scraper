import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from holders.holders import Holder

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


class Database:
    def __init__(self):
        self.engine = create_engine(f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}")
        self.session = sessionmaker(bind=self.engine)

    def get_data(self, model, *args):
        with self.session() as s:
            result = s.query(*[getattr(model, arg) for arg in args]).all()

            return result

    def create_table(self, table_name: str):
        metadata = MetaData()

        table = Table(
            self.__get_correct_table_name(table_name),
            metadata,
            Column("address", String, primary_key=True),
            Column("balance", String),
            Column("percents_of_coins", Float)
        )

        metadata.create_all(self.engine)

        return table

    def insert_data(self, table: Table, data: Holder):
        with self.engine.connect() as connection:
            stmt = insert(table).values(**data)
            on_conflict_stmt = stmt.on_conflict_do_update(index_elements=[table.c.address], set_={
                table.c.balance: data.balance,
                table.c.percents_of_coins: data.percents_of_coins
            })

            connection.execute(on_conflict_stmt)
            connection.commit()

    @staticmethod
    def __get_correct_table_name(table_name: str):
        lower_table_name = table_name.lower()

        if lower_table_name[0].isdigit():
            return f"_{lower_table_name}"

        return lower_table_name
