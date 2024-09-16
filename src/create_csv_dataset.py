import re
from pathlib import Path

import inquirer
import numpy as np
import pandas as pd
import scipy.io as sio

from src.config import PROJ_ROOT
from src.utils.extract_session_info_from_file_path import extract_session_info_from_path
from src.utils.select_file import select_file


def convert_txt_to_csv(txt_file: Path, output_dir: Path):
    """
    Converts a .txt file with time and sEMG values to a .csv file.

    Args:
        txt_file (Path): The path to the .txt file.
        output_dir (Path): The directory where the .csv file will be saved.
    """
    # Load the .txt file
    try:
        data = pd.read_csv(txt_file, sep="\s+", header=None, skiprows=5)
    except pd.errors.ParserError as e:
        print(f"Error parsing file {txt_file}: {e}")
        return

    # Extract participant name, session number, and side information using the same function
    try:
        participant_name, session_info, side_info, set_info = extract_session_info_from_path(
            txt_file
        )
    except ValueError as e:
        print(f"Error extracting session info from file {txt_file}: {e}")
        return

    # Save as a .csv file with participant name, session number, and side info in the filename
    csv_filename = output_dir / f"{participant_name}_{side_info}_{session_info}_Set_{set_info}.csv"

    # Write the data to a .csv file
    data.columns = ["time", "sEMG"]  # Assuming the columns are time and sEMG values
    data.to_csv(csv_filename, index=False)

    print(f"Saved .csv file to {csv_filename}")


if __name__ == "__main__":
    # Example usage
    directory_to_search = PROJ_ROOT / "raw_data"  # Replace with the correct path
    selected_txt_file = select_file("Select the .txt file to convert", directory_to_search, ".txt")

    output_directory = PROJ_ROOT / "csv_data"  # Replace with the correct path
    output_directory.mkdir(exist_ok=True)

    convert_txt_to_csv(selected_txt_file, output_directory)
