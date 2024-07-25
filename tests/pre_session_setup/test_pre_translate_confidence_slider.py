"""
Test file for the pre-speaking session confidence slider

Test cases:
- Set-up with no changes should have expected output
- Change to confidence level should have expected change to timer settings

"""

import pytest
from streamlit.testing.v1 import AppTest
from app_components.app_setup import app_setup
from app_components.pre_session_setup import confidence_slider


@pytest.fixture
def app_setup_component():
    component = AppTest.from_function(app_setup)
    return component


@pytest.fixture
def pre_session_component():
    component = AppTest.from_function(confidence_slider)
    return component


def test_confidence_slider_default(app_setup_component, pre_session_component):

    # Run to initialise the slider
    app_setup_component.run()
    pre_session_component.session_state = app_setup_component.session_state
    pre_session_component.run()

    assert hasattr(pre_session_component.session_state, "confidence_level")

    default_slider_value = pre_session_component.slider[0].value

    assert pre_session_component.session_state.confidence_level == default_slider_value


def test_confidence_slider_change_value(app_setup_component, pre_session_component):
    """Note: asserts that the default is different to the slider max"""

    # Run to initialise the slider
    app_setup_component.run()
    pre_session_component.session_state = app_setup_component.session_state
    pre_session_component.run()

    default_slider_value = pre_session_component.slider[0].value
    slider_max_value = pre_session_component.slider[0].max

    pre_session_component.slider[0].set_value(slider_max_value)

    # Run to enact the change to slider value
    pre_session_component.run()

    run_slider_value = pre_session_component.slider[0].value

    assert run_slider_value != default_slider_value
    assert pre_session_component.session_state.confidence_level == slider_max_value
