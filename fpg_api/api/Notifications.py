"""File to store all of the notification endpoints."""

import utils


def init_notifications(player_id, token):
    """Initialize notifications for a player.

    Args:
        player_id (int): The ID of the player.
        token (str): The notification token.

    Returns:
        bool: True if initialization was successful, False otherwise.

    """
    token_exists = check_token_exists(player_id, token)

    if not token_exists:
        query = """
                INSERT INTO TOKENS (PLAYER_ID, TOKEN, CREATED_AT, ACTIVE)
                VALUES (%s, %s, CURRENT_TIMESTAMP(2), 1)
                """
        params = (player_id, token)

        utils.run_sql_query(query, True, params=params)

    token_active = check_token_active(player_id, token)

    if not token_active:
        query = """
                UPDATE TOKENS
                SET ACTIVE = 1
                WHERE PLAYER_ID = %s
                AND token = %s
                """
        params = (player_id, token)

        utils.run_sql_query(query, True, params=params)

    return True


def check_token_active(player_id, token):
    """Check if a notification token is active for a player.

    Args:
        player_id (int): The ID of the player.
        token (str): The notification token.

    Returns:
        bool: True if the token is active, False otherwise.

    """
    query = """
            SELECT ACTIVE
            FROM TOKENS
            WHERE PLAYER_ID = %s
            AND TOKEN = %s
            """
    params = (player_id, token)

    return utils.run_sql_query(query, params=params)["ACTIVE"][0] == 1


def check_token_exists(player_id, token):
    """Check if a notification token exists for a player.

    Args:
        player_id (int): The ID of the player.
        token: the expo string used to send notifications.

    Returns:
        bool: True if the token exists, False otherwise.

    """
    query = """
            SELECT COUNT(*) AS TOKEN_EXISTS
            FROM TOKENS
            WHERE PLAYER_ID = %s
            AND TOKEN = %s
            """

    params = (player_id, token)

    return utils.run_sql_query(query, params=params)["TOKEN_EXISTS"][0] > 0


def deactivate_notifications(token, player_id):
    """Deactivate Notifications when players log out of the app."""
    query = """
            UPDATE TOKENS
            SET ACTIVE = 0
            WHERE TOKEN = %s
            AND PLAYER_ID = %s
            """

    params = (token, player_id)

    utils.run_sql_query(query, True, params=params)

    return True
