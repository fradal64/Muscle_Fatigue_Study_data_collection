import re
from pathlib import Path

import pandas as pd

from src.config import PROJ_ROOT
from src.utils.extract_session_info_from_file_path import extract_session_info_from_path
from src.utils.get_rpe_filepath import get_rpe_file_path


def convert_txt_to_csv(txt_file: Path, output_dir: Path):
    """
    Converts a .txt file with time and sEMG values to a .csv file, appending the RPE data
    to the right side of the existing columns, and renaming columns as needed.

    Args:
        txt_file (Path): The path to the .txt file.
        output_dir (Path): The directory where the .csv file will be saved.
    """
    # Load the .txt file (EMG data)
    try:
        emg_data = pd.read_csv(txt_file, sep=r"\s+", header=None, skiprows=5)
    except pd.errors.ParserError as e:
        print(f"Error parsing file {txt_file}: {e}")
        return

    # Extract participant name, session number, and side information
    try:
        participant_name, session_info, side_info, set_info = extract_session_info_from_path(
            txt_file
        )
    except ValueError as e:
        print(f"Error extracting session info from file {txt_file}: {e}")
        return

    # Rename the EMG time and sEMG columns
    emg_data.columns = ["time_sEMG_seconds", "sEMG"]

    # Get the corresponding RPE file path
    rpe_file = get_rpe_file_path(txt_file)

    # If the RPE file exists, load the RPE data and append it to the right
    if rpe_file:
        try:
            rpe_data = pd.read_csv(rpe_file)
            rpe_data.columns = ["time_RPE_seconds", "RPE"]
            emg_data = pd.concat([emg_data, rpe_data], axis=1)
        except Exception as e:
            print(f"Error loading or appending RPE data from {rpe_file}: {e}")

    # Save as a .csv file with participant name, session number, and side info in the filename
    csv_filename = output_dir / f"{participant_name}_{side_info}_{session_info}_Set_{set_info}.csv"

    emg_data.to_csv(csv_filename, index=False)
    print(f"Saved .csv file to {csv_filename}")


def process_raw_data_directory(raw_data_dir: Path, csv_data_dir: Path):
    """
    Walks through the raw_data_dir, preserves only the main folder names in csv_data_dir, 
    and converts all .txt files to .csv format, skipping any files named 'completed.txt'.

    Args:
        raw_data_dir (Path): The directory containing the raw .txt files.
        csv_data_dir (Path): The directory where the converted .csv files will be saved.
    """
    for txt_file in raw_data_dir.rglob("*.txt"):
        if txt_file.name == "completed.txt":
            print(f"Skipping file: {txt_file}")
            continue

        # Only preserve the main folder (first-level folder) structure
        main_folder = txt_file.relative_to(raw_data_dir).parts[0]
        output_dir = csv_data_dir / main_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        # Convert the .txt file to .csv and save it in the corresponding folder
        convert_txt_to_csv(txt_file, output_dir)


if __name__ == "__main__":
    raw_data_directory = PROJ_ROOT / "raw_data"  # Path to the raw data directory
    csv_data_directory = PROJ_ROOT / "csv_data"  # Path to the csv data directory

    # Ensure the base output directory exists
    csv_data_directory.mkdir(exist_ok=True)

    # Process all .txt files in the raw data directory
    process_raw_data_directory(raw_data_directory, csv_data_directory)
