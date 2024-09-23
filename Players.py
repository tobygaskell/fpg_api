import utils


def get_player_id(email): 
    '''
    '''
    query = '''
            SELECT PLAYER_ID 
            FROM PLAYERS 
            WHERE EMAIL = '{}'
            '''.format(email)
#     print(query)
    return utils.run_sql_query(query)['PLAYER_ID'][0]

def init_player(email): 
    '''
    '''
    query = '''
            SELECT COUNT(DISTINCT PLAYER_ID) AS PLAYER_EXISTS
            FROM PLAYERS
            WHERE EMAIL = '{}'
            '''.format(email)

    if utils.run_sql_query(query)['PLAYER_EXISTS'][0] == 0: 

        query = '''
                INSERT INTO PLAYERS
                VALUES
                (NEXTVAL(PLAYER_IDS), '{}')
                '''.format(email)

        utils.run_sql_query(query, True)

    return get_player_id(email)