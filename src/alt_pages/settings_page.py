"""
File for components on the user settings page
"""


def category_creation():
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st
    import pandas as pd
    from pathlib import Path

    current_dir = Path(__file__).resolve().parent

    # Navigate up to the root directory
    root_dir = current_dir.parent.parent

    # Construct the path to the data.csv file
    data_file_path = root_dir / "data" / "user_categories.csv"

    try:
        category_df = pd.read_csv(data_file_path)
    except FileNotFoundError:
        st.exception(
            "No category creations file. Please set up a CSV file called 'user_categories' in the 'data' folder."
        )
        return None

    if list(category_df.columns) != ["category"]:
        st.exception("Category creations file is incorrectly formatted.")
        return None

    st.subheader("Current categories")
    st.dataframe(category_df, hide_index=True)

    st.subheader("Add new category")
    new_category = st.text_input(label="Add new category", label_visibility="collapsed")

    def _save_category(df: pd.DataFrame, category_str: str):
        new_row = pd.DataFrame({"category": [category_str]})
        new_df = pd.concat([df, new_row], ignore_index=True)
        new_df.to_csv(data_file_path, index=False)

    save_category = st.button(
        "Save category",
        disabled=new_category == "",
        on_click=_save_category,
        kwargs={"df": category_df, "category_str": new_category},
    )
    if save_category:
        st.success("Category saved!")
