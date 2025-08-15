"""Flask application providing the FPG API endpoints and documentation."""

import os

from dotenv import load_dotenv
from flasgger import Swagger, swag_from
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth

import utils
from fpg_api.api import Choices, Fixtures, Notifications, players, results, scores
from fpg_api.api import rounds as round_api

load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

schemes = os.environ.get("SCHEMES") if os.environ.get("SCHEMES") else "https"

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "FPG API",
        "description": "API documentation for the FPG application",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": [schemes],
    "paths": {},
    "definitions": {},
    "securityDefinitions": {
        "basicAuth": {
            "type": "basic",
        },
    },
}
swagger = Swagger(app, template=swagger_template)


# ----------------------------------------------------------------------------
# Webpages
# ----------------------------------------------------------------------------


@app.route("/api", methods=["GET"])
def api():
    """Render the API documentation page."""
    hostname = os.getenv("HOSTNAME", "localhost")
    return render_template("api.html", hostname=hostname)


@app.route("/", methods=["GET"])
def home():
    """Render the home page."""
    return render_template("home.html")


@app.route("/rules", methods=["GET"])
def rules():
    """Render the rules page."""
    return render_template("rules.html")


# ----------------------------------------------------------------------------
# GET
# ----------------------------------------------------------------------------


@app.route("/current_round", methods=["GET"])
@swag_from("swagger/current_round.yml")
def get_current_round():
    """Get the current round ID and season for the FPG API."""
    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    round_id, season = round_api.get_current_round()

    utils.log_call(player_id, "current_round")

    return {"Round ID": round_id, "season": season}


@app.route("/deactivate_notifications", methods=["GET"])
@swag_from("swagger/deactivate_notifications.yml")
def deactivate_notifications():
    """Deactivate notifications for a player using their token and player_id."""
    player_id = request.args.get("player_id")

    token = request.args.get("token")

    utils.log_call(player_id, "deactivate_notifications")

    data = Notifications.deactivate_notifications(token, player_id)

    return {"Notifications deactivated": data}


@app.route("/get_available_choices", methods=["GET"])
@swag_from("swagger/get_available_choices.yml")
def get_available_choices():
    """Get the available choices for a player in a given season."""
    player_id = request.args.get("player_id")

    season = request.args.get("season")

    utils.log_call(player_id, "get_available_choices")

    return Choices.get_available_choices(player_id, season)


@app.route("/get_choices", methods=["GET"])
@swag_from("swagger/get_choices.yml")
def get_choices():
    """Get the choices for a given round and season, optionally including method information."""
    round_id = request.args.get("round_id")

    season = request.args.get("season")

    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    try:
        inc_method = request.args.get("inc_method")
        inc_method = inc_method.lower() == "true"
    except (KeyError, AttributeError):
        inc_method = False

    data = Choices.get_choices(round_id, season, inc_method)

    utils.log_call(player_id, "get_choices")

    return data


@app.route("/get_fixtures", methods=["GET"])
@swag_from("swagger/get_fixtures.yml")
def get_fixtures():
    """Get the fixtures for a given round and season."""
    round_id = request.args.get("round_id")

    season = request.args.get("season")

    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    utils.log_call(player_id, "get_fixtures")

    return Fixtures.get_fixtures(round_id, season)


@app.route("/get_player_info", methods=["GET"])
@swag_from("swagger/get_player_info.yml")
def get_player_info():
    """Get player information for a given player_id and season."""
    player_id = request.args.get("player_id")

    season = request.args.get("season")

    player_info = players.get_player_info(player_id, season)

    utils.log_call(player_id, "get_player_info")

    return player_info


@app.route("/get_points", methods=["GET"])
@swag_from("swagger/get_points.yml")
def get_points():
    """Get the points for a given round and season."""
    round_id = request.args.get("round_id")

    season = request.args.get("season")

    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    points = scores.get_points(round_id, season)

    utils.log_call(player_id, "get_points")

    return points


@app.route("/get_previous_choices", methods=["GET"])
@swag_from("swagger/get_previous_choices.yml")
def get_previous_choices():
    """Get the previous choices made by a player in a given season."""
    player_id = request.args.get("player_id")

    season = request.args.get("season")

    prev_choices = Choices.get_previous_choices(player_id, season)

    utils.log_call(player_id, "get_previous_choices")

    return prev_choices


@app.route("/get_previous_points", methods=["GET"])
@swag_from("swagger/get_previous_points.yml")
def get_previous_points():
    """Get the previous points earned by a player in a given season."""
    player_id = request.args.get("player_id")

    season = request.args.get("season")

    prev_points = Choices.get_previous_points(player_id, season)

    utils.log_call(player_id, "get_previous_points")

    return prev_points


@app.route("/get_rolling_standings", methods=["GET"])
@swag_from("swagger/get_rolling_standings.yml")
def get_rolling_standings():
    """Get the rolling standings for a given season."""
    season = request.args.get("season")
    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    rolling_standings = results.get_rolling_standings(season)

    utils.log_call(player_id, "get_rolling_standings")

    return rolling_standings


