import utils 
import pandas as pd 

def init_results(round): 
    '''
    '''
    results = utils.get_api("https://api-football-v1.p.rapidapi.com/v3/fixtures?", 
                            {"league":"39", "season":"2024", "round":"Regular Season - {}".format(round)})
    
    results_df = pd.DataFrame({'FIXTURE_ID'     : [], 
                                'GAME_STATUS'   : [], 
                                'ROUND'         : [], 
                                'HOME_GOALS'    : [], 
                                'AWAY_GOALS'    : [], 
                                'SCORE'         : []})
    

    for i in range(results['results']):
        teams = []

        teams.append(results['response'][i]['teams']['home'])
        teams.append(results['response'][i]['teams']['away'])

        if len([i['name'] for i in teams if i['winner']]) == 1: 
            winner = [i['name'] for i in teams if i['winner']][0]

        else: 
            winner = 'Draw'

        home_goals = results['response'][i]['goals']['home']
        away_goals = results['response'][i]['goals']['away']

        new_row = pd.DataFrame({'FIXTURE_ID'    : [results['response'][i]['fixture']['id']], 
                                'GAME_STATUS'   : [results['response'][i]['fixture']['status']['long']], 
                                'ROUND'         : [results['response'][i]['league']['round'].split(' - ')[1]], 
                                'HOME_GOALS'    : [home_goals], 
                                'AWAY_GOALS'    : [away_goals], 
                                'SCORE'         : ['{} - {}'.format( home_goals, away_goals)], 
                                'WINNER'        : [winner]})

        results_df = pd.concat([results_df, new_row])

    return utils.append_sql(results_df, 'RESULTS')

def get_result(choice, fixture_id):
    '''
    TODO: Write Function
    '''
    query = '''
            SELECT * 
            FROM RESULTS
            WHERE FIXTURE_ID = {} 
            '''.format(fixture_id)
    
    data = utils.run_sql_query(query)

    status = data['GAME_STATUS'][0]

    winner = data['WINNER'][0]

    if status == 'Match Finished':

        if winner == 'Draw': 
            result = 'Draw'

        else: 
            if choice == winner: 
                result = 'Win'
            else: 
                result = 'Loss'
    else:
        result = None

    return result


def get_standings(): 
    '''
    '''
    # query = '''
    #         SELECT RANK() over (ORDER BY SUM(total) DESC) as POSITION, F.PLAYER_ID, SUBSTRING_INDEX(email, '@', 1) AS USER, SUM(total) AS SCORE 
    #         FROM SCORES AS F
    #         INNER JOIN PLAYERS AS P 
    #         ON F.PLAYER_ID = P.PLAYER_ID
    #         GROUP BY player_id 
    #         ORDER BY sum(total) desc;
    #         '''
    
    query = '''
            with base as (
            select distinct c.player_id, r.round, r.fixture_id, team_choice, home_team, away_team, home_goals, away_goals,  home_goals - away_goals as GD
            from FPG.RESULTS r 
            left join FPG.FIXTURES f 
            on r.FIXTURE_ID  = f.FIXTURE_ID 
            left join FPG.CHOICES c 
            on TEAM_CHOICE = home_team 
            and r.round = c.round
            left join FPG.PLAYERS p 
            on c.PLAYER_ID  = p.PLAYER_ID 

            union 

            select distinct c.player_id, r.round, r.fixture_id, team_choice, home_team, away_team, home_goals, away_goals, away_goals - home_goals as GD
            from FPG.RESULTS r 
            left join FPG.FIXTURES f 
            on r.FIXTURE_ID  = f.FIXTURE_ID 
            left join FPG.CHOICES c 
            on TEAM_CHOICE = away_team 
            and r.round = c.round
            left join FPG.PLAYERS p 
            on c.PLAYER_ID  = p.PLAYER_ID 
            )

            , subtotal as (
            select *, sum(GD) over (partition by player_id order by round asc) as rolling_gd
            from base
            where player_id is not null
            order by player_id, round desc
            )

            , standings as ( 
            SELECT  F.PLAYER_ID, SUBSTRING_INDEX(email, '@', 1) AS USER, SUM(total) AS SCORE 
            FROM FPG.SCORES AS F
            INNER JOIN FPG.PLAYERS AS P 
            ON F.PLAYER_ID = P.PLAYER_ID
            GROUP BY player_id 
            ORDER BY sum(total) desc
            )

            , totals as (
            select player_id, rolling_gd
            from subtotal
            where round in (select max(round) from subtotal) 
            )

            select RANK() over (ORDER BY score DESC, rolling_gd desc) as Position, stand.player_id, user as User, rolling_gd as 'Goal Diff', score as Score
            from standings as stand 
            inner join totals as t 
            on stand.player_id = t.player_id;
            '''
    data = utils.run_sql_query(query)

    return data.to_json(orient='records')

def get_rolling_standings():
    '''
    '''
    query = '''
            select *, rank() over (partition by round order by rolling_total desc ) as position
            from (SELECT distinct s.round, p.player_id, SUBSTRING_INDEX(email, '@', 1) AS USER, 
                         COALESCE(SUM(TOTAL) OVER (PARTITION by player_id order by s.round asc), 0) as rolling_total
            FROM SCORES AS s
            INNER JOIN PLAYERS AS p
            ON s.PLAYER_ID = p.PLAYER_ID
            INNER JOIN ROUNDS AS r
            on s.ROUND = r.ROUND
            ) as a;
            '''
    
    data = utils.run_sql_query(query)

    return data.to_json(orient='records')