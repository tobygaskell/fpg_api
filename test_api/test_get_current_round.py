import pytest
import os
import sys
import pandas as pd


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fpg_api.app import app
from fpg_api.api.Round import get_current_round
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_current_round_without_player_id(client):
    with patch('fpg_api.api.Round.get_current_round', return_value=42):
        response = client.get('/current_round')
        assert response.status_code == 200
        assert response.json == {'Round ID': 42}


def test_get_current_round_with_player_id(client):
    with patch('fpg_api.api.Round.get_current_round', return_value=99):
        response = client.get('/current_round?player_id=123')
        assert response.status_code == 200
        assert response.json == {'Round ID': 99}


def test_get_current_round():
    # Mock the SQL query result
    with patch('fpg_api.api.Round.utils.run_sql_query') as mock_run_sql:
        mock_run_sql.return_value = pd.DataFrame({'current_round': [27]})
        result = get_current_round()
        assert result == 27
