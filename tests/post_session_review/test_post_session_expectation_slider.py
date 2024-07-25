"""
Test file for the post-speaking session 'how did this go vs expectation' slider

Requirements:
- Should only appear once chosen time threshold has been met
- Should be in expander section?

Test cases:
- [X] Should be disabled on initial set-up
- [X] When enabled, should have 1 slider element in component slider list
"""

import pytest
from streamlit.testing.v1 import AppTest
from app_components.app_setup import app_setup
from app_components.post_session_review import expectation_comparison_slider


@pytest.fixture
def app_setup_component():
    component = AppTest.from_function(app_setup)
    return component


@pytest.fixture
def post_session_component():
    component = AppTest.from_function(expectation_comparison_slider)
    return component


def test_comparison_slider_disabled_status(app_setup_component, post_session_component):

    # Run to initialise the slider
    app_setup_component.run()
    post_session_component.session_state = app_setup_component.session_state
    post_session_component.run()

    assert len(post_session_component.slider) == 1
    assert post_session_component.slider[0].disabled


def test_comparison_slider_active_status_change(
    app_setup_component, post_session_component
):

    # Run to initialise the slider
    app_setup_component.run()
    post_session_component.session_state = app_setup_component.session_state
    post_session_component.run()

    post_session_component.session_state["target_time_met"] = True

    # Run to enact the change to the 'target time met' session state
    post_session_component.run()

    assert not post_session_component.slider[0].disabled
