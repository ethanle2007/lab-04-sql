import logging
import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Configure logging at import time
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Database connection settings from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# Default CSV location
DEFAULT_CSV = "MOCK_DATA.csv"
TABLE_NAME = "mock"


def read_data(filename: str) -> pd.DataFrame:

    logger.info("Reading CSV file: %s", filename)
    data = pd.read_csv(filename)
    logger.info("Loaded %d rows and %d columns", data.shape[0], data.shape[1])
    return data


def clean_data(data: pd.DataFrame) -> pd.DataFrame:

    logger.info("Cleaning data (%d rows before cleaning)", len(data))

    # Drop any row that contains at least one missing value
    cleaned = data.dropna().reset_index(drop=True)

    removed = len(data) - len(cleaned)
    logger.info("Removed %d rows with missing values; %d rows remain", removed, len(cleaned))
    return cleaned


def load_data(data: pd.DataFrame, table: str = TABLE_NAME) -> None:

    # Fail early with a clear message if any connection setting is missing
    settings = {
        "DB_HOST": DB_HOST,
        "DB_NAME": DB_NAME,
        "DB_USER": DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
    }
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

    logger.info("Connecting to MySQL database '%s' on host '%s'", DB_NAME, DB_HOST)

    # no special characters in the password
    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME,
    )
    engine = create_engine(url)

    try:
        logger.info("Uploading %d rows to table '%s'", len(data), table)
        # creates the table if it doesn't exist
        data.to_sql(
            name=table,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=1000,
        )
        logger.info("Upload complete")
    finally:
        # Always release the connection pool
        engine.dispose()
        logger.info("Database connection closed")


def main() -> None:

    logger.info("Starting pipeline")

    # Allow the CSV path to be passed in cli
    filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV

    data = read_data(filename)
    data = clean_data(data)
    load_data(data, TABLE_NAME)

    logger.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()