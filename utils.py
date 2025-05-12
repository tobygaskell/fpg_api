import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv(override=True)  # loads from .env by default


def connect_sql():
    '''
    '''
    sql_user = os.environ.get('sql_user')
    sql_pass = os.environ.get('sql_pass')
    sql_host = os.environ.get('sql_host')
    sql_db = os.environ.get('sql_db')

    config = {
        'user': sql_user,
        'password': sql_pass,
        'host': sql_host,
        'database': sql_db
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    return cursor, conn


def run_sql_query(query, commit=False):
    '''
    '''
    csr, conn = connect_sql()

    with csr as cur:
        cur.execute(query)
        if commit:
            conn.commit()
        try:
            data = pd.DataFrame.from_records(
                iter(cur),
                columns=[x[0] for x in cur.description]
                )
        except BaseException:
            data = pd.DataFrame()

    return data


def append_sql(data, table):
    '''
    '''
    try:
        sql_user = os.environ.get('sql_user')
        sql_pass = os.environ.get('sql_pass')
        sql_host = os.environ.get('sql_host')
        sql_db = os.environ.get('sql_db')

        c = f'mysql+mysqlconnector://{sql_user}:{sql_pass}@{sql_host}/{sql_db}'

        engine = create_engine(c)

        data.to_sql(table, engine, if_exists='append', index=False)

        engine.dispose()

        return True
    except BaseException:
        return False


def log_call(player_id, endpoint):
    '''
    Args:
        player_id (_type_): _description_
        endpoint (_type_): _description_
    '''
    query = '''
            INSERT INTO CALL_LOGS
            (player_id, endpoint, call_time)
            values
            ({}, '{}', CURRENT_TIMESTAMP(2))
            '''.format(player_id if player_id else 'null', endpoint)

    run_sql_query(query, True)

    return True
