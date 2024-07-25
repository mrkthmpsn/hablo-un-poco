"""
File for post-session review components
"""


def expectation_comparison_slider():
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st

    st.session_state["expectation_comparison"] = st.slider(
        label="How did that go?",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        disabled=not st.session_state.target_time_met,
    )


def data_save():
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st
    import pandas as pd
    import datetime
    from pathlib import Path

    if not hasattr(st.session_state, "save_error"):
        st.session_state.save_error = False

    def _save_session_data() -> None:
        try:
            current_dir = Path(__file__).resolve().parent

            # Navigate up to the root directory
            root_dir = current_dir.parent.parent

            # Construct the path to the data.csv file
            data_file_path = root_dir / "data" / "user_data.csv"
            df = pd.read_csv(data_file_path)
        except FileNotFoundError:
            st.session_state.save_error = True
            return None

        session_df = pd.DataFrame(
            {
                "practice_date": [datetime.date.today().strftime("%Y-%m-%d")],
                "topic_selected": [st.session_state.topic_selected],
                "confidence_level": [st.session_state.confidence_level],
                "target_time_seconds": [st.session_state.target_time_seconds],
                "expectation_comparison": [st.session_state.expectation_comparison],
            }
        )

        new_df = pd.concat([df, session_df])

        new_df.to_csv(data_file_path, index=False)

    save_button = st.button(
        "Save the session data",
        disabled=not st.session_state.target_time_met or st.session_state.save_error,
        on_click=_save_session_data,
    )

    if st.session_state.save_error:
        st.exception(
            "No data file to save to. Please set up a CSV file called 'user_data' in the 'data' folder."
        )
    if save_button:
        st.success("Session data saved!")
