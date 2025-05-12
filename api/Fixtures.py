import utils


def get_fixtures(round_id):
    '''
    This Function will take in a round id and return the fixture
    information for that round including the logo urls for the
    home and away team.

    PARAMS:
    round_id (int) - Theround you want the fixtures for.

    RETURNS:
    data (json) - This is the json version of data returned from
    the query used to get the fixtures.
    '''
    query = '''
            SELECT F.*, HOME.HOME_LOGO, AWAY.AWAY_LOGO
            FROM (

            (SELECT *
             FROM FIXTURES
             WHERE ROUND = {}) AS F

            LEFT JOIN

            (SELECT TEAM_NAME, LOGO AS HOME_LOGO
             FROM TEAMS) as HOME

            ON F.HOME_TEAM = HOME.TEAM_NAME

            LEFT JOIN

            (SELECT TEAM_NAME, LOGO AS AWAY_LOGO
             FROM TEAMS ) AS AWAY

            ON F.AWAY_TEAM = AWAY.TEAM_NAME );
            '''.format(round_id)

    data = utils.run_sql_query(query)

    return data.to_json(orient='records')
