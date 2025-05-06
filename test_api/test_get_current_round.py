from api import fpg_api as app

import pytest
import sys
import os

# Add parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def client():
    # app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_current_round(client, mocker):
    # Mock the Round.get_current_round function
    mock_round = mocker.patch('app.Round.get_current_round', return_value=42)

    # Mock the utils.log_call function
    mock_log = mocker.patch('app.utils.log_call')

    response = client.get('/current_round?player_id=123')

    assert response.status_code == 200
    assert response.json == {'Round ID': 42}
    mock_round.assert_called_once()
    mock_log.assert_called_once_with('123', 'current_round')
