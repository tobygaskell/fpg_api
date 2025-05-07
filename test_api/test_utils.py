from unittest.mock import MagicMock, patch
import pandas as pd
from utils import run_sql_query


def test_run_sql_query_returns_dataframe():
    # Mock the connect_sql function
    with patch('utils.connect_sql') as mock_connect_sql:
        # Mock cursor and connection objects
        mock_cursor = MagicMock()
        mock_conn = MagicMock()

        # Mock description and result rows
        mock_cursor.__enter__.return_value.description = [('round_id',), ('name',)]
        mock_cursor.__enter__.return_value.__iter__.return_value = [
            (1, 'Round 1'),
            (2, 'Round 2')
        ]

        # Setup return values for connect_sql
        mock_connect_sql.return_value = (mock_cursor, mock_conn)

        # Call the function under test
        result = run_sql_query("SELECT * FROM rounds")

        # Validate result
        expected_df = pd.DataFrame([
            (1, 'Round 1'),
            (2, 'Round 2')
        ], columns=['round_id', 'name'])

        pd.testing.assert_frame_equal(result, expected_df)

        # Ensure execute was called
        mock_cursor.__enter__.return_value.execute.assert_called_once_with("SELECT * FROM rounds")
