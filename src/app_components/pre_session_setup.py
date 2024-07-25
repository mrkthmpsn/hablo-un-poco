"""
File for pre-session set-up components
"""


def confidence_slider() -> None:
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st
    from utils.state_utils import load_session_value, store_session_value

    load_session_value(key_base="confidence_level")
    st.slider(
        "What's your confidence level about this practice?",
        min_value=1,
        max_value=7,
        step=1,
        key="_confidence_level",
        on_change=store_session_value,
        kwargs={"key_base": "confidence_level"},
    )


def topic_selection_selectbox() -> None:
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st
    from pathlib import Path
    import pandas as pd
    from utils.state_utils import load_session_value, store_session_value

    current_dir = Path(__file__).resolve().parent

    # Navigate up to the root directory
    root_dir = current_dir.parent.parent

    # Construct the path to the data.csv file
    data_file_path = root_dir / "data" / "user_categories.csv"

    category_df = pd.read_csv(data_file_path)

    load_session_value(key_base="topic_selected")

    topic_selection = st.selectbox(
        "Topic selection box",
        category_df["category"],
        index=(
            list(category_df["category"]).index(st.session_state["_topic_selected"])
            if st.session_state["_topic_selected"] is not None
            else None
        ),
        placeholder="Choose a topic...",
        label_visibility="collapsed",
        key="_topic_selected",
        on_change=store_session_value,
        kwargs={"key_base": "topic_selected"},
    )

    if topic_selection is not None:
        st.write(f"Let's talk about **{topic_selection}**")
