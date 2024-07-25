"""
File for session timer component(s)
"""


def session_timer_area() -> None:
    """
    Note: For Streamlit apps-within-functions, imports have to be within the function
    """

    import streamlit as st
    import asyncio
    import datetime
    from utils.timer_utils import stopwatch_function, format_interval
    from app_components.constants import CONFIDENCE_TIME_INTERVAL_DICT

    session_time_details = CONFIDENCE_TIME_INTERVAL_DICT[
        st.session_state["confidence_level"]
    ]

    target_time_seconds = st.slider(
        "slider",
        value=session_time_details["min"] + 30,
        min_value=session_time_details["min"],
        max_value=session_time_details["max"],
        step=30,
    )
    st.session_state["target_time_seconds"] = target_time_seconds

    timer_area = st.empty()

    if st.session_state.is_paused:
        timer_colour = "#a1b5d8"
        timer_area.markdown(
            f"""
                <p class="time" style="color:{timer_colour}">
                    {format_interval(datetime.timedelta(seconds=st.session_state.timer.seconds))}
                </p>
                """,
            unsafe_allow_html=True,
        )

    def pause_unpause_button():
        st.session_state.is_paused = not st.session_state.is_paused

    def clear_timer():
        st.session_state.timer = datetime.timedelta(minutes=0, seconds=0)

    st.button("Start/Pause", on_click=pause_unpause_button)
    st.button("Reset timer", on_click=clear_timer)

    # Put this here during TDD. Technically threshold would be met in the asyncio function but I think the functionality
    # of this session state (enabling a different function) it should only change when the thing is paused
    st.session_state.target_time_met = (
        st.session_state.timer.seconds >= target_time_seconds
    )

    if st.session_state.is_paused:
        asyncio.run(
            stopwatch_function(
                timer_area, target_time_seconds=target_time_seconds, function_on=False
            )
        )
    else:
        asyncio.run(
            stopwatch_function(timer_area, target_time_seconds=target_time_seconds)
        )
