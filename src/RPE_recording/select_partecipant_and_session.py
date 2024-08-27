from dearpygui import dearpygui as dpg
from pathlib import Path
from loguru import logger
import os
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.config import PROJ_ROOT

def populate_participants():
    participants = os.listdir(os.path.join(PROJ_ROOT, "raw_data"))
    
    if not participants:  # Check if the list is empty
        dpg.configure_item("participant_combo", items=["No participants found"])
        dpg.set_value("participant_combo", "No participants found")
        logger.error("No participants found.")
    else:
        dpg.configure_item("participant_combo", items=participants)

def populate_sessions(sender, app_data, user_data):
    participant = dpg.get_value("participant_combo")
    
    if participant == "No participants found":
        logger.error("No participants selected because there are none.")
        dpg.configure_item("session_combo", items=["No sessions found"])
        dpg.set_value("session_combo", "No sessions found")
        return
    
    sessions = os.listdir(os.path.join(PROJ_ROOT, "raw_data", participant))
    
    if not sessions:  # Check if the list is empty
        dpg.configure_item("session_combo", items=["No sessions found"])
        dpg.set_value("session_combo", "No sessions found")
        logger.error(f"No sessions found for participant {participant}.")
    else:
        dpg.configure_item("session_combo", items=sessions)

def load_session(sender, app_data):
    participant = dpg.get_value("participant_combo")
    session = dpg.get_value("session_combo")

    if participant == "No participants found" or session == "No sessions found":
        logger.error("Cannot load session because a valid participant or session was not selected.")
        return

    logger.info(f"Working with participant: {participant}, session: {session}")

