"""
File for components on the user data viewer page
"""


def session_history():
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st
    from pathlib import Path
    import pandas as pd

    current_dir = Path(__file__).resolve().parent

    # Navigate up to the root directory
    root_dir = current_dir.parent.parent

    # Construct the path to the data.csv file
    data_file_path = root_dir / "data" / "user_data.csv"

    user_history_df = pd.read_csv(data_file_path)

    st.dataframe(user_history_df, hide_index=True)
