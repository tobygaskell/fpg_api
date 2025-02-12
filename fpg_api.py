from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import os

import Players
import Round
import Results
import Scores
import Engine
import Choices
import Games
import Fixtures
import Teams
import utils

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {
    os.environ.get('api_username'): os.environ.get('api_admin')
}


@auth.verify_password
def verify(username, password):
    '''
    '''
    # print(username)
    # print(password)
    # print(USER_DATA.get(username))
    if not (username, password):
        return False

    return USER_DATA.get(username) == password


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

    score, basic_score, h2h_score, derby_score, dmm_score, subtotal = (
        Scores.get_score(result, h2h, derby, dmm, doubled)
        )

    return {'Player': player,
            'Score': score,
            'Basic': basic_score,
            'H2H': h2h_score,
            'Derby': derby_score,
            'DMM': dmm_score,
            'Sub Total': subtotal}


@app.route('/get_result', methods=['POST'])
def get_result():
    '''
    '''
    request_data = request.get_json()

    player = request_data['Player']
    choice = request_data['Choice']
    round_id = request_data['Round']

    fixture_id, h2h, derby = Games.get_game_info(choice, round_id)

    result = Results.get_result(choice, fixture_id)

    return {'Player': player,
            'Result': result,
            'Choice': choice,
            'Round': round_id,
            'H2H': h2h,
            'Derby': derby}


@app.route('/init_round', methods=['POST'])
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

    return {'Initialized': init,
            'Round': round_id,
            'Message': message}


@app.route('/get_logo', methods=['POST'])
def get_logo():
    '''
    '''
    request_data = request.get_json()

    team = request_data['Team']

    return {'Logo': Teams.get_logo(team)}


@app.route('/init_results', methods=['POST'])
def init_results():
    '''
    '''
    request_data = request.get_json()

    round = request_data['Round']

    saved = Results.init_results(round)

    return {'Saved': saved}


@app.route('/calculate_scores', methods=['POST'])
def calculate_scores():
    '''
    '''
    request_data = request.get_json()

    round_id = request_data['Round']

    calculated = Scores.calculate_scores(round_id)

    return {'Calculated': calculated}


# ----------------------------------------------------------------------------
# GET
# ----------------------------------------------------------------------------


@app.route('/get_round_info', methods=['GET'])
@auth.login_required
def get_round_info():
    '''
    '''
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    round_id = request.args.get('round_id')

    doubled, dmm, cut_off = Round.get_round_info(round_id)

    utils.log_call(player_id, 'get_round_info')

    return {'Round': round_id,
            'Double': doubled,
            'DMM': dmm,
            'Cut Off': cut_off}


@app.route('/get_choices', methods=['GET'])
@auth.login_required
def get_choices():
    '''
    '''
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    round_id = request.args.get('round_id')

    data = Choices.get_choices(round_id)

    utils.log_call(player_id, 'get_choices')

    return data


@app.route('/init_player', methods=['GET'])
@auth.login_required
def init_player():
    '''
    '''
    email = request.args.get('email')

    player_id = Players.init_player(email)

    utils.log_call(player_id, 'init_player')

    return {'player_id': int(player_id)}


@app.route('/engine', methods=['GET'])
@auth.login_required
def engine():
    '''
    '''
    Engine.main()

    return {'Everyday Ran': True}


@app.route('/get_fixtures', methods=['GET'])
@auth.login_required
def get_fixtures():
    '''
    '''
    round_id = request.args.get('round_id')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    utils.log_call(player_id, 'get_fixtures')

    return Fixtures.get_fixtures(round_id)


@app.route('/get_available_choices', methods=['GET'])
@auth.login_required
def get_available_choices():
    '''
    '''
    player_id = request.args.get('player_id')

    utils.log_call(player_id, 'get_available_choices')

    return Choices.get_available_choices(player_id)


@app.route('/current_round', methods=['GET'])
@auth.login_required
def get_current_round():
    '''
    '''
    round_id = Round.get_current_round()

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    utils.log_call(player_id, 'current_round')

    return {'Round ID': round_id}


@app.route('/get_standings', methods=['GET'])
@auth.login_required
def get_standings():
    '''
    '''
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    standings = Results.get_standings()

    utils.log_call(player_id, 'get_standings')

    return standings


@app.route('/get_points', methods=['GET'])
@auth.login_required
def get_points():
    '''
    '''
    round_id = request.args.get('round_id')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    scores = Scores.get_points(round_id)

    utils.log_call(player_id, 'get_points')

    return scores


@app.route('/get_rolling_standings', methods=['GET'])
@auth.login_required
def get_rolling_standings():
    '''
    '''
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    rolling_standings = Results.get_rolling_standings()

    utils.log_call(player_id, 'get_rolling_standings')

    return rolling_standings


@app.route('/get_previous_choices', methods=['GET'])
@auth.login_required
def get_previous_choices():
    '''
    '''
    player_id = request.args.get('player_id')

    prev_choices = Choices.get_previous_choices(player_id)

    utils.log_call(player_id, 'get_previous_choices')

    return prev_choices


@app.route('/get_previous_points', methods=['GET'])
@auth.login_required
def get_previous_points():
    '''
    '''
    player_id = request.args.get('player_id')

    prev_points = Choices.get_previous_points(player_id)

    utils.log_call(player_id, 'get_previous_points')

    return prev_points


@app.route('/get_player_info', methods=['GET'])
@auth.login_required
def get_player_info():
    '''
    '''
    player_id = request.args.get('player_id')

    player_info = Players.get_player_info(player_id)

    utils.log_call(player_id, 'get_player_info')

    return player_info

# ----------------------------------------------------------------------------
# POST
# ----------------------------------------------------------------------------


@app.route('/make_choice', methods=['POST'])
@auth.login_required
def make_choice():
    '''
    '''
    request_data = request.get_json()

    choice = request_data['Choice']
    player = request_data['Player']
    round = request_data['Round']

    submitted = Choices.make_choice(player, choice, round)

    utils.log_call(player, 'make_choice')

    return {'Submitted': submitted}


@app.route('/update_choice', methods=['POST'])
@auth.login_required
def update_choice():
    '''
    '''
    request_data = request.get_json()

    choice = request_data['Choice']
    player = request_data['Player']
    round_id = request_data['Round']

    updated = Choices.update_choice(player, choice, round_id)

    utils.log_call(player, 'update_choice')

    return {'Updated': updated}


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)
