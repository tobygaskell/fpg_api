import pytest
import os
import sys
import pandas as pd


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fpg_api.app import app
from fpg_api.api.Choices import get_available_choices
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_available_choices(client):
    '''
    '''
    mock_player_id = "123"
    mock_choices = {
        "choices": ["Player A", "Player B"]
    }

    with patch('fpg_api.api.Choices.get_available_choices',
               return_value=mock_choices) as mock_get_choices:

        response = client.get(f'/get_available_choices?player_id={mock_player_id}')

        assert response.status_code == 200
        assert response.json == mock_choices
        mock_get_choices.assert_called_once_with(mock_player_id)


def test_get_available_choices_returns_json():
    '''
    '''
    mock_player_id = 123
    mock_df = pd.DataFrame({
        'TEAM_NAME': ['Team A', 'Team B']
    })

    expected_json = '[{"TEAM_NAME":"Team A"},{"TEAM_NAME":"Team B"}]'

    with patch('fpg_api.api.Choices.utils.run_sql_query',
               return_value=mock_df) as mock_run_sql:
        result = get_available_choices(mock_player_id)

        assert result == expected_json
        mock_run_sql.assert_called_once()
