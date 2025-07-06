"""Module for round-related API functions."""

import utils


def get_round_info(round_id, season=2024):
    """Retrieve round info such as DP_ROUND, DMM_ROUND, and CUT_OFF for a given round and season."""
    query = """
            SELECT DP_ROUND, DMM_ROUND, CUT_OFF
            FROM ROUNDS
            WHERE ROUND = %s
            AND SEASON = %s
            LIMIT 1
            """

    data = utils.run_sql_query(query, params=(round_id, season))
    doubled = bool(data["DP_ROUND"][0])
    dmm = bool(data["DMM_ROUND"][0])
    cut_off = data["CUT_OFF"][0]

    return doubled, dmm, cut_off


def get_current_round():
    """Retrieve the current round ID and season from the CURRENT_ROUND table."""
    query = """
            SELECT ROUND_ID as current_round,
                   SEASON as season
            FROM CURRENT_ROUND
            """

    data = utils.run_sql_query(query)
    round_id = data["current_round"][0]
    season = data["season"][0]

    return int(round_id), int(season)


def weekly_info(player_id, round_id, season):
    """Retrieve weekly information for a given round, player and season."""
    query = """
            WITH a AS (
                SELECT *
                FROM CHOICES
                WHERE player_id = %s
                AND round = %s
                AND season = %s
            ),

            b AS (
                SELECT *
                FROM RESULTS
                WHERE round = %s
                AND SEASON = %s
            ),

            c AS (
                SELECT *
                FROM SCORES s
                WHERE round = %s
                AND SEASON = %s
                AND player_id = %s
            ),

            d AS (
                SELECT *
                FROM FIXTURES f
                WHERE ROUND = %s
                AND SEASON = %s
                AND (home_team IN (SELECT team_choice FROM a)
                OR away_team IN (SELECT team_choice FROM a))
            ),

            e AS (
            SELECT *
            FROM ROUNDS
            WHERE round = %s
            AND SEASON = %s
            )

            SELECT a.round AS round,
                   a.player_id AS player_id,
                   a.team_choice AS pick,
                   d.home_team AS home_team,
                   d.away_team AS away_team,
                   b.home_goals AS home_goals,
                   b.away_goals AS away_goals,
                   c.basic_points AS basic,
                   c.h2h_points AS head_to_head,
                   c.derby_points AS derby,
                   c.dmm_points AS dmm,
                   c.lonely_points AS lonely_points,
                   e.dp_round AS Doubled,
                   COALESCE(c.total, 0) AS total,
                   COALESCE(c.subtotal, 0) as subtotal,
                   COALESCE(c.running_total, 0) as running_total,
                   c.docked_points as docked_points


            FROM a
            INNER JOIN b
            ON a.round = b.round
            INNER JOIN c
            ON a.round = c.round
            INNER JOIN d
            ON d.fixture_id = b.fixture_id
            INNER JOIN e
            ON a.ROUND = e.ROUND;
            """

    params = (
        player_id,
        round_id,
        season,  # a
        round_id,
        season,  # b
        round_id,
        season,
        player_id,  # c
        round_id,
        season,  # d
        round_id,
        season,  # e
    )

    weekly_info = utils.run_sql_query(query, params=params)

    return weekly_info.to_json(orient="records")
