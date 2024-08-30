from datetime import datetime
from loguru import logger
from pathlib import Path
import csv
import dearpygui.dearpygui as dpg
from src.config import RAW_DATA_DIR


def save_data(data, time_data):

    participant = dpg.get_value("participant_combo")
    session = dpg.get_value("session_combo")

    logger.info(f"Saving data for participant {participant} and session {session}")

    if not participant or not session:
        logger.error("Participant or session not selected. Data not saved.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"RPE_data_{participant}_{session}_{timestamp}.csv"
    filepath = RAW_DATA_DIR / participant / session / "RPE" / filename 

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'RPE Value'])
        for t, v in zip(time_data, data):
            writer.writerow([f"{t:.2f}", v])
