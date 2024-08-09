"""
Test file for the pre-speaking session translation area

Test cases:
- [X] No text selected results in no text rendered
- [X] Rendering the output properly
- [X] Text splits by line-breaks into a list
- [X] Only translate once
- [X] Deals with the appropriate type of session state
- [X] Ignores/strips empty lines
- Dealing with emojis?
"""

from unittest.mock import patch, MagicMock

import pytest
from google.cloud import translate
from streamlit.testing.v1 import AppTest

from app_components.reusable import translation_area


@pytest.fixture
def translation_area_component():
    component = AppTest.from_function(translation_area, kwargs={"area_type": "pre"})
    return component


def test_pre_session_translation_area_no_text(translation_area_component):

    translation_area_component.run()

    assert hasattr(
        translation_area_component.session_state, "pre_session_translation_list"
    )
    assert hasattr(
        translation_area_component.session_state, "pre_session_translation_area_string"
    )
    assert (
        translation_area_component.session_state.pre_session_translation_area_string
        == ""
    )
    assert isinstance(
        translation_area_component.session_state.pre_session_translation_list, list
    )
    assert len(translation_area_component.text) == 0


@patch("utils.translate_utils.translate_text")
def test_pre_session_translation_area_single_phrase(
    mock_translate_text, translation_area_component
):

    # Run to initialise the slider
    translation_area_component.run()

    translation_area_component.text_area[0].set_value("dog")

    mock_translation = MagicMock(spec=translate.Translation)
    mock_translation.translated_text = "perro"
    mock_translate_text.return_value = mock_translation

    # Run to enact the change to text area value
    translation_area_component.run()

    assert isinstance(
        translation_area_component.session_state.pre_session_translation_list, list
    )
    assert translation_area_component.session_state.pre_session_translation_list == [
        "dog - perro"
    ]
    assert len(translation_area_component.text) == 1
    assert translation_area_component.text[0].value == "dog - perro"


@patch("utils.translate_utils.translate_text")
def test_pre_session_translation_area_multiple_phrases_with_line_break(
    mock_translate_text, translation_area_component
):

    # Run to initialise the slider
    translation_area_component.run()

    translation_area_component.text_area[0].set_value("the dog\nthe cat")

    mock_translations_list = []
    for translation in ["el perro", "el gato"]:
        mock_translation = MagicMock(spec=translate.Translation)
        mock_translation.translated_text = translation
        mock_translations_list.append(mock_translation)

    mock_translate_text.side_effect = mock_translations_list

    # Run to enact the change to text area value
    translation_area_component.run()

    assert isinstance(
        translation_area_component.session_state.pre_session_translation_list, list
    )
    assert (
        len(translation_area_component.session_state.pre_session_translation_list) == 2
    )
    assert (
        translation_area_component.session_state.pre_session_translation_list[0]
        == "the dog - el perro"
    )
    assert (
        translation_area_component.session_state.pre_session_translation_list[1]
        == "the cat - el gato"
    )
    assert len(translation_area_component.text) == 1
    assert (
        translation_area_component.text[0].value
        == "the dog - el perro\nthe cat - el gato"
    )


@patch("utils.translate_utils.translate_text")
def test_pre_session_translation_area_only_translate_on_change(
    mock_translate_text, translation_area_component
):
    # Run to initialise the slider
    translation_area_component.run()

    translation_area_component.text_area[0].set_value("dog")

    mock_translation = MagicMock(spec=translate.Translation)
    mock_translation.translated_text = "perro"
    mock_translate_text.return_value = mock_translation

    # Run to enact the change to text area value
    translation_area_component.run()

    assert (
        translation_area_component.session_state.pre_session_translation_area_string
        == "dog"
    )

    # Run to test an imagined change in another component
    translation_area_component.run()

    # TODO[**] I'm not really sure this is testing what I want - I _really_ want to test it's not running the
    #  translations twice
    assert (
        translation_area_component.session_state.pre_session_translation_area_string
        == "dog"
    )


# We don't use the fixture here because we want to test the args functionality
def test_translation_area_appropriate_session_state():
    # Run to initialise the translation area
    translation_area_component = AppTest.from_function(
        translation_area, kwargs={"area_type": "post"}
    )
    translation_area_component.run()

    assert hasattr(
        translation_area_component.session_state, "post_session_translation_area_string"
    )
    assert hasattr(
        translation_area_component.session_state, "post_session_translation_list"
    )


@patch("utils.translate_utils.translate_text")
def test_translation_area_ignore_empty_line(
    mock_translate_text, translation_area_component
):
    # Run to initialise the slider
    translation_area_component.run()

    translation_area_component.text_area[0].set_value("dog\n ")

    mock_translation = MagicMock(spec=translate.Translation)
    mock_translation.translated_text = "perro"
    mock_translate_text.return_value = mock_translation

    # Run to enact the change to text area value
    translation_area_component.run()

    assert (
        len(translation_area_component.session_state.pre_session_translation_list) == 1
    )
    assert (
        translation_area_component.session_state.pre_session_translation_area_string
        == "dog"
    )
    assert (
        translation_area_component.session_state.pre_session_translation_list[0]
        == "dog - perro"
    )
