"""
File with utils for dealing with the session state
"""

import streamlit as st


def store_session_value(key_base: str):
    st.session_state[key_base] = st.session_state["_" + key_base]


def load_session_value(key_base: str):
    st.session_state["_" + key_base] = st.session_state[key_base]
