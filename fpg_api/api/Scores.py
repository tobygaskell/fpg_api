import utils


def get_points(round_id, season=2024):
    '''
    '''
    query = '''
            WITH SEASON_SCORES AS (
                SELECT * FROM SCORES WHERE SEASON = {}
            )
            ,  SEASON_CHOICES AS (
                SELECT * FROM CHOICES WHERE SEASON = {}
            )

            SELECT p.player_id,
                SUBSTRING_INDEX(email, '@', 1)  AS User,
                team_choice                     AS Choice,
                CASE WHEN COALESCE(basic_points, 0) = 1 THEN 'Won'
                        WHEN COALESCE(basic_points, 0) = 0 THEN 'Drew'
                        WHEN COALESCE(basic_points, 0) = -1 THEN 'Lost'
                END as Result,
                COALESCE(basic_points, 0)       AS Basic,
                COALESCE(h2h_points, 0)         AS 'Head 2 Head',
                COALESCE(derby_points, 0)       AS Derby,
                COALESCE(dmm_points, 0)         AS 'Draw Means More',
                COALESCE(subtotal, 0)           AS Subtotal,
                COALESCE(total, 0)              AS Total
            FROM SEASON_SCORES as s
            LEFT JOIN PLAYERS as p
            on s.player_id = p.player_id
            LEFT JOIN SEASON_CHOICES AS c
            ON p.player_id = c.player_id AND s.round = c.round
            WHERE s.round = {}
            ORDER BY TOTAL DESC, Result Desc, Choice
            '''.format(season, season, round_id)

    points = utils.run_sql_query(query)

    return points.to_json(orient='records')


def get_season_overview(player_id, season=2024):
    '''
    '''
    query = '''
            WITH a AS (
                SELECT ROW_NUMBER() OVER (ORDER BY '1') AS round
                FROM CALL_LOGS cl
                LIMIT 38),

            b AS (
            SELECT PLAYER_ID,
                   ROUND,
                   COALESCE(BASIC_POINTS, 0) AS RESULT,
                   COALESCE(TOTAL, 0) AS POINTS
            FROM SCORES AS s
            WHERE player_id = {}
            AND season = {})

            SELECT a.round,
                COALESCE(b.player_id, {}) AS player_id,
                b.result,
                b.points
            FROM a
            LEFT JOIN b
            ON a.round = b.round
            ORDER BY a.ROUND;
            '''.format(player_id, season, player_id)

    season_overview = utils.run_sql_query(query)

    return season_overview.to_json(orient='records')
