from flask import Flask, request
import get_score as gs
import random
import utils
import init_player as p_init
app = Flask(__name__)

@app.route('/get_score', methods=['POST'])
def get_score():
    '''
    '''
    request_data = request.get_json()

    player = request_data['Player']
    result = request_data['Result']
    h2h = request_data['H2H']
    derby = request_data['Derby']
    dmm = request_data['DMM']
    doubled = request_data['Doubled']

    score, basic_score, h2h_score, derby_score, dmm_score, subtotal = gs.main(result, 
                                                                              h2h, 
                                                                              derby, 
                                                                              dmm, 
                                                                              doubled)

    return {'Player'     : player,
            'Score'      : score, 
            'Basic'      : basic_score, 
            'H2H'        : h2h_score, 
            'Derby'      : derby_score, 
            'DMM'        : dmm_score, 
            'Sub Total'  : subtotal}

@app.route('/get_result', methods = ['POST'])
def get_result(): 
    '''
    '''
    request_data = request.get_json()

    player = request_data['Player']
    team = request_data['Choice']
    round = request_data['Round']

    result = random.choice(['Win', 'Lose', 'Draw'])

    teams = get_teams()['Teams']

    oppo = random.choice(teams)

    if result == 'Win': 
        score = '2-1'
    
    elif result == 'Draw': 
        score = '1-1'

    elif result == 'Lose': 
        score = '0-3'

    venue = random.choice(['Home', 'Away'])

    h2h = random.choice([True, False])

    derby = random.choice([True, False])

    return {'Player'   : player, 
            'Result'   : result, 
            'Choice'   : team, 
            'Round'    : round, 
            'Opponent' : oppo, 
            'Score'    : score, 
            'Venue'    : venue, 
            'H2H'      : h2h, 
            'Derby'    : derby}

@app.route('/get_teams', methods = ['GET'])
def get_teams(): 
    '''
    '''
    return {'Teams' : ['Team {}'.format(i+1) for i in range(20)]}

@app.route('/get_round_info', methods = ['POST'])
def get_round_info(): 
    '''    
    '''
    request_data = request.get_json()

    round = request_data['Round']

    query = '''
            SELECT doubled, dmm
            FROM round_info
            WHERE round = {}
            LIMIT 1
            '''.format(round)
    
    data = utils.run_sql_query(query)

    doubled = bool(data['doubled'][0])
    dmm = bool(data['dmm'][0])

    return {'Round'  : round, 
            'Double' : doubled, 
            'DMM'    : dmm}

@app.route('/make_choice', methods = ['POST'])
def make_choice(): 
    '''
    '''
    request_data = request.get_json()

    choice = request_data['Choice']
    player = request_data['Player']
    round  = request_data['Round']

    query = '''
            INSERT INTO CHOICES
            (PLAYER_ID, TEAM_CHOICE, ROUND, FIXTURE_ID)
            values
            ({}, '{}', {}, {});
            '''.format(player, choice, round, 10)
    
    utils.run_sql_query(query, True)

    return {'Submitted': True, 
            'query': query}

@app.route('/get_choices', methods = ['GET'])
def get_choice(): 
    '''
    '''
    query = '''
            select * from CHOICE
            '''
    
    data = utils.run_sql_query(query)

    print(data)

    return {'data': data.to_json()}


@app.route('/init_round', methods = ['POST'])
def init_round(): 
    '''
    '''
    request_data = request.get_json()

    round = request_data['Round']

    if round > 0 and round < 38:

        dmm = random.randrange(100) < 10
        doubled = random.randrange(100) < 10

        query = '''
                INSERT INTO ROUNDS
                (ROUND, DP_ROUND, DMM_ROUND)
                values
                ({}, {}, {});
                '''.format(round, doubled, dmm)
        
        utils.run_sql_query(query, True)

        init = True
        message = 'Round {} info saved'.format(round)

    else:
        init = False
        message = 'Round out of Scope'
        
    return {'Initialized' : init,
            'Round'       : round, 
            'Message'     : message}


@app.route('/init_player', methods = ['POST'])
def init_player(): 
    '''
    '''
    request_data = request.get_json()

    email = request_data['Email']

    player_id = p_init.check_if_player(email)

    print(player_id)

    return {'player_id': int(player_id)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)