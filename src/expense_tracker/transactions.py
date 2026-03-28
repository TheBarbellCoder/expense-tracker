import duckdb
import logging


class Database:
    def __init__(self, db_name: str = "expenses.duckdb"):
        # Initialize database connection
        self.db = duckdb.connect(db_name)
        self.db.sql("CREATE SEQUENCE IF NOT EXISTS seq_id START 1")
        self.db.sql("CREATE TABLE IF NOT EXISTS Category (label VARCHAR(16) UNIQUE)")
        # self.db.table("Category").show()

    def __del__(self):
        # Close database connection
        self.db.close()

    def add_category(self, category: str) -> None:
        self.db.sql(f"INSERT INTO Category (label) VALUES ('{category}')")

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
