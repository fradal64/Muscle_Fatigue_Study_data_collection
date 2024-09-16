import re
from pathlib import Path

import inquirer

from src.config import PROJ_ROOT
from src.utils.extract_session_info_from_file_path import extract_session_info_from_path
from src.utils.natural_sort_key import natural_sort_key


def select_file(prompt: str, directory: Path, file_extension: str) -> Path:
    """
    Prompts the user to select a file from a specific directory with a specific extension,
    displaying session, participant name, and left/right information in the dropdown menu.

    Args:
        prompt (str): The prompt to display for file selection.
        directory (Path): The directory to search within.
        file_extension (str): The file extension to filter by.

    Returns:
        Path: The selected file path.
    """
    files = list(directory.rglob(f"*{file_extension}"))
    relative_paths = [
        file.relative_to(PROJ_ROOT) for file in files if file.name != "completed.txt"
    ]
    sorted_paths = sorted(relative_paths, key=natural_sort_key)

    # Prepare the list of filenames for display with session, participant name, and left/right info
    display_choices = []
    file_mapping = {}  # Dictionary to map display choices back to file paths

    for path in sorted_paths:
        try:
            participant_name, session_info, side_info, set_info = extract_session_info_from_path(
                path
            )
            display_name = f"Participant: {participant_name}, {session_info}, Side: {side_info}, Set: {set_info}"
            display_choices.append(display_name)
            file_mapping[display_name] = path
        except ValueError as e:
            print(f"Skipping file due to error: {e}")

    questions = [
        inquirer.List(
            "file",
            message=prompt,
            choices=display_choices,
            carousel=True,
        )
    ]
    answers = inquirer.prompt(questions)
    selected_file = file_mapping[answers["file"]]
    return PROJ_ROOT / selected_file
