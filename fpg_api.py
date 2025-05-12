from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger, swag_from
import os

import api.Players as Players
import api.Round as Round
import api.Results as Results
import api.Scores as Scores
import api.Choices as Choices
import api.Fixtures as Fixtures
import utils
# import Notifications
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "FPG API",
        "description": "API documentation for the FPG application",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [os.environ.get('schemes')],
    "paths": {},
    "definitions": {},
    "securityDefinitions": {
        "basicAuth": {
            "type": "basic"
        }
    }
}
swagger = Swagger(app, template=swagger_template)

USER_DATA = {
    os.environ.get('api_username'): os.environ.get('api_admin')
}


@auth.verify_password
def verify(username, password):
    '''
    '''
    if not (username, password):
        return False

    return USER_DATA.get(username) == password

# ----------------------------------------------------------------------------
# GET
# ----------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def index():
    '''
    '''
    return 'FPG API - V1.0.0 - RUNNING!'


@app.route('/current_round', methods=['GET'])
@swag_from('swagger/current_round.yml')
def get_current_round():
    '''
    '''
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    round_id = Round.get_current_round()

    utils.log_call(player_id, 'current_round')

    return {'Round ID': round_id}


# @app.route('/engine', methods=['GET'])
# @auth.login_required
# def engine():
#     '''
#     '''
#     Engine.main()

#     return {'Everyday Ran': True}


# @app.route('/get_all_tokens', methods=['GET'])
# @swag_from('swagger/get_all_tokens.yml')
# def get_all_tokens():
#     '''
#     '''
#     utils.log_call(None, get_all_tokens)

#     data = Notifications.get_all_tokens()

#     return data


@app.route('/get_available_choices', methods=['GET'])
@swag_from('swagger/get_available_choices.yml')
def get_available_choices():
    '''
    '''
    player_id = request.args.get('player_id')

    utils.log_call(player_id, 'get_available_choices')

    return Choices.get_available_choices(player_id)


@app.route('/get_choices', methods=['GET'])
@swag_from('swagger/get_choices.yml')
def get_choices():
    '''
    '''
    round_id = request.args.get('round_id')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    data = Choices.get_choices(round_id)

    utils.log_call(player_id, 'get_choices')

    return data


@app.route('/get_fixtures', methods=['GET'])
@swag_from('swagger/get_fixtures.yml')
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


# @app.route('/get_missing_pick_tokens', methods=['GET'])
# # @swag_from('swagger/get_missing_pick_tokens.yml')
# def get_missing_pick_tokens():
#     '''
#     '''
#     data = Notifications.get_missing_pick_tokens()

#     utils.log_call(None, 'get_missing_pick_tokens')

#     return data


@app.route('/get_player_info', methods=['GET'])
@swag_from('swagger/get_player_info.yml')
def get_player_info():
    '''
    '''
    player_id = request.args.get('player_id')

    player_info = Players.get_player_info(player_id)

    utils.log_call(player_id, 'get_player_info')

    return player_info


@app.route('/get_points', methods=['GET'])
@swag_from('swagger/get_points.yml')
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


@app.route('/get_previous_choices', methods=['GET'])
@swag_from('swagger/get_previous_choices.yml')
def get_previous_choices():
    '''
    '''
    player_id = request.args.get('player_id')

    prev_choices = Choices.get_previous_choices(player_id)

    utils.log_call(player_id, 'get_previous_choices')

    return prev_choices


@app.route('/get_previous_points', methods=['GET'])
@swag_from('swagger/get_previous_points.yml')
def get_previous_points():
    '''
    '''
    player_id = request.args.get('player_id')

    prev_points = Choices.get_previous_points(player_id)

    utils.log_call(player_id, 'get_previous_points')

    return prev_points


@app.route('/get_rolling_standings', methods=['GET'])
@swag_from('swagger/get_rolling_standings.yml')
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


@app.route('/get_round_info', methods=['GET'])
@swag_from('swagger/get_round_info.yml')
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


@app.route('/get_round_results', methods=['GET'])
@swag_from('swagger/get_round_results.yml')
def get_round_results():
    '''
    '''
    round_id = request.args.get('round_id')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    results = Results.get_round_results(round_id)

    utils.log_call(player_id, 'get_round_results')

    return results


@app.route('/get_season_overview', methods=['GET'])
@swag_from('swagger/get_season_overview.yml')
def get_season_overview():
    '''
    '''
    player_id = request.args.get('player_id')

    season_overview = Scores.get_season_overview(player_id)

    utils.log_call(player_id, 'get_season_overview')

    return season_overview


@app.route('/get_standings', methods=['GET'])
@swag_from('swagger/get_standings.yml')
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


@app.route('/get_weekly_info', methods=['GET'])
@swag_from('swagger/get_weekly_info.yml')
def get_weekly_info():
    '''
    '''
    player_id = request.args.get('player_id')
    round_id = request.args.get('round_id')

    weekly_info = Round.weekly_info(player_id, round_id)

    utils.log_call(player_id, 'get_weekly_info')

    return weekly_info


@app.route('/init_player', methods=['GET'])
@swag_from('swagger/init_player.yml')
def init_player():
    '''
    '''
    email = request.args.get('email')

    player_id = Players.init_player(email)

    utils.log_call(player_id, 'init_player')

    return {'player_id': int(player_id)}


# ----------------------------------------------------------------------------
# POST
# ----------------------------------------------------------------------------


@app.route('/make_choice', methods=['POST'])
@swag_from('swagger/make_choice.yml')
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
@swag_from('swagger/update_choice.yml')
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


# @app.route('/init_notifications', methods=['POST'])
# # @swag_from('swagger/init_notifications.yml')
# def init_notifications():
#     '''
#     '''
#     request_data = request.get_json()

#     player_id = request_data['player_id']
#     token = request_data['token']

#     init = Notifications.init_notifications(player_id, token)

#     utils.log_call(player_id, 'init_notifications')

#     return {'Notifications initialised': init}


if __name__ == '__main__':

    env = os.getenv('ENV')

    if env == 'uat':
        app.run(port=5000, host='0.0.0.0')

    elif env == 'local':
        app.run(debug=True)
