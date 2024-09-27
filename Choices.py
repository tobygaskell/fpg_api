import pandas as pd
import utils
import Round
from datetime import datetime

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

def make_choice(player, choice, round_id):
    '''
    TODO: Test
    '''
    submitted = False

    _, _, cut_off = Round.get_round_info(round_id)

    if cut_off > datetime.now(): 

        query = '''
                SELECT COUNT(*) AS CHOICE_EXISTS 
                FROM CHOICES 
                WHERE PLAYER_ID = {}
                AND ROUND = {}
                '''.format(player, round_id)
        
        choices_exists = utils.run_sql_query(query)['CHOICE_EXISTS'][0]

        if choices_exists == 0:

            query = '''
                    INSERT INTO CHOICES
                    (PLAYER_ID, TEAM_CHOICE, ROUND)
                    values
                    ({}, '{}', {});
                    '''.format(player, choice, round_id)
            
            utils.run_sql_query(query, True)

            submitted = True
        
        else: 
            submitted = 'Already Chosen'

    else: 
        submitted = 'Too Late'

    return submitted

def get_available_choices(player_id): 
    '''
    '''
    query = '''
            SELECT TEAM_NAME 
            FROM TEAMS
            WHERE TEAM_NAME NOT IN (SELECT TEAM_CHOICE
                                    FROM CHOICES 
                                    WHERE PLAYER_ID = {}
                                    GROUP BY TEAM_CHOICE
                                    HAVING COUNT(*) > 1)
            '''.format(player_id)
    
    data = utils.run_sql_query(query)

    return data.to_json(orient='records')


def update_choice(player, choice, round_id): 
    '''
    '''
    query = '''
            UPDATE CHOICES
            SET TEAM_CHOICE = '{}'
            WHERE PLAYER_ID = {}
            AND ROUND = {}
            '''.format(choice, player, round_id)
    
    utils.run_sql_query(query, True)

    return True


def get_preious_choices(player_id): 
    '''
    '''
    print(player_id)
    query = '''
            select team_name as Choice, case when choice_cnt > 0 then True else False end as '1st Pick', 
                                        case when choice_cnt > 1 then True else False end as '2nd Pick' 

            from ((
            select team_name
            from FPG.TEAMS )  t 
            left join 
            (
            select Team_choice, count(*) as choice_cnt
            FROM FPG.CHOICES c
            WHERE PLAYER_ID = {}
            group by team_choice) as c
            on team_name = team_choice) 
            '''.format(player_id)
    data = utils.run_sql_query(query)
    return data.to_json(orient= 'records')