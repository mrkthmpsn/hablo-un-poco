"""
File for reusable components in multiple sections of the app
"""


def translation_area(area_type: str):
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function

    :param area_type: "pre" or "post", to designate whether the component is being used before or after the translation
        session.
    """

    import streamlit as st
    from utils.translate_utils import translate_text

    if not hasattr(st.session_state, f"{area_type}_session_translation_area_string"):
        st.session_state[f"{area_type}_session_translation_area_string"] = ""
    if not hasattr(st.session_state, f"{area_type}_session_translation_list"):
        st.session_state[f"{area_type}_session_translation_list"] = []

    if area_type == "pre":
        message_string = (
            "Write down any words that you want translated before practicing"
        )
    else:
        message_string = "Translate any words you couldn't remember during the practice"

    translation_requests = st.text_area(
        f"{message_string} - translated using Google Translate's API"
    )
    if (
        translation_requests
        != st.session_state[f"{area_type}_session_translation_area_string"]
    ):
        st.session_state[f"{area_type}_session_translation_area_string"] = (
            translation_requests
        )

        translation_list = translation_requests.split("\n")
        translated_list = []
        # Should write some checks for things like non-text appearing, like emojis, and line breaks etc
        for translation_request in translation_list:
            pre_chat_translation_output = translate_text(
                translation_request, target_language_code="es"
            )

            full_translation_output = (
                f"{translation_request} - {pre_chat_translation_output.translated_text}"
            )
            translated_list.append(full_translation_output)

        st.session_state[f"{area_type}_session_translation_list"] = translated_list

    if len(st.session_state[f"{area_type}_session_translation_list"]) > 0:
        st.text("\n".join(st.session_state[f"{area_type}_session_translation_list"]))
