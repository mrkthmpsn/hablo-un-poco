"""
Test file for app set-up

Test cases:
- [X] All session state variables have been set up
    - Do I want to add `clear_timer` too, despite it being set-up differently in-code atm?
"""

import pytest
from streamlit.testing.v1 import AppTest

from app_components.app_setup import app_setup


@pytest.fixture
def app_setup_component():
    component = AppTest.from_function(app_setup)
    return component


def test_app_setup(app_setup_component):

    app_setup_component.run()

    assert hasattr(app_setup_component.session_state, "timer")
    assert hasattr(app_setup_component.session_state, "is_paused")
    assert hasattr(app_setup_component.session_state, "target_time_met")
    assert hasattr(app_setup_component.session_state, "session_min")
    assert hasattr(app_setup_component.session_state, "session_max")
    assert hasattr(app_setup_component.session_state, "confidence_level")
    assert hasattr(app_setup_component.session_state, "topic_selected")
