"""Utility functions for SQL database operations and logging API calls."""

import logging
import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

load_dotenv(override=True)


def connect_sql():
    """Establish a connection to the SQL database and return the cursor and connection objects."""
    sql_user = os.environ.get("SQL_USER")
    sql_pass = os.environ.get("SQL_PASS")
    sql_host = os.environ.get("SQL_HOST")
    sql_db = os.environ.get("SQL_DB")

    config = {
        "user": sql_user,
        "password": sql_pass,
        "host": sql_host,
        "database": sql_db,
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    return cursor, conn


def run_sql_query(query, commit=False, params=()):
    """Execute a SQL query, optionally committing changes, and return the results as a DataFrame."""
    csr, conn = connect_sql()
    with csr as cur:
        cur.execute(query, params)
        if commit:
            conn.commit()
        try:
            if cur.description:  # Only attempt to fetch rows if results exist
                data = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
            else:
                data = pd.DataFrame()
        except Exception:
            logger.exception("Something went wrong")
            data = pd.DataFrame()

    return data


def append_sql(data, table):
    """Append a DataFrame to a specified SQL table using SQLAlchemy."""
    try:
        sql_user = os.environ.get("SQL_USER")
        sql_pass = os.environ.get("SQL_PASS")
        sql_host = os.environ.get("SQL_HOST")
        sql_db = os.environ.get("SQL_DB")

        c = f"mysql+mysqlconnector://{sql_user}:{sql_pass}@{sql_host}/{sql_db}"

        engine = create_engine(c)

        data.to_sql(table, engine, if_exists="append", index=False)

        engine.dispose()

    except BaseException:
        logger.exception("Something went wrong")
        return False
    else:
        return True


def log_call(player_id, endpoint):
    """Log an API call made by a player to a specific endpoint."""
    query = """
            INSERT INTO CALL_LOGS
            (player_id, endpoint, call_time)
            values
            (%s, %s, CURRENT_TIMESTAMP(2))
            """

    params = (player_id, endpoint)

    run_sql_query(query, True, params=params)

    return True
