# app/data/persistence.py

import psycopg2
from psycopg2 import sql
from typing import Optional

from app.data.models import Candle
from app.data.logger import log


class PostgresCandleRepository:
    """
    Phase-1 PostgreSQL persistence layer.

    Responsibilities:
    - Insert closed candles
    - Commit per insert
    - Never crash trading engine

    NOT responsible for:
    - Gap detection
    - Historical recovery
    - Aggregation
    """

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        try:
            self.conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
            )
            self.conn.autocommit = False  # explicit commit control
            self.cursor = self.conn.cursor()

            log(
                "DB_CONNECTED",
                layer="persistence",
                symbol="SYSTEM",
            )

        except Exception as e:
            log(
                "DB_CONNECTION_FAILED",
                layer="persistence",
                symbol="SYSTEM",
                error=str(e),
            )
            raise

    # ==========================================================
    # Insert Candle
    # ==========================================================

    def insert_candle(self, candle: Candle) -> None:
        """
        Insert a closed candle safely.

        Uses:
        ON CONFLICT DO NOTHING
        """

        try:
            insert_query = """
                INSERT INTO candles (
                    symbol,
                    timeframe,
                    open_time,
                    close_time,
                    open_price,
                    high_price,
                    low_price,
                    close_price,
                    volume,
                    number_of_trades,
                    is_closed,
                    mode
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, timeframe, open_time)
                DO NOTHING;
            """

            self.cursor.execute(
                insert_query,
                (
                    candle.symbol,
                    candle.timeframe,
                    candle.open_time,
                    candle.close_time,
                    candle.open_price,
                    candle.high_price,
                    candle.low_price,
                    candle.close_price,
                    candle.volume,
                    candle.number_of_trades,
                    candle.is_closed,
                    candle.mode,
                ),
            )

            self.conn.commit()

            log(
                "CANDLE_PERSISTED",
                layer="persistence",
                symbol=candle.symbol,
                timeframe=candle.timeframe,
            )

        except Exception as e:
            self.conn.rollback()

            log(
                "CANDLE_PERSIST_FAILED",
                layer="persistence",
                symbol=candle.symbol,
                error=str(e),
            )

    # ==========================================================
    # Close Connection
    # ==========================================================

    def close(self) -> None:
        try:
            self.cursor.close()
            self.conn.close()

            log(
                "DB_CONNECTION_CLOSED",
                layer="persistence",
                symbol="SYSTEM",
            )

        except Exception:
            pass