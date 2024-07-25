"""
Test file for the pre-speaking session set-up of the topic selection component

Test cases:
- [X] Default is None & fetches categories from df
- [X] Change causes a change in the session state value & an st.write-produced markdown element
"""

from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd

from app_components.app_setup import app_setup
from app_components.pre_session_setup import topic_selection_selectbox


@pytest.fixture
def app_setup_component():
    component = AppTest.from_function(app_setup)
    return component


@pytest.fixture
def pre_session_component():
    component = AppTest.from_function(topic_selection_selectbox)
    return component


@pytest.fixture
def mock_category_df():
    return pd.DataFrame({"category": ["Football", "TV", "Current Events"]})


@patch("pandas.read_csv")
def test_topic_selection_default(
    mock_read_csv, app_setup_component, pre_session_component, mock_category_df
):
    mock_read_csv.return_value = mock_category_df

    # Run to initialise the component
    app_setup_component.run()
    pre_session_component.session_state = app_setup_component.session_state
    pre_session_component.run()

    assert not pre_session_component.exception
    mock_read_csv.assert_called_once()
    assert hasattr(pre_session_component.session_state, "topic_selected")
    assert pre_session_component.session_state.topic_selected is None
    assert len(pre_session_component.markdown) == 0


@patch("pandas.read_csv")
def test_topic_selection_change_value(
    mock_read_csv, app_setup_component, pre_session_component, mock_category_df
):
    mock_read_csv.return_value = mock_category_df
    selected_category = mock_category_df["category"][1]

    # Run to initialise the component
    app_setup_component.run()
    pre_session_component.session_state = app_setup_component.session_state
    pre_session_component.run()

    pre_session_component.selectbox[0].select(selected_category)

    # Run to enact the change to component value
    pre_session_component.run()

    assert pre_session_component.session_state.topic_selected == selected_category
    assert len(pre_session_component.markdown) == 1