@app.route("/get_round_info", methods=["GET"])
@swag_from("swagger/get_round_info.yml")
def get_round_info():
    """Get round info such as if the round is doubled, DMM, and cut-off for a round and season."""
    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    round_id = request.args.get("round_id")

    season = request.args.get("season")

    doubled, dmm, cut_off = round_api.get_round_info(round_id, season)

    utils.log_call(player_id, "get_round_info")

    return {"Round": round_id, "Double": doubled, "DMM": dmm, "Cut Off": cut_off}


@app.route("/get_round_results", methods=["GET"])
@swag_from("swagger/get_round_results.yml")
def get_round_results():
    """Get the round results for a given round and season."""
    round_id = request.args.get("round_id")
    season = request.args.get("season")

    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    round_results = results.get_round_results(round_id, season)

    utils.log_call(player_id, "get_round_results")

    return round_results


@app.route("/get_season_overview", methods=["GET"])
@swag_from("swagger/get_season_overview.yml")
def get_season_overview():
    """Get the season overview for a player in a given season."""
    player_id = request.args.get("player_id")
    season = request.args.get("season")

    season_overview = scores.get_season_overview(player_id, season)

    utils.log_call(player_id, "get_season_overview")

    return season_overview


@app.route("/get_standings", methods=["GET"])
@swag_from("swagger/get_standings.yml")
def get_standings():
    """Get the standings for a given season."""
    season = request.args.get("season")

    try:
        player_id = request.args.get("player_id")
    except (KeyError, AttributeError):
        player_id = None

    standings = results.get_standings(season)

    utils.log_call(player_id, "get_standings")

    return standings


@app.route("/get_weekly_info", methods=["GET"])
@swag_from("swagger/get_weekly_info.yml")
def get_weekly_info():
    """Get weekly information for a player, round, and season."""
    player_id = request.args.get("player_id")
    round_id = request.args.get("round_id")
    season = request.args.get("season")

    weekly_info = round_api.weekly_info(player_id, round_id, season)

    utils.log_call(player_id, "get_weekly_info")

    return weekly_info


@app.route("/get_username", methods=["GET"])
@swag_from("swagger/get_username.yml")
def get_username():
    """Get the username for a given player_id."""
    player_id = request.args.get("player_id")

    username = players.get_username(player_id)

    utils.log_call(player_id, "get_username")

    return {"Username": username}


@app.route("/init_player", methods=["GET"])
@swag_from("swagger/init_player.yml")
def init_player():
    """Initialise a player using the provided email address."""
    email = request.args.get("email")

    player_id = players.init_player(email)

    utils.log_call(int(player_id), "init_player")

    return {"player_id": int(player_id)}


# ----------------------------------------------------------------------------
# POST
# ----------------------------------------------------------------------------


@app.route("/init_notifications", methods=["POST"])
@swag_from("swagger/init_notifications.yml")
def init_notifications():
    """Initialise notifications for a player using their player_id and token."""
    request_data = request.get_json()

    player_id = request_data["player_id"]
    token = request_data["token"]

    init = Notifications.init_notifications(player_id, token)

    utils.log_call(player_id, "init_notifications")

    return {"Notifications initialised": init}


@app.route("/init_player_app", methods=["POST"])
# @swag_from('swagger/init_player_app.yml')
def init_player_app():
    """Initialise a player in the app using the provided email, username, and team."""
    request_data = request.get_json()

    email = request_data["Email"]

    try:
        username = request_data["Username"]
    except KeyError:
        username = ""

    try:
        team = request_data["Team"]
    except KeyError:
        team = ""

    player_id = players.init_player(email, username, team)

    utils.log_call(player_id, "init_player_app")

    return {"player_id": int(player_id)}


@app.route("/make_choice", methods=["POST"])
@swag_from("swagger/make_choice.yml")
def make_choice():
    """Submit a player's choice for a given round and season."""
    request_data = request.get_json()

    choice = request_data["Choice"]
    player = request_data["Player"]
    round_id = request_data["Round"]
    season = request_data["season"]

    submitted = Choices.make_choice(player, choice, round_id, season)

    utils.log_call(player, "make_choice")

    return {"Submitted": submitted}


@app.route("/update_choice", methods=["POST"])
@swag_from("swagger/update_choice.yml")
def update_choice():
    """Update a player's choice for a given round and season."""
    request_data = request.get_json()

    choice = request_data["Choice"]
    player = request_data["Player"]
    round_id = request_data["Round"]
    season = request_data["season"]

    updated = Choices.update_choice(player, choice, round_id, season)

    utils.log_call(player, "update_choice")

    return {"Updated": updated}


@app.route("/update_username", methods=["POST"])
@swag_from("swagger/update_username.yml")
def update_username():
    """Update the username for a given player_id."""
    request_data = request.get_json()

    player_id = request_data["player_id"]
    username = request_data["new_username"]

    updated = players.update_username(player_id, username)

    utils.log_call(player_id, "update_username")

    return {"Updated": updated}
