from datetime import datetime
from loguru import logger
from pathlib import Path
import csv

from src.config import PROJ_ROOT

def save_data():
    global participant, session, data, time_data
    if not participant or not session:
        logger.warning("Participant or session not selected. Data not saved.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"RPE_data_{participant}_{session}_{timestamp}.csv"
    filepath = PROJ_ROOT / filename

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'RPE Value'])
        for t, v in zip(time_data, data):
            if v is not None:
                writer.writerow([f"{t:.2f}", v])

    logger.info(f"Data saved to {filepath}")