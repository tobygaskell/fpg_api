import Choices
import Round
import utils


def get_game_info(choice, round_id):
    '''
    TODO: Test
    '''
    choices = Choices.get_choices(round_id)

    query = '''
            SELECT FIXTURE_ID, DERBY, CASE WHEN HOME_TEAM = '{}' 
                                           THEN AWAY_TEAM 
                                           ELSE HOME_TEAM END AS OPPO
            FROM FIXTURES
            WHERE ROUND = {}
            AND (HOME_TEAM = '{}'
              OR AWAY_TEAM = '{}')
            '''.format(choice, round_id, choice, choice)
    
    data = utils.run_sql_query(query)

    fixture_id = int(data['FIXTURE_ID'][0])
    derby = bool(data['DERBY'][0])
    oppo = data['OPPO'][0]

    h2h = False

    if oppo in choices.values():
        h2h = True

    return fixture_id, derby, h2h