# AI_BRIDGE - Portfolio DB

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Trade(Base):

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)
    strategy = Column(String)
    pnl = Column(Float)


class PortfolioDB:

    def __init__(self):

        self.engine = create_engine("sqlite:///portfolio.db")

        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    # =========================================
    # INSERT
    # =========================================

    def insert_trade(self, symbol, strategy, pnl):

        trade = Trade(
            symbol=symbol,
            strategy=strategy,
            pnl=pnl
        )

        self.session.add(trade)
        self.session.commit()
