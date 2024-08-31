import os

from dearpygui import dearpygui as dpg
from loguru import logger

from src.config import RAW_DATA_DIR


def populate_participants():
    participants = [item.name for item in RAW_DATA_DIR.iterdir() if item.is_dir()]

    if not participants:  # Check if the list is empty
        dpg.configure_item("participant_combo", items=["No participants found"])
        dpg.set_value("participant_combo", "No participants found")
        logger.error("No participants found.")
    else:
        dpg.configure_item("participant_combo", items=participants)


def get_filtered_sessions(participant_dir):

    sessions = participant_dir.iterdir()  # List all items in the participant's directory

    filtered_sessions = []
    for session in sessions:
        if session.is_dir():  # Ensure the session is a directory
            # Check if "completed.txt" file exists in the session directory
            completed_file = session / "completed.txt"
            
            if not completed_file.exists():  # Exclude directory if it contains "completed.txt"
                filtered_sessions.append(session.name)

    return filtered_sessions

def populate_sessions(sender, app_data, user_data):
    participant = dpg.get_value("participant_combo")

    if participant == "No participants found":
        logger.error("No participants selected because there are none.")
        dpg.configure_item("session_combo", items=["No sessions found"])
        dpg.set_value("session_combo", "No sessions found")
        return

        # Construct the participant's directory path using Path
    participant_dir = RAW_DATA_DIR / participant

    # Filter out directories that should be excluded
    filtered_sessions = get_filtered_sessions(participant_dir)

    if not filtered_sessions:  # Check if the list is empty
        dpg.configure_item("session_combo", items=["No sessions found"])
        dpg.set_value("session_combo", "No sessions found")
        logger.error(f"No sessions found for participant {participant}.")
    else:
        dpg.configure_item("session_combo", items=filtered_sessions)


def load_session(sender, app_data):
    participant = dpg.get_value("participant_combo")
    session = dpg.get_value("session_combo")

    if participant == "No participants found" or session == "No sessions found":
        logger.error(
            "Cannot load session because a valid participant or session was not selected."
        )
        return

    logger.info(f"Working with participant: {participant}, session: {session}")
