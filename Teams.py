import utils


def get_logo(team_name):
    '''
    '''
    query = '''
            SELECT LOGO
            FROM TEAMS
            WHERE TEAM_NAME = '{}'
            '''.format(team_name)

    data = utils.run_sql_query(query)

    logo = data['LOGO'][0]

    return logo
