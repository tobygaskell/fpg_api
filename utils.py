import os
import pandas as pd
import mysql.connector
import requests
from sqlalchemy import create_engine
import yagmail
from dotenv import load_dotenv


load_dotenv()  # loads from .env by default


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


def get_api(url, querystring={}):
    '''
    '''
    headers = {
        "X-RapidAPI-Key": os.environ.get('api_key'),
        "X-RapidAPI-Host": os.environ.get('api_host')
    }
    response = requests.request("GET",
                                url,
                                headers=headers,
                                params=querystring)

    return response.json()


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


def send_email(email, subject, body):
    '''
    '''
    email_user = os.environ.get('email_user')
    email_pass = os.environ.get('email_pass')

    yag = yagmail.SMTP(email_user, email_pass)

    yag.send(email, subject, body)

    return True


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


def log_notification(token, title, body, sound, status):
    '''
    '''
    query = '''
            INSERT INTO NOTIFICATION_LOGS
            (token, title, body, sound, status, send_time)
            VALUES
            ('{}', '{}', '{}', '{}', '{}', CURRENT_TIMESTAMP(2));
            '''.format(token, title, body, sound, status)

    run_sql_query(query, True)
