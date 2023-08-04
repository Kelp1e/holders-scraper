from sqlalchemy import Column, String, Integer, Float, Numeric, Boolean, Text, BIGINT
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrencies'

    token_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    token_symbol = Column(String(32), nullable=False)
    slug_name = Column(String(255), nullable=False)
    price = Column(Numeric(16, 8), default=-1)
    price_changes = Column(JSONB, default={"24h": 0, "7d": 0})
    volume = Column(Numeric(32, 8), default=0)
    circulation_supply = Column(Numeric(64, 2))
    total_supply = Column(Numeric(64, 2))
    max_supply = Column(Numeric(64, 2))
    circulation_supply_procent = Column(Numeric(8, 2))
    token_marketcap = Column(Numeric(64, 8))
    marketcap_id = Column(Integer)
    socials = Column(JSONB, default={})
    contracts = Column(JSONB, default=[])
    tokenomics = Column(JSONB, default={})
    investors = Column(JSONB, default=[])
    circulation_supply_confirmed = Column(Boolean)
    tags = Column(JSONB, default=[])
    description = Column(Text)
    hrating = Column(Numeric(4, 2))
