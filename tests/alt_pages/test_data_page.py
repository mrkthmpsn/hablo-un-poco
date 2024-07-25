"""
Test file for the page to view the user's data

Test cases:
- [ ] Renders properly
"""

from unittest.mock import patch
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from alt_pages.data_viewer_page import session_history


@pytest.fixture
def data_viewer_component():
    component = AppTest.from_function(session_history)
    return component


@patch("pandas.read_csv")
def test_data_viewer_success(mock_read_csv, data_viewer_component):
    mock_read_csv.return_value = pd.DataFrame(
        {
            "practice_date": ["2024-07-24", "2024-07-25"],
            "topic_selected": ["TV programme", "Football"],
            "confidence_level": [2, 3],
            "target_time_seconds": [60, 120],
            "expectation_comparison": [4, 2],
        }
    )

    data_viewer_component.run()

    assert not data_viewer_component.exception
    assert len(data_viewer_component.dataframe) == 1
