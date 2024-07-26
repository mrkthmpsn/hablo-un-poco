"""
File for the Streamlit app
"""

import streamlit as st
from streamlit_extras.badges import badge

from alt_pages.data_viewer_page import session_history
from app_components.app_setup import app_setup
from app_components.post_session_review import expectation_comparison_slider, data_save
from app_components.pre_session_setup import (
    confidence_slider,
    topic_selection_selectbox,
)
from app_components.reusable import translation_area
from app_components.session_timer import session_timer_area
from alt_pages.settings_page import category_creation

st.header("hablo un poco")

# TODO[*] Language selection could happen here
st.subheader("actually practice some Spanish")

# Set-up

app_setup()

# Set-up
with st.sidebar:
    badge(type="github", name="mrkthmpsn/hablo-un-poco")
    badge(type="twitter", name="tweetsbymarkt")


def page1():
    confidence_slider()

    topic_selection_selectbox()

    # Pre-chat translation
    translation_area(area_type="pre")

    st.divider()

    # Speaking session
    st.write("Choose the length of this practice, and then start the timer and go!")
    session_timer_area()

    st.divider()

    # Post-session
    with st.expander("After the session...", expanded=st.session_state.target_time_met):
        expectation_comparison_slider()

        translation_area(area_type="post")

        data_save()


def page2():
    st.write(
        "Testing a second page and what better way than with a good old lorem ipsum"
    )
    category_creation()


def page3():
    st.write("Here are all the things you've done so far")
    session_history()


pg = st.navigation(
    [
        st.Page(page1, title="App"),
        st.Page(page2, title="Settings"),
        st.Page(page3, title="Practice history"),
    ]
)
pg.run()
