from os import environ

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# load .env
load_dotenv()

POSTGRES_CONNECTION = environ.get("POSTGRES_CONNECTION")
POSTGRES_DATABASE = environ.get("POSTGRES_DATABASE")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_ENDPOINT = environ.get("POSTGRES_ENDPOINT")

CONNSTR = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_CONNECTION}/{POSTGRES_DATABASE}?sslmode=require&options=project%3D{POSTGRES_ENDPOINT}"

# Create sqlalchemy engine and session
postgres_engine = create_engine(CONNSTR)
Session = sessionmaker(bind=postgres_engine)
session = Session()

test_table = "neon_db_test"

# create test table
create_table_ddl = f"""
    CREATE TABLE {test_table} (
        col_a INTEGER,
        col_b DATE
    );
"""

# run query to create test table - this will result in a pandas error but the table should get created
create_table_df = pd.read_sql(
    sql=create_table_ddl,
    con=postgres_engine
)

# create dataframe with data to insert into test table
insert_df = pd.DataFrame({
    "col_a": [2023, 2023],
    "col_b": ["2023-01-27", "2023-01-28"]
})

# insert data from dataframe into test table
insert_df.to_sql(
    test_table,
    con=postgres_engine,
    if_exists="append",
    index=False
)

# read data from test table to see if data was added
read_data_df = pd.read_sql(
    sql=f"SELECT * FROM {test_table};",
    con=postgres_engine
)

# drop test table - this will result in pandas error but should drop the table
drop_table_df = pd.read_sql(
    sql=f"DROP TABLE {test_table};",
    con=postgres_engine
)
