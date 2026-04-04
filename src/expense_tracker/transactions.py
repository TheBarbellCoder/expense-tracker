import duckdb
import pandas as pd
import logging


class Database:
    def __init__(self, db_name: str = "expenses.duckdb"):
        # Initialize database connection
        self.db = duckdb.connect(db_name)
        self.db.sql(
            "CREATE TABLE IF NOT EXISTS Category (label VARCHAR(16) PRIMARY KEY)"
        )
        self.db.sql(
            """CREATE TABLE IF NOT EXISTS Transaction (
            booking_date DATE,
            payee VARCHAR,
            transaction VARCHAR(6),
            amount FLOAT,
            category VARCHAR(16),
            UNIQUE (booking_date, payee, transaction, amount))"""
        )

        # self.db.table("Category").show()
        # self.db.table("Transaction").show()

    def __del__(self):
        # Close database connection
        self.db.close()

    def add_category(self, category: str) -> bool:
        try:
            self.db.sql(
                f"""INSERT INTO Category (label)
                VALUES ('{category.strip().title()}')"""
            )
            return True
        except duckdb.ConstraintException:
            return False

    def ingest_transactions(self, df: "pd.dataframe") -> None:
        df = df.rename(
            columns={
                "Booking Date": "booking_date",
                "Payee": "payee",
                "Transaction": "transaction",
                "Amount": "amount",
                "Category": "category",
            }
        )
        self.db.sql("""INSERT INTO Transaction (booking_date, payee, transaction, amount, category)
                    SELECT booking_date, payee, transaction, amount, category FROM df
                    ON CONFLICT (booking_date, payee, transaction, amount) DO UPDATE SET
                    category = EXCLUDED.category
                    """)

    @property
    def categories(self):
        return self.db.sql("SELECT * FROM Category")


if __name__ == "__main__":
    # Setup logging
    log_formatter = logging.Formatter(
        "{asctime} [{levelname}] {message}", style="{", datefmt="%Y.%m.%d %H:%M"
    )
    logstream_handler = logging.StreamHandler()
    logstream_handler.setLevel(logging.DEBUG)
    logstream_handler.setFormatter(log_formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logstream_handler)
