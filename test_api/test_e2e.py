"""Intergration Tests for fpg api."""

import os

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL = os.getenv("BASE_URL")

acceptable_status_code = 200
timeout = 30

def test_rules():
    """Test Rules."""
    r = requests.get(f"{BASE_URL}/rules", timeout=timeout)
    assert r.status_code == acceptable_status_code

def test_api():
    """Test Api."""
    r = requests.get(f"{BASE_URL}/api", timeout=timeout)
    assert r.status_code == acceptable_status_code

def test_index():
    """Test Index."""
    r = requests.get(f"{BASE_URL}/", timeout=timeout)
    assert r.status_code == acceptable_status_code

def test_get_current_round():
    """Test get current round."""
    r = requests.get(f"{BASE_URL}/current_round?player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = {'Round ID', 'season'}

    assert expected_keys.issubset(data.keys()), f"Response keys missing. Got keys: {data.keys()}"
    assert isinstance(data['Round ID'], int), f"Round ID is not int: {data['Round ID']}"
    assert isinstance(data['season'], int), f"season is not int: {data['season']}"


def test_get_available_choices():
    """Test get available choices."""
    r = requests.get(f"{BASE_URL}/get_available_choices?player_id=6&season=2025", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_length = 1
    expected_keys = {'TEAM_NAME'}

    assert len(data) >= expected_length
    assert isinstance(data, list), "Available choices is not an array"
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_choices_inc_method():
    """Test get choices inc method."""
    r = requests.get(f"{BASE_URL}/get_choices?round_id=10&season=2024&inc_method=true",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = {'Choice', 'Method'}
    expected_length = 1

    assert len(data) >= expected_length
    assert isinstance(data['6'], dict)
    assert isinstance(data, dict)
    assert expected_keys.issubset(data['6'].keys())


def test_get_choices_not_inc_method():
    """Test get choices not inc method."""
    r = requests.get(f"{BASE_URL}/get_choices?round_id=10&season=2024&inc_method=false",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_length = 1

    assert len(data) >= expected_length
    assert isinstance(data, dict)
    assert isinstance(data['6'], str)


def test_get_fixtures():
    """Test get fixtures."""
    r = requests.get(f"{BASE_URL}/get_fixtures?round_id=10&season=2024&player_id=6",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()
    expected_length = 10
    expected_keys = { "AWAY_LOGO", "AWAY_TEAM", "DERBY", "FIXTURE_ID", "HOME_LOGO",
                      "HOME_TEAM", "KICKOFF", "LOCATION", "ROUND", "SEASON" }

    assert len(data) == expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_player_info():
    """Test get player info."""
    r = requests.get(f"{BASE_URL}/get_player_info?season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "draw_cnt", "lose_cnt", "round_cnt", "total_points", "win_cnt" }
    expected_length = 1

    assert len(data) == expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_points():
    """Test get points."""
    r = requests.get(f"{BASE_URL}/get_points?round_id=10&season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = {"Basic", "Choice", "Derby", "Draw Means More", "Head 2 Head",
                     "Result", "Subtotal", "Total", "User", "player_id"}
    expected_length = 1

    assert len(data) >= expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_previous_choices():
    """Test get previous choies."""
    r = requests.get(f"{BASE_URL}/get_previous_choices?season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = {"1st Pick", "2nd Pick", "Choice"}
    expected_length = 20

    assert len(data) == expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_previous_points():
    """Test get previous points."""
    r = requests.get(f"{BASE_URL}/get_previous_points?season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = {"1st Pick", "2nd Pick", "Choice"}
    expected_length = 20

    assert len(data) == expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_rolling_standings():
    """Test get rolling standings."""
    r = requests.get(f"{BASE_URL}/get_rolling_standings?season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "Goal Diff", "Position", "Score", "User", "player_id", "round" }
    expected_length = 1

    assert len(data) >= expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_round_info():
    """Test get round info."""
    r = requests.get(f"{BASE_URL}/get_round_info?round_id=10&season=2024&player_id=6",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "Cut Off", "DMM", "Double", "Round" }
    expected_length = 4

    assert len(data) == expected_length
    assert isinstance(data, dict)
    assert expected_keys.issubset(data.keys())


def test_get_round_results():
    """Test get round results."""
    r = requests.get(f"{BASE_URL}/get_round_results?round_id=10&season=2024&player_id=6",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "AWAY_GOALS", "FIXTURE_ID", "GAME_STATUS",
                      "HOME_GOALS", "ROUND", "SCORE", "WINNER" }
    expected_length = 10

    assert len(data) == expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())


def test_get_season_overview():
    """Test get season overview."""
    r = requests.get(f"{BASE_URL}/get_season_overview?season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "player_id", "POINTS", "RESULT", "round" }
    expected_length = 1

    assert len(data) >= expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())

def test_get_standings():
    """Test get standings."""
    r = requests.get(f"{BASE_URL}/get_standings?season=2024&player_id=6", timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "Goal Diff", "Position", "Score", "User", "movement_indicator", "player_id" }
    expected_length = 1

    assert len(data) >= expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())

def test_get_username():
    """Test get username."""
    r = requests.get(f"{BASE_URL}/get_username?player_id=6",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "Username" }
    expected_length = 1

    assert len(data) == expected_length
    assert isinstance(data, dict)
    assert expected_keys.issubset(data.keys())

def test_get_weekly_info():
    """Test get weekly info."""
    r = requests.get(f"{BASE_URL}/get_weekly_info?round_id=10&season=2024&player_id=6",
                     timeout=timeout)
    assert r.status_code == acceptable_status_code, f"Unexpected status code: {r.status_code}"

    data = r.json()

    expected_keys = { "away_goals", "away_team", "basic", "derby", "dmm", "Doubled",
                      "head_to_head", "home_goals", "home_team", "lonely_points", "pick",
                      "player_id", "round", "total", "subtotal", "running_total", 'docked_points'}
    expected_length = 1

    assert len(data) == expected_length
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert expected_keys.issubset(data[0].keys())
