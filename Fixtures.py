import utils



def get_fixtures(round_id): 
    '''
    '''
    query = '''
            SELECT F.*, HOME.HOME_LOGO, AWAY.AWAY_LOGO 
            FROM (

            (SELECT * 
            FROM FPG.FIXTURES 
            WHERE ROUND = {}) AS F

            LEFT JOIN 

            (SELECT TEAM_NAME, LOGO AS HOME_LOGO 
            FROM FPG.TEAMS) as HOME 
            
            ON F.HOME_TEAM = HOME.TEAM_NAME 

            LEFT JOIN 

            (SELECT TEAM_NAME, LOGO AS AWAY_LOGO

            FROM FPG.TEAMS ) AS AWAY

            ON F.AWAY_TEAM = AWAY.TEAM_NAME );
            '''.format(round_id)
    
    data = utils.run_sql_query(query)

    return data.to_json(orient= 'records')