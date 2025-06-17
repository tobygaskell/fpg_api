import utils


def get_round_info(round_id, season=2024):
    '''
    '''
    query = '''
            SELECT DP_ROUND, DMM_ROUND, CUT_OFF
            FROM ROUNDS
            WHERE ROUND = {}
            AND SEASON = {}
            LIMIT 1
            '''.format(round_id, season)

    data = utils.run_sql_query(query)
    doubled = bool(data['DP_ROUND'][0])
    dmm = bool(data['DMM_ROUND'][0])
    cut_off = data['CUT_OFF'][0]

    return doubled, dmm, cut_off


def get_current_round():
    '''
    '''
    query = '''
            SELECT ROUND_ID as current_round,
                   SEASON as season
            FROM CURRENT_ROUND
            '''

    data = utils.run_sql_query(query)

    round_id = data['current_round'][0]
    season = data['season'][0]

    return int(round_id), int(season)


def weekly_info(player_id, round_id, season):
    '''
    '''
    query = '''
            WITH a AS (
                SELECT *
                FROM CHOICES
                WHERE player_id = {}
                AND round = {}
                AND season = {}
            ),

            b AS (
                SELECT *
                FROM RESULTS
                WHERE round = {}
                AND SEASON = {}
            ),

            c AS (
                SELECT *
                FROM SCORES s
                WHERE round = {}
                AND SEASON = {}
                AND player_id = {}
            ),

            d AS (
                SELECT *
                FROM FIXTURES f
                WHERE ROUND = {}
                AND SEASON = {}
                AND (home_team IN (SELECT team_choice FROM a)
                OR away_team IN (SELECT team_choice FROM a))
            ),

            e AS (
            SELECT *
            FROM ROUNDS
            WHERE round = {}
            AND SEASON = {}
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
            '''.format(player_id, round_id, season,
                       round_id, season,
                       round_id, season, player_id,
                       round_id, season,
                       round_id, season)

    weekly_info = utils.run_sql_query(query)

    return weekly_info.to_json(orient='records')
