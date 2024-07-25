"""
File for app setup function

Set-up:
- [X] `time` text styling (for timer)
- Session state
    - [X] `timer`
    - [X] `is_paused`
    - [X] `clear_timer`
    - [ ] `target_time_met`
"""


def app_setup():
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """
    import streamlit as st
    import datetime

    st.markdown(
        """
        <style>
        .time {
            font-size: 70px !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Define session state elements
    if "timer" not in st.session_state:
        st.session_state.timer = datetime.timedelta(minutes=0, seconds=0)

    if "is_paused" not in st.session_state:
        st.session_state.is_paused = True

    if "target_time_met" not in st.session_state:
        st.session_state.target_time_met = False

    if not hasattr(st.session_state, "session_min"):
        st.session_state["session_min"] = None

    if not hasattr(st.session_state, "session_max"):
        st.session_state["session_max"] = None

    if not hasattr(st.session_state, "confidence_level"):
        st.session_state["confidence_level"] = 4

    if not hasattr(st.session_state, "topic_selected"):
        st.session_state["topic_selected"] = None
