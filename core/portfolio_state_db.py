# AI_BRIDGE - Portfolio State Database

import sqlite3
from datetime import datetime


class PortfolioStateDB:

    def __init__(self, path="portfolio.db"):

        self.conn = sqlite3.connect(path)
        self._init()

    def _init(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            strategy TEXT,
            profit REAL,
            timestamp TEXT
        )
        """)

        self.conn.commit()

    # =========================================
    # INSERT TRADE
    # =========================================

    def insert_trade(self, symbol, strategy, profit):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO trades (symbol, strategy, profit, timestamp)
        VALUES (?, ?, ?, ?)
        """, (symbol, strategy, profit, datetime.utcnow().isoformat()))

        self.conn.commit()

    # =========================================
    # GET PERFORMANCE
    # =========================================

    def get_total_pnl(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT SUM(profit) FROM trades")

        result = cursor.fetchone()[0]

        return result or 0
