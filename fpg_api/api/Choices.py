import utils
import fpg_api.api.Round as Round
from datetime import datetime


def get_choices(round_id, season=2024, inc_method=False):
    '''
    This Function will get the already chosen teams from the
    database and return them in a python dictionary

    Args:
        round_id (int): the round you would like to see the
        choices for

    Returns:
        dict: a dict with the player ID as the key and the
        team choice as the value
    '''
    query = '''
            SELECT PLAYER_ID, TEAM_CHOICE, ROUND, METHOD
            FROM CHOICES
            WHERE ROUND = {}
            AND SEASON = {}
            '''.format(round_id, season)

    choices = utils.run_sql_query(query)
    if inc_method:
        choices_dict = {row['PLAYER_ID']: {'Choice': row['TEAM_CHOICE'],
                                           'Method': row['METHOD']} for _,
                        row in choices.iterrows()}
    else:
        choices_dict = {row['PLAYER_ID']: row['TEAM_CHOICE'] for _,
                        row in choices.iterrows()}

    return choices_dict


def make_choice(player, choice, round_id, season=2024):
    '''
    _summary_

    Args:
        player (_type_): _description_
        choice (_type_): _description_
        round_id (_type_): _description_

    Returns:
        _type_: _description_
    '''
    submitted = False

    _, _, cut_off = Round.get_round_info(round_id, season)

    if cut_off > datetime.now():

        query = '''
                SELECT COUNT(*) AS CHOICE_EXISTS
                FROM CHOICES
                WHERE PLAYER_ID = {}
                AND SEASON = {}
                AND ROUND = {}
                '''.format(player, season, round_id)

        choices_exists = utils.run_sql_query(query)['CHOICE_EXISTS'][0]

        if choices_exists == 0:

            query = '''
                    INSERT INTO CHOICES
                    (PLAYER_ID, TEAM_CHOICE, ROUND, SEASON)
                    values
                    ({}, '{}', {}, {});
                    '''.format(player, choice, round_id, season)

            utils.run_sql_query(query, True)

            submitted = True

        else:
            submitted = 'Already Chosen'

    else:
        submitted = 'Too Late'

    return submitted


def get_available_choices(player_id, season=2024):
    '''
    _summary_

    Args:
        player_id (_type_): _description_

    Returns:
        _type_: _description_
    '''
    query = '''
            SELECT TEAM_NAME
            FROM TEAMS
            WHERE SEASON = {}
            AND TEAM_NAME NOT IN (SELECT TEAM_CHOICE
                                FROM CHOICES
                                WHERE PLAYER_ID = {}
                                AND SEASON = {}
                                GROUP BY TEAM_CHOICE
                                HAVING COUNT(*) > 1)
            '''.format(season, player_id, season)

    data = utils.run_sql_query(query)

    return data.to_json(orient='records')


def update_choice(player, choice, round_id, season=2024):
    '''
    _summary_

    Args:
        player (_type_): _description_
        choice (_type_): _description_
        round_id (_type_): _description_

    Returns:
        _type_: _description_
    '''
    query = '''
            UPDATE CHOICES
            SET TEAM_CHOICE = '{}'
            WHERE PLAYER_ID = {}
            AND ROUND = {}
            AND SEASON = {}
            '''.format(choice, player, round_id, season)

    utils.run_sql_query(query, True)

    return True


def get_previous_choices(player_id, season=2024):
    '''
    _summary_

    Args:
        player_id (_type_): _description_

    Returns:
        _type_: _description_
    '''
    query = '''
            SELECT team_name as Choice, case when choice_cnt > 0
                                            then True else False
                                        end as '1st Pick',
                                        case when choice_cnt > 1
                                            then True else False
                                        end as '2nd Pick'

            from ((
            select team_name
            from TEAMS
            WHERE SEASON = {}) AS t
            left join
            (
            select Team_choice, count(*) as choice_cnt
            FROM CHOICES c
            WHERE PLAYER_ID = {}
            AND SEASON = {}
            and c.round <> (SELECT ROUND_ID from CURRENT_ROUND)
            group by team_choice) as c
            on team_name = team_choice)
            ORDER BY case when choice_cnt > 1
                        then True else False end desc,
                    case when choice_cnt > 0
                        then True else False end desc, Choice
            '''.format(season, player_id, season)

    data = utils.run_sql_query(query)

    return data.to_json(orient='records')


def get_previous_points(player_id, season=2024):
    '''
    '''
    query = '''
            WITH a as (
                select s.player_id, s.round,
                    COALESCE(total, 0) as total,
                    c.team_choice
                from ((SELECT * FROM SCORES WHERE SEASON = {}) s
                inner join (SELECT * FROM CHOICES WHERE SEASON = {}) c
                on s.round = c.ROUND
                and s.PLAYER_ID = c.PLAYER_ID )
                where s.player_id = {}
                order by s.round
                )

            , first_pick as (
                select c.team_choice, coalesce(total, 0) as first_pick
                from (
                (select * from a) as c
                inner join
                (select team_choice, min(round) as first_pick
                from a
                group by team_choice) as b
                on c.team_choice = b.team_choice
                and c.round = b.first_pick))

            , second_pick as (
                select c.team_choice, coalesce(total, 0) as second_pick
                from (
                (select * from a) as c
                inner join
                (select team_choice, max(round) as second_pick,
                        count(*) as pick_cnt
                from a
                group by team_choice
                having pick_cnt = 2 ) as b
                on c.team_choice = b.team_choice
                and c.round = b.second_pick))

            select COALESCE(q.team_choice, t.team_name) as Choice,
                first_pick as '1st Pick',
            second_pick as '2nd Pick'
            from first_pick as q
            left join second_pick as w
            on q.team_choice = w.team_choice
            right join (SELECT * FROM TEAMS WHERE SEASON = {}) t
            on q.team_choice = t.TEAM_NAME
            order by coalesce(second_pick, -100000) desc,
                    coalesce(first_pick, -100000) desc,
                    Choice
            '''.format(season, season, player_id, season)

    data = utils.run_sql_query(query)

    return data.to_json(orient='records')
