"""
Test file for data-saving functionality after a speaking session

Test cases:
- [X] Option disabled prior to a completed speaking session
- [X] Has data required to save
- [X] Raises error if save attempted but no file to save to
What's the appropriate way of testing that the data saves?
"""

import datetime
from unittest.mock import patch, mock_open

import pandas as pd
import pytest
import streamlit.testing.v1.element_tree
from streamlit.testing.v1 import AppTest
from streamlit.testing.v1.element_tree import ElementList

from app_components.app_setup import app_setup
from app_components.post_session_review import data_save, expectation_comparison_slider
from app_components.pre_session_setup import (
    confidence_slider,
    topic_selection_selectbox,
)
from app_components.session_timer import session_timer_area


@pytest.fixture
def app_setup_component():
    component = AppTest.from_function(app_setup)
    return component


@pytest.fixture
def confidence_slider_component():
    component = AppTest.from_function(confidence_slider)
    return component


@pytest.fixture
def topic_selection_component():
    component = AppTest.from_function(topic_selection_selectbox)
    return component


@pytest.fixture
def session_timer_component():
    component = AppTest.from_function(session_timer_area)
    return component


@pytest.fixture
def expectation_comparison_component():
    component = AppTest.from_function(expectation_comparison_slider)
    return component


@pytest.fixture
def post_session_component():
    component = AppTest.from_function(data_save)

    return component


def test_data_save_disabled(app_setup_component, post_session_component):
    # Run to initialise the component
    app_setup_component.run()
    post_session_component.session_state = app_setup_component.session_state
    post_session_component.run()

    assert len(post_session_component.button) == 1
    assert post_session_component.button[0].disabled


@patch("pandas.read_csv")
def test_data_save_data_availability(
    mock_read_csv,
    app_setup_component,
    confidence_slider_component,
    topic_selection_component,
    session_timer_component,
    expectation_comparison_component,
    post_session_component,
):
    mock_read_csv.side_effect = [
        # Mock for initialising run of topic selection
        pd.DataFrame({"category": ["Football", "TV", "Current Events"]}),
        # Mock for 2nd run of topic selection
        pd.DataFrame({"category": ["Football", "TV", "Current Events"]}),
    ]

    # Run to initialise the component
    # TODO[***] This seems like a bad way of doing this testing
    app_setup_component.run()
    confidence_slider_component.session_state = app_setup_component.session_state
    confidence_slider_component.run()
    topic_selection_component.session_state = confidence_slider_component.session_state
    topic_selection_component.run()
    topic_selection_component.selectbox[0].select("Football")
    topic_selection_component.run()
    session_timer_component.session_state = topic_selection_component.session_state
    session_timer_component.run()
    expectation_comparison_component.session_state = (
        session_timer_component.session_state
    )
    expectation_comparison_component.run()
    post_session_component.session_state = (
        expectation_comparison_component.session_state
    )
    post_session_component.run()

    # What data do I want
    assert hasattr(post_session_component.session_state, "topic_selected")
    assert hasattr(post_session_component.session_state, "confidence_level")
    assert hasattr(post_session_component.session_state, "target_time_seconds")
    assert hasattr(post_session_component.session_state, "expectation_comparison")

    assert not post_session_component.exception


@patch("pandas.read_csv")
def test_data_save_no_file_error(
    mock_read_csv,
    app_setup_component,
    confidence_slider_component,
    topic_selection_component,
    session_timer_component,
    expectation_comparison_component,
    post_session_component,
):

    mock_read_csv.side_effect = [
        # Mock for initialising run of topic selection
        pd.DataFrame({"category": ["Football", "TV", "Current Events"]}),
        # Mock for 2nd run of topic selection
        pd.DataFrame({"category": ["Football", "TV", "Current Events"]}),
        # Mock for behaviour of no data saving file
        FileNotFoundError,
    ]

    app_setup_component.run()
    confidence_slider_component.session_state = app_setup_component.session_state
    confidence_slider_component.run()
    topic_selection_component.session_state = confidence_slider_component.session_state
    topic_selection_component.run()
    topic_selection_component.selectbox[0].select("Football")
    topic_selection_component.run()
    session_timer_component.session_state = topic_selection_component.session_state
    session_timer_component.run()
    expectation_comparison_component.session_state = (
        session_timer_component.session_state
    )
    expectation_comparison_component.run()
    post_session_component.session_state = (
        expectation_comparison_component.session_state
    )
    post_session_component.run()

    post_session_component.button[0].click()

    post_session_component.run()

    assert post_session_component.exception
    assert (
        post_session_component.exception[0].message
        == "No data file to save to. Please set up a CSV file called 'user_data' in the 'data' folder."
    )

    # Button should be disabled again
    assert post_session_component.button[0].disabled


@patch("pandas.read_csv")
# Mock to allow us to use `to_csv` and check that it's been called
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.DataFrame.to_csv")
@patch("datetime.date")
def test_data_save_success(
    mock_date,
    mock_to_csv,
    mock_open,
    mock_read_csv,
    app_setup_component,
    confidence_slider_component,
    topic_selection_component,
    session_timer_component,
    expectation_comparison_component,
    post_session_component,
):
    app_setup_component.run()
    confidence_slider_component.session_state = app_setup_component.session_state
    confidence_slider_component.run()
    topic_selection_component.session_state = confidence_slider_component.session_state
    topic_selection_component.run()
    topic_selection_component.selectbox[0].select("Football")
    topic_selection_component.run()
    session_timer_component.session_state = topic_selection_component.session_state
    session_timer_component.run()
    expectation_comparison_component.session_state = (
        session_timer_component.session_state
    )
    expectation_comparison_component.run()
    post_session_component.session_state = (
        expectation_comparison_component.session_state
    )
    post_session_component.run()

    post_session_component.session_state.target_time_met = True

    mock_read_csv.return_value = pd.DataFrame(
        {
            "practice_date": ["2024-01-01", "2024-01-02"],
            "topic_selected": ["Football", "TV"],
            "confidence_level": [4, 3],
            "target_time_seconds": [120, 90],
            "expectation_comparison": [4, 4],
        }
    )

    mock_date.today.return_value = datetime.date(year=2024, month=1, day=3)
    post_session_component.session_state.topic_selected = "Football"
    post_session_component.session_state.confidence_level = 2
    post_session_component.session_state.target_time_seconds = 90
    post_session_component.session_state.expectation_comparison = 3

    post_session_component.button[0].click()

    post_session_component.run()

    # Assertions

    # Check that the to_csv method was called once
    mock_to_csv.assert_called_once()

    assert not post_session_component.exception
    assert len(post_session_component.success) == 1
