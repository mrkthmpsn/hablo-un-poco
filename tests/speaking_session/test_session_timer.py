"""
Test file for the session timer feature

Test cases:
- [X] Slider min and max values based on session state
- Test that there's actually a timer??
- Pause button changes pause session state
- [X] Test that meeting the timer value sets the `target_time_met` session state
- [X] Test that the reset button resets the `target_time_met` session state

"""

import datetime

import pytest
from streamlit.testing.v1 import AppTest

from app_components.app_setup import app_setup
from app_components.constants import CONFIDENCE_TIME_INTERVAL_DICT
from app_components.pre_session_setup import confidence_slider
from app_components.session_timer import session_timer_area


@pytest.fixture
def session_timer_component():
    component = AppTest.from_function(session_timer_area)
    return component


# Using this to get the session state 'is_paused' which is set-up here - not sure this is best way of testing
@pytest.fixture
def app_setup_component():
    component = AppTest.from_function(app_setup)
    return component


# Using this to set the `session_min` and `session_max` session states easily with a run of the component
@pytest.fixture
def confidence_slider_component():
    component = AppTest.from_function(confidence_slider)
    return component


def test_session_timer_slider_values(session_timer_component):

    # Run to initialise the components
    session_timer_component.run()

    session_timer_component.session_state["confidence_level"] = 5

    # Run to enact the change in session state
    session_timer_component.run()

    assert (
        session_timer_component.slider[0].value
        == CONFIDENCE_TIME_INTERVAL_DICT[5]["min"] + 30
    )
    assert (
        session_timer_component.slider[0].min == CONFIDENCE_TIME_INTERVAL_DICT[5]["min"]
    )
    assert (
        session_timer_component.slider[0].max == CONFIDENCE_TIME_INTERVAL_DICT[5]["max"]
    )


def test_session_timer_timer_setup(app_setup_component, session_timer_component):

    # TODO[**] I don't think this is a good test

    # Run to initialise the components
    app_setup_component.run()
    session_timer_component.run()

    session_timer_component.session_state["is_paused"] = (
        app_setup_component.session_state.is_paused
    )
    session_timer_component.session_state["timer"] = (
        app_setup_component.session_state.timer
    )

    session_timer_component.session_state["confidence_level"] = 4

    # Run to enact changes to session state in this component
    session_timer_component.run()

    assert len(session_timer_component.markdown) == 1
    assert session_timer_component.session_state.is_paused
    assert len(session_timer_component.button) == 2


def test_session_timer_reaching_target_time(
    app_setup_component, confidence_slider_component, session_timer_component
):

    # TODO[***] This is too cumbersome, needing to run both components to get the right session state
    # Run to initialise the components
    app_setup_component.run()
    confidence_slider_component.session_state = app_setup_component.session_state
    confidence_slider_component.run()

    session_timer_component.session_state = confidence_slider_component.session_state

    session_timer_component.run()

    # Change values
    target_time_seconds = 60
    session_timer_component.slider[0].set_value(target_time_seconds)

    session_timer_component.session_state.timer = datetime.timedelta(
        minutes=0, seconds=58
    )

    # Run to enact the change to the slider and session timer
    session_timer_component.run()

    assert session_timer_component.session_state.target_time_met is False

    session_timer_component.session_state.timer = datetime.timedelta(
        minutes=1, seconds=3
    )

    # Run to enact the change to session timer
    session_timer_component.run()

    assert session_timer_component.session_state.target_time_met is True


def test_session_timer_reset_button(
    app_setup_component, confidence_slider_component, session_timer_component
):

    # TODO[***] This is too cumbersome, needing to run both components to get the right session state
    # Run to initialise the components
    app_setup_component.run()
    confidence_slider_component.session_state = app_setup_component.session_state
    confidence_slider_component.run()

    session_timer_component.session_state = confidence_slider_component.session_state

    session_timer_component.run()

    session_timer_component.session_state.timer = datetime.timedelta(
        minutes=0, seconds=58
    )
    # Run to enact the change to the session timer value
    session_timer_component.run()

    session_timer_component.button[1].click()
    session_timer_component.run()

    assert isinstance(session_timer_component.session_state.timer, datetime.timedelta)
    assert session_timer_component.session_state.timer.seconds == 0
