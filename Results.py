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
