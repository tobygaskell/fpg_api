"""Module for retrieving fixture information for a round."""

import utils


def get_fixtures(round_id, season=2024):
    """Return fixture information for a round.

    PARAMS:
    round_id (int) - The round you want the fixtures for.

    Returns:
    data (json) - This is the json version of data returned from
    the query used to get the fixtures.

    """
    query = """
            SELECT F.*, HOME.HOME_LOGO, AWAY.AWAY_LOGO
            FROM (

            (SELECT *
             FROM FIXTURES
             WHERE ROUND = %s
             AND SEASON = %s) AS F

            LEFT JOIN

            (SELECT TEAM_NAME, LOGO AS HOME_LOGO
             FROM TEAMS
             WHERE SEASON = %s) as HOME

            ON F.HOME_TEAM = HOME.TEAM_NAME

            LEFT JOIN

            (SELECT TEAM_NAME, LOGO AS AWAY_LOGO
             FROM TEAMS
             WHERE SEASON = %s) AS AWAY

            ON F.AWAY_TEAM = AWAY.TEAM_NAME );
            """

    params = (round_id, season, season, season)

    data = utils.run_sql_query(query, params=params)

    return data.to_json(orient="records")
