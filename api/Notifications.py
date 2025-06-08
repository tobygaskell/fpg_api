import utils


def init_notifications(player_id, token):
    '''
    Initialize notifications for a player.

    Args:
        player_id (int): The ID of the player.
        token (str): The notification token.

    Returns:
        bool: True if initialization was successful, False otherwise.
    '''
    token_exists = check_token_exists(player_id, token)

    if not token_exists:
        query = '''
                INSERT INTO TOKENS (PLAYER_ID, TOKEN, CREATED_AT, ACTIVE)
                VALUES ({}, '{}', CURRENT_TIMESTAMP(2), 1)
                '''.format(player_id, token)

        utils.run_sql_query(query, True)

    token_active = check_token_active(player_id, token)

    if not token_active:
        query = '''
                UPDATE TOKENS
                SET ACTIVE = 1
                WHERE PLAYER_ID = {}
                AND token = '{}'
                '''.format(player_id, token)

        utils.run_sql_query(query, True)

    return True


def check_token_active(player_id, token):
    '''
    Check if a notification token is active for a player.

    Args:
        player_id (int): The ID of the player.
        token (str): The notification token.

    Returns:
        bool: True if the token is active, False otherwise.
    '''
    query = '''
            SELECT ACTIVE
            FROM TOKENS
            WHERE PLAYER_ID = {}
            AND TOKEN = '{}'
            '''.format(player_id, token)

    return utils.run_sql_query(query)['ACTIVE'][0] == 1


def check_token_exists(player_id, token):
    '''
    Check if a notification token exists for a player.

    Args:
        player_id (int): The ID of the player.

    Returns:
        bool: True if the token exists, False otherwise.
    '''
    query = '''
            SELECT COUNT(*) AS TOKEN_EXISTS
            FROM TOKENS
            WHERE PLAYER_ID = {}
            AND TOKEN = '{}'
            '''.format(player_id, token)

    return utils.run_sql_query(query)['TOKEN_EXISTS'][0] > 0


def deactivate_notifications(token, player_id):
    '''
    '''
    query = '''
            UPDATE TOKENS
            SET ACTIVE = 0
            WHERE TOKEN = '{}'
            AND PLAYER_ID = {}
            '''.format(token, player_id)

    utils.run_sql_query(query, True)

    return True
