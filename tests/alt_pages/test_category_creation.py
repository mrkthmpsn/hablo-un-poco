"""
Test file for category creation component

Test cases:
- [X] Raises error if no categories file
- [X] Raises error if file wrongly formatted
- [ ] Sets session state with working file [?]
- [ ] Creates new category
"""

from unittest.mock import patch, mock_open

import pytest
from streamlit.testing.v1 import AppTest

from alt_pages.settings_page import category_creation
import pandas as pd


@pytest.fixture
def category_creation_component():
    component = AppTest.from_function(category_creation)
    return component


@patch("pandas.read_csv")
def test_category_creation_no_file_error(mock_read_csv, category_creation_component):

    mock_read_csv.side_effect = FileNotFoundError

    # Run to initialise the component
    category_creation_component.run()

    assert category_creation_component.exception
    assert len(category_creation_component.exception) == 1
    assert (
        category_creation_component.exception[0].message
        == "No category creations file. Please set up a CSV file called 'user_categories' in the 'data' folder."
    )


@patch("pandas.read_csv")
def test_category_creation_invalid_file_format(
    mock_read_csv, category_creation_component
):

    mock_read_csv.return_value = pd.DataFrame()

    # Run to initialise the component
    category_creation_component.run()

    assert category_creation_component.exception
    assert len(category_creation_component.exception) == 1
    assert (
        category_creation_component.exception[0].message
        == "Category creations file is incorrectly formatted."
    )


@patch("pandas.read_csv")
def test_category_creation_loads(mock_read_csv, category_creation_component):
    mock_read_csv.return_value = pd.DataFrame({"category": ["Football", "TV"]})

    # Run to initialise the component
    category_creation_component.run()

    assert not category_creation_component.exception
    assert len(category_creation_component.text_input) == 1
    assert len(category_creation_component.dataframe) == 1
    assert len(category_creation_component.button) == 1
    # Assert 'save category' button is disabled as there's no input
    assert category_creation_component.button[0].disabled


@patch("pandas.read_csv")
# Mock to allow us to use `to_csv` and check that it's been called
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.DataFrame.to_csv")
def test_category_creation_successful_creation(
    mock_to_csv, mock_open, mock_read_csv, category_creation_component
):

    mock_read_csv.side_effect = [
        # Initial set-up
        pd.DataFrame({"category": ["Football", "TV"]}),
        # After the click event
        pd.DataFrame({"category": ["Football", "TV"]}),
        # Subsequent run after adding category
        pd.DataFrame({"category": ["Football", "TV", "Current Events"]}),
    ]

    # Run to initialise the component
    category_creation_component.run()

    category_creation_component.text_input[0].set_value("Current Events")
    category_creation_component.button[0].click()

    category_creation_component.run()

    # Check that the to_csv method was called once
    mock_to_csv.assert_called_once()

    assert not category_creation_component.exception

    category_creation_component.run()

    assert not category_creation_component.exception
    pd.testing.assert_frame_equal(
        category_creation_component.dataframe[0].value,
        pd.DataFrame({"category": ["Football", "TV", "Current Events"]}),
    )
