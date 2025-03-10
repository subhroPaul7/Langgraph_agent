import os
from datetime import datetime, timezone
import streamlit as st
from textwrap import wrap


# for loading configs to environment variables using st.secrets
def load_config():
    # Define default values
    default_values = {
        'SERPER_API_KEY': 'default_serper_api_key',
        'GROQ_API_KEY': 'default_groq_api_key'
        # 'GEMINI_API_KEY': 'default_gemini_api_key'
    }
    
    for key, default_value in default_values.items():
        os.environ[key] = st.secrets.get(key, default_value)

# for getting the current date and time in UTC
def get_current_utc_datetime():
    now_utc = datetime.now(timezone.utc)
    current_time_utc = now_utc.strftime("%Y-%m-%d %H:%M:%S %Z")
    return current_time_utc

# for checking if an attribute of the state dict has content.
def check_for_content(var):
    if var:
        try:
            var = var.content
            return var.content
        except:
            return var
    else:
        var

def custom_print(message, stdscr=None, scroll_pos=0):
    if stdscr:
        max_y, max_x = stdscr.getmaxyx()
        max_y -= 2  # Leave room for a status line at the bottom

        wrapped_lines = []
        for line in message.split("\n"):
            wrapped_lines.extend(wrap(line, max_x))

        num_lines = len(wrapped_lines)
        visible_lines = wrapped_lines[scroll_pos:scroll_pos + max_y]

        stdscr.clear()
        for i, line in enumerate(visible_lines):
            stdscr.addstr(i, 0, line[:max_x])

        stdscr.addstr(max_y, 0, f"Lines {scroll_pos + 1} - {scroll_pos + len(visible_lines)} of {num_lines}")
        stdscr.refresh()

        return num_lines
    else:
        print(message)
