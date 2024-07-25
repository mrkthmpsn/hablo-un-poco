"""
Test file for the app itself

Test cases:
- [X] Runs without crashing on load (i.e. no input (a.k.a. the easiest test))
- [ ] Runs without crashing with inputs(?)
- [ ] A clean run results in expected session state
"""

import os

from streamlit.testing.v1 import AppTest


def test_app():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", "src", "streamlit_app.py")

    app = AppTest.from_file(file_path)

    app.run()

    assert not app.exception
