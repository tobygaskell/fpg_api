from flask import Flask, request, render_template
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger, swag_from
from datetime import datetime
import os


import fpg_api.api.Players as Players
import fpg_api.api.Round as Round
import fpg_api.api.Results as Results
import fpg_api.api.Scores as Scores
import fpg_api.api.Choices as Choices
import fpg_api.api.Fixtures as Fixtures
import fpg_api.api.Notifications as Notifications
import utils

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

schemes = os.environ.get('schemes') if os.environ.get('schemes') else 'https'

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "FPG API",
        "description": "API documentation for the FPG application",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [schemes],
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


@app.route('/api', methods=['GET'])
def index():
    hostname = os.getenv('HOSTNAME', 'localhost')
    year = datetime.now().year
    return render_template('api.html', hostname=hostname, year=year)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/current_round', methods=['GET'])
@swag_from('swagger/current_round.yml')
def get_current_round():
    '''
    '''
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    round_id, season = Round.get_current_round()

    utils.log_call(player_id, 'current_round')

    return {'Round ID': round_id,
            'season': season}


@app.route('/deactivate_notifications', methods=['GET'])
@swag_from('swagger/deactivate_notifications.yml')
def deactivate_notifications():
    '''
    '''
    player_id = request.args.get('player_id')

    token = request.args.get('token')

    utils.log_call(player_id, 'deactivate_notifications')

    data = Notifications.deactivate_notifications(token, player_id)

    return {'Notifications deactivated': data}


@app.route('/get_available_choices', methods=['GET'])
@swag_from('swagger/get_available_choices.yml')
def get_available_choices():
    '''
    '''

    player_id = request.args.get('player_id')

    season = request.args.get('season')

    utils.log_call(player_id, 'get_available_choices')

    return Choices.get_available_choices(player_id, season)


@app.route('/get_choices', methods=['GET'])
@swag_from('swagger/get_choices.yml')
def get_choices():
    '''
    '''
    round_id = request.args.get('round_id')

    season = request.args.get('season')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    try:
        inc_method = request.args.get('inc_method')
        inc_method = inc_method.lower() == 'true'
    except BaseException:
        inc_method = False

    data = Choices.get_choices(round_id, season, inc_method)

    utils.log_call(player_id, 'get_choices')

    return data


@app.route('/get_fixtures', methods=['GET'])
@swag_from('swagger/get_fixtures.yml')
def get_fixtures():
    '''
    '''
    round_id = request.args.get('round_id')

    season = request.args.get('season')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    utils.log_call(player_id, 'get_fixtures')

    return Fixtures.get_fixtures(round_id, season)


@app.route('/get_player_info', methods=['GET'])
@swag_from('swagger/get_player_info.yml')
def get_player_info():
    '''
    '''
    player_id = request.args.get('player_id')

    season = request.args.get('season')

    player_info = Players.get_player_info(player_id, season)

    utils.log_call(player_id, 'get_player_info')

    return player_info


@app.route('/get_points', methods=['GET'])
@swag_from('swagger/get_points.yml')
def get_points():
    '''
    '''
    round_id = request.args.get('round_id')

    season = request.args.get('season')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    scores = Scores.get_points(round_id, season)

    utils.log_call(player_id, 'get_points')

    return scores


@app.route('/get_previous_choices', methods=['GET'])
@swag_from('swagger/get_previous_choices.yml')
def get_previous_choices():
    '''
    '''
    player_id = request.args.get('player_id')

    season = request.args.get('season')

    prev_choices = Choices.get_previous_choices(player_id, season)

    utils.log_call(player_id, 'get_previous_choices')

    return prev_choices


@app.route('/get_previous_points', methods=['GET'])
@swag_from('swagger/get_previous_points.yml')
def get_previous_points():
    '''
    '''
    player_id = request.args.get('player_id')

    season = request.args.get('season')

    prev_points = Choices.get_previous_points(player_id, season)

    utils.log_call(player_id, 'get_previous_points')

    return prev_points


