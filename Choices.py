import pandas as pd
import utils

def get_choices(round_id):
    '''
    TODO: Test
    '''
    query = '''
            SELECT PLAYER_ID, TEAM_CHOICE, ROUND
            FROM CHOICES
            WHERE ROUND = {}
            '''.format(round_id)
    
    choices = utils.run_sql_query(query)

    choices_dict = {row['PLAYER_ID']: row['TEAM_CHOICE'] for _, row in choices.iterrows()}

    return choices_dict

def make_choice(player, choice, round):
    '''
    TODO: Test
    '''
    query = '''
            INSERT INTO CHOICES
            (PLAYER_ID, TEAM_CHOICE, ROUND)
            values
            ({}, '{}', {});
            '''.format(player, choice, round)
    
    utils.run_sql_query(query, True)

    return True


def get_available_choices(player_id): 
    '''
    '''
    query = '''
            SELECT TEAM_NAME 
            FROM FPG.TEAMS
            WHERE TEAM_NAME NOT IN (SELECT TEAM_CHOICE
                                    FROM FPG.CHOICES 
                                    WHERE PLAYER_ID = {}
                                    GROUP BY TEAM_CHOICE
                                    HAVING COUNT(*) > 1)
            '''.format(player_id)
    
    data = utils.run_sql_query(query)

    return data.to_json(orient='records')


