"""
File for utils relating to the stopwatch timer
"""

import asyncio
import datetime

import streamlit as st


def format_time_seconds(interval_seconds):
    minutes, seconds = divmod(interval_seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def format_interval(interval):
    total_seconds = int(interval.total_seconds())
    return format_time_seconds(total_seconds)


async def stopwatch_function(test, target_time_seconds: int, function_on: bool = True):
    while function_on:
        state_timer = datetime.timedelta(seconds=st.session_state.timer.seconds)
        timer_colour = (
            "#E34A6F" if state_timer.seconds < target_time_seconds else "#36BFAA"
        )
        test.markdown(
            f"""
            <p class="time" style="color:{timer_colour}">
                {format_interval(state_timer)}
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.session_state.timer = state_timer + datetime.timedelta(seconds=1)
        r = await asyncio.sleep(1, result=None)
