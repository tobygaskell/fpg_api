from flask import Flask, request

import Players 
import Round 
import Results 
import Scores 
import Engine
import Choices
import Games
import Fixtures
import Teams

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

    score, basic_score, h2h_score, derby_score, dmm_score, subtotal = Scores.get_score(result, 
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
    choice = request_data['Choice']
    round_id = request_data['Round']

    fixture_id, h2h, derby = Games.get_game_info(choice, round_id)

    result = Results.get_result(choice, fixture_id)

    return {'Player'   : player, 
            'Result'   : result, 
            'Choice'   : choice, 
            'Round'    : round_id, 
            'H2H'      : h2h, 
            'Derby'    : derby}

@app.route('/get_teams', methods = ['GET'])
def get_teams(): 
    '''
    TODO: Write Functionality
    '''
    return {'Teams' : ['Team {}'.format(i+1) for i in range(20)]}

@app.route('/get_round_info', methods = ['POST'])
def get_round_info(): 
    '''    
    '''
    request_data = request.get_json()

    round = request_data['Round']

    doubled, dmm = Round.get_round_info(round)

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

    submitted = Choices.make_choice(player, choice, round)

    return {'Submitted': submitted}

@app.route('/get_choices', methods = ['POST'])
def get_choices(): 
    '''
    '''
    request_data = request.get_json()

    round_id = request_data['Round']

    data = Choices.get_choices(round_id)

    return {'data': data.to_json()}

@app.route('/init_round', methods = ['POST'])
def init_round(): 
    '''
    '''
    request_data = request.get_json()

    round_id = request_data['Round']

    init = Round.init_round(round_id)

    if init:
        message = 'Round {} info saved'.format(round_id)

    else:
        message = 'Round out of Scope'
        
    return {'Initialized' : init,
            'Round'       : round_id, 
            'Message'     : message} 

@app.route('/init_player', methods = ['POST'])
def init_player(): 
    '''
    '''
    request_data = request.get_json()

    email = request_data['Email']

    player_id = Players.init_player(email)

    return {'player_id': int(player_id)}

@app.route('/get_logo', methods = ['POST'])
def get_logo(): 
    '''
    '''
    request_data = request.get_json()

    team = request_data['Team']

    return {'Logo': Teams.get_logo(team)}

@app.route('/engine', methods = ['GET'])
def engine(): 
    '''
    '''
    Engine.main()

    return {'Everyday Ran' : True}

@app.route('/init_results', methods = ['POST'])
def init_results(): 
    '''
    '''
    request_data = request.get_json()

    round = request_data['Round']

    saved = Results.init_results(round)

    return {'Saved': saved}

@app.route('/get_fixtures', methods=['POST'])
def get_fixtures(): 
    '''
    '''
    request_data = request.get_json()
    round_id = request_data['Round']
    return Fixtures.get_fixtures(round_id)

@app.route('/get_available_choices', methods=['POST'])
def get_available_choices():
    '''
    '''
    request_data = request.get_json()
    player_id = request_data['Player']
    return Choices.get_available_choices(player_id)

@app.route('/current_round', methods=['GET'])
def get_current_round(): 
    '''
    '''
    round_id = Round.get_current_round()
    return {'Round ID' : round_id}

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)