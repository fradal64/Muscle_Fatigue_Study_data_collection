import re
from pathlib import Path

from src.utils.extract_session_info_from_file_path import extract_session_info_from_path
from src.utils.natural_sort_key import natural_sort_key


def get_rpe_file_path(txt_file: Path) -> Path:
    """
    Retrieves the RPE file path corresponding to the provided txt file based on the order of the files
    in the RPE folder (1-to-1 correspondence with EMG files).

    Args:
        txt_file (Path): The path to the .txt file for which we want to find the corresponding RPE file.

    Returns:
        Path: The path to the corresponding RPE file.
    """
    # Extract session, participant, and side information from the txt file path
    try:
        participant_name, session_info, side_info, set_info = extract_session_info_from_path(
            txt_file
        )
    except ValueError as e:
        print(f"Error extracting session info from file {txt_file}: {e}")
        return None

    # Construct the path to the RPE folder corresponding to the session
    rpe_dir = txt_file.parent.parent / "RPE"  # Navigate to the RPE directory of the session

    # List all RPE files in the RPE directory and sort them in natural order
    rpe_files = sorted(rpe_dir.glob("*.csv"), key=natural_sort_key)

    # Convert the set_info (EMG file number) to a 0-based index
    set_index = int(set_info) - 1

    # Ensure the set index does not exceed the number of RPE files
    if set_index >= len(rpe_files):
        print(f"No matching RPE file for set {set_info} in {rpe_dir}")
        return None

    # Return the corresponding RPE file based on its order
    return rpe_files[set_index]
