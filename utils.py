import os
import pandas as pd
import mysql.connector


def connect_sql():
    '''
    '''
    sql_user = os.environ.get('sql_user')
    sql_pass = os.environ.get('sql_pass')
    sql_host = os.environ.get('sql_host')
    sql_db = os.environ.get('sql_db')

    config = {
        'user'     : sql_user,
        'password' : sql_pass,
        'host'     : sql_host,
        'database' : sql_db
    }

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    return cursor, conn

def run_sql_query(query, commit = False):
    '''
    '''
    csr, conn = connect_sql()

    with csr as cur: 
        cur.execute(query)
        if commit: 
            conn.commit()
        try: 
            data = pd.DataFrame.from_records(iter(cur), columns = [x[0] for x in cur.description])
        except:
            data = pd.DataFrame()

    return data
