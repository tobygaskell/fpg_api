import utils


def get_round_info(round_id):
    '''
    '''
    query = '''
            SELECT DP_ROUND, DMM_ROUND, CUT_OFF
            FROM ROUNDS
            WHERE ROUND = {}
            LIMIT 1
            '''.format(round_id)

    data = utils.run_sql_query(query)
    doubled = bool(data['DP_ROUND'][0])
    dmm = bool(data['DMM_ROUND'][0])
    cut_off = data['CUT_OFF'][0]

    return doubled, dmm, cut_off


def get_current_round():
    '''
    '''
    query = '''
            SELECT MAX(ROUND_ID) as current_round
            FROM CURRENT_ROUND
            '''

    round_id = utils.run_sql_query(query)['current_round'][0]

    return int(round_id)


def weekly_info(player_id, round_id):
    '''
    '''
    query = '''
            WITH a AS (
                SELECT *
                FROM CHOICES
                WHERE player_id = {}
                AND round = {}
            ),

            b AS (
                SELECT *
                FROM RESULTS
                WHERE round = {}
            ),

            c AS (
                SELECT *
                FROM SCORES s
                where round = {}
                AND player_id = {}
            ),

            d AS (
                SELECT *
                FROM FIXTURES f
                WHERE ROUND = {}
                AND (home_team IN (SELECT team_choice FROM a)
                OR away_team IN (SELECT team_choice FROM a))
            ),

            e AS (
            SELECT * FROM ROUNDS WHERE round = {}
            )

            SELECT a.round AS round,
                   a.player_id AS player_id,
                   a.team_choice AS pick,
                   d.home_team AS home_team,
                   d.away_team AS away_team,
                   b.home_goals AS home_goals,
                   b.away_goals AS away_goals,
                   COALESCE(c.basic_points, 0) AS basic,
                   COALESCE(c.h2h_points, 0) AS head_to_head,
                   COALESCE(c.derby_points, 0) AS derby,
                   COALESCE(c.dmm_points, 0) AS dmm,
                   0 AS lonely_points,
                   e.dp_round AS Doubled,
                   COALESCE(c.total, 0) AS total

            FROM a
            INNER JOIN b
            ON a.round = b.round
            INNER JOIN c
            ON a.round = c.round
            INNER JOIN d
            ON d.fixture_id = b.fixture_id
            INNER JOIN e
            ON a.ROUND = e.ROUND;
            '''.format(player_id, round_id, round_id,
                       round_id, player_id, round_id,
                       round_id)

    weekly_info = utils.run_sql_query(query)

    return weekly_info.to_json(orient='records')
