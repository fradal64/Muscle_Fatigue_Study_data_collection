import re
from pathlib import Path


def extract_session_info_from_path(file_path: Path):
    """
    Extracts the participant name (without '_Right' or '_Left'), session number, side info ('Left' or 'Right'),
    and set number (from the file name just before the extension) from the file path.

    Args:
        file_path (Path): The file path to extract information from.

    Returns:
        tuple: A tuple containing the participant name, session number, side info, and set number.
    """
    parts = file_path.parts

    # Regular expressions to extract participant, session, side, and set info
    participant_pattern = re.compile(r"P\d+_\w+")
    session_pattern = re.compile(r"Session_(\d+)")
    side_pattern = re.compile(r"(Left|Right)")
    set_pattern = re.compile(r"_(\d+)\.txt$")

    participant_name = None
    session_info = None
    side_info = None
    set_info = None

    # Iterate over the path components and search for matching patterns
    for part in parts:
        if participant_pattern.search(part):
            participant_name = part
        if session_pattern.search(part):
            session_info = session_pattern.search(part).group(0)  # Extracts the full "Session_001"
        if side_pattern.search(part):
            side_info = side_pattern.search(part).group(1)  # Extract Left or Right

    # Strip '_Right' or '_Left' from the participant name
    if participant_name:
        participant_name = re.sub(r"_(Left|Right)", "", participant_name)

    # Extract the set number from the file name
    file_name = file_path.name
    if set_pattern.search(file_name):
        set_info = set_pattern.search(file_name).group(
            1
        )  # Extract the set number (e.g., '1' from 'Leonardo_Garofalo_Right_1.txt')

    # Safeguard: ensure all needed info is extracted
    if not participant_name or not session_info or not side_info or not set_info:
        raise ValueError(f"Could not extract session info correctly from path: {file_path}")

    return participant_name, session_info, side_info, set_info
