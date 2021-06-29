from sqlalchemy import Column, Integer, String

from database import Base


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True)
    currency_title = Column(String)
    currency_symbol = Column(String)
    currency_type = Column(String)
    rate_used = Column(String)
    timestamp = Column(Integer)