@app.route('/get_rolling_standings', methods=['GET'])
@swag_from('swagger/get_rolling_standings.yml')
def get_rolling_standings():
    '''
    '''
    season = request.args.get('season')
    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    rolling_standings = Results.get_rolling_standings(season)

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

    season = request.args.get('season')

    doubled, dmm, cut_off = Round.get_round_info(round_id, season)

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
    season = request.args.get('season')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    results = Results.get_round_results(round_id, season)

    utils.log_call(player_id, 'get_round_results')

    return results


@app.route('/get_season_overview', methods=['GET'])
@swag_from('swagger/get_season_overview.yml')
def get_season_overview():
    '''
    '''
    player_id = request.args.get('player_id')
    season = request.args.get('season')

    season_overview = Scores.get_season_overview(player_id, season)

    utils.log_call(player_id, 'get_season_overview')

    return season_overview


@app.route('/get_standings', methods=['GET'])
@swag_from('swagger/get_standings.yml')
def get_standings():
    '''
    '''
    season = request.args.get('season')

    try:
        player_id = request.args.get('player_id')
    except BaseException:
        player_id = None

    standings = Results.get_standings(season)

    utils.log_call(player_id, 'get_standings')

    return standings


@app.route('/get_weekly_info', methods=['GET'])
@swag_from('swagger/get_weekly_info.yml')
def get_weekly_info():
    '''
    '''
    player_id = request.args.get('player_id')
    round_id = request.args.get('round_id')
    season = request.args.get('season')

    weekly_info = Round.weekly_info(player_id, round_id, season)

    utils.log_call(player_id, 'get_weekly_info')

    return weekly_info


@app.route('/get_username', methods=['GET'])
@swag_from('swagger/get_username.yml')
def get_username():
    '''
    '''
    player_id = request.args.get('player_id')

    username = Players.get_username(player_id)

    utils.log_call(player_id, 'get_username')

    return {'Username': username}


@app.route('/rules', methods=['GET'])
def rules():
    '''
    '''
    return render_template('rules.html')


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

@app.route('/init_notifications', methods=['POST'])
@swag_from('swagger/init_notifications.yml')
def init_notifications():
    '''
    '''
    request_data = request.get_json()

    player_id = request_data['player_id']
    token = request_data['token']

    init = Notifications.init_notifications(player_id, token)

    utils.log_call(player_id, 'init_notifications')

    return {'Notifications initialised': init}


@app.route('/init_player_app', methods=['POST'])
# @swag_from('swagger/init_player_app.yml')
def init_player_app():
    '''
    '''
    request_data = request.get_json()

    email = request_data['Email']

    try:
        username = request_data['Username']
    except KeyError:
        username = ''

    try:
        team = request_data['Team']
    except KeyError:
        team = ''

    player_id = Players.init_player(email, username, team)

    utils.log_call(player_id, 'init_player_app')

    return {'player_id': int(player_id)}


@app.route('/make_choice', methods=['POST'])
@swag_from('swagger/make_choice.yml')
def make_choice():
    '''
    '''
    request_data = request.get_json()

    choice = request_data['Choice']
    player = request_data['Player']
    round = request_data['Round']
    season = request_data['season']

    submitted = Choices.make_choice(player, choice, round, season)

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
    season = request_data['season']

    updated = Choices.update_choice(player, choice, round_id, season)

    utils.log_call(player, 'update_choice')

    return {'Updated': updated}


@app.route('/update_username', methods=['POST'])
@swag_from('swagger/update_username.yml')
def update_username():
    '''
    '''
    request_data = request.get_json()

    player_id = request_data['player_id']
    username = request_data['new_username']

    updated = Players.update_username(player_id, username)

    utils.log_call(player_id, 'update_username')

    return {'Updated': updated}