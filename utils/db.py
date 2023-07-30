import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, Column, String, BIGINT, Float, create_engine

from database.models import Cryptocurrency
from utils.formatters import get_correct_table_name

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
)


def get_slug_names_from_cryptocurrencies(s):
    slug_names = [slug_name[0]
                  for slug_name
                  in s.query(Cryptocurrency.slug_name).distinct().all()]

    return slug_names


def get_market_id_and_contracts_from_cryptocurrencies(s):
    contracts_with_id = s.query(Cryptocurrency.marketcap_id, Cryptocurrency.contracts).all()

    return [i for i in contracts_with_id if i[1]]


def create_table(table_name: str):
    metadata = MetaData()

    table = Table(
        get_correct_table_name(table_name),
        metadata,
        Column("address", String, primary_key=True),
        Column("balance", BIGINT),
        Column("percents_of_coins", Float)
    )

    metadata.create_all(engine)

    return table


def insert_data(table, data: dict):
    with engine.connect() as connection:
        insert = table.insert().values(**data)
        connection.execute(insert)
        connection.commit()
