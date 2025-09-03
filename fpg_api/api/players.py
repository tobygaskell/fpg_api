"""Module for player-related database operations and utilities."""

import utils


def get_player_id(email):
    """Get player ID."""
    query = """
            SELECT PLAYER_ID
            FROM PLAYERS
            WHERE EMAIL = %s
            """
    params = (email,)

    return utils.run_sql_query(query, params=params)["PLAYER_ID"][0]


def init_player(email, username="", team=""):
    """Initialise players."""
    query = """
            SELECT COUNT(DISTINCT PLAYER_ID) AS PLAYER_EXISTS
            FROM PLAYERS
            WHERE EMAIL = %s
            """
    params = (email,)

    if utils.run_sql_query(query, params=params)["PLAYER_EXISTS"][0] == 0:
        query = """
                INSERT INTO PLAYERS
                (PLAYER_ID, EMAIL, USERNAME, FAV_TEAM, CREATED_AT)
                VALUES
                (NEXTVAL(PLAYER_IDS), %s, %s, %s, CURRENT_TIMESTAMP(2));
                """
        params = (email, username, team)

        utils.run_sql_query(query, True, params=params)

    return get_player_id(email)


def get_player_info(player_id, season=2024):
    """Get player info."""
    query = """
            SELECT SUM(total) AS total_points,
                   SUM(CASE WHEN BASIC_POINTS = 1
                            THEN 1 ELSE 0 END) AS win_cnt,
                   SUM(CASE WHEN BASIC_POINTS = 0
                            THEN 1 ELSE 0 END) AS draw_cnt,
                   SUM(CASE WHEN BASIC_POINTS = -1
                            THEN 1 ELSE 0 END) AS lose_cnt,
                   COUNT(round) as round_cnt
            FROM SCORES
            WHERE PLAYER_ID = %s
            AND SEASON = %s
            """
    params = (player_id, season)

    return utils.run_sql_query(query, params=params).to_json(orient="records")


def get_username(player_id):
    """Get the username of a player by their player ID.

    Args:
        player_id (int): The ID of the player.

    Returns:
        str: The username of the player.

    """
    query = """
            SELECT COALESCE(NULLIF(username, ''),
                         SUBSTRING_INDEX(email, '@', 1)) AS USER
            FROM PLAYERS
            WHERE PLAYER_ID = %s
            """
    params = (player_id,)

    return utils.run_sql_query(query, params=params)["USER"][0]


def update_username(player_id, username):
    """Update the username of a player.

    Args:
        player_id (int): The ID of the player.
        username (str): The new username for the player.

    Returns:
        bool: True if the update was successful, False otherwise.

    """
    query = """
            UPDATE PLAYERS
            SET USERNAME = %s
            WHERE PLAYER_ID = %s
            """

    params = (username, player_id)

    utils.run_sql_query(query, True, params=params)

    return True
