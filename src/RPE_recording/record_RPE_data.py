from pathlib import Path
import inquirer
from loguru import logger
import sys
from typing import Optional, List

# Add pythonpath to the system path
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Import PROJ_ROOT and RAW_DATA_DIR from config.py
from src.config import PROJ_ROOT, RAW_DATA_DIR


def strip_proj_root(path: Path) -> Path:
    """Utility function to strip the PROJ_ROOT from a given Path."""
    try:
        return path.relative_to(PROJ_ROOT)
    except ValueError:
        # If path is not under PROJ_ROOT, return the original path
        return path



def list_subdirectories(parent_dir: Path) -> List[Path]:
    """List all subdirectories in a given parent directory, skipping those with a COMPLETED.txt file."""
    subdirs = [
        subdir for subdir in parent_dir.iterdir() 
        if subdir.is_dir() and not (subdir / "COMPLETED.txt").exists()
    ]
    stripped_parent_dir = strip_proj_root(parent_dir)
    # logger.debug(f"Subdirectories in {stripped_parent_dir} (excluding those with COMPLETED.txt): {subdirs}")
    return subdirs

def choose_participant(base_path: Path) -> Optional[Path]:
    """Prompt user to choose a participant from the available directories using inquirer."""
    participants = list_subdirectories(base_path)
    if not participants:
        logger.warning("No available participants found (all have COMPLETED.txt or none exist).")
        print("No available participants found.")
        return None
    
    participant_names = [participant.name for participant in participants]

    questions = [
        inquirer.List(
            'participant',
            message="Select a participant",
            choices=participant_names
        )
    ]
    answers = inquirer.prompt(questions)
    selected_participant = answers['participant']

    stripped_participant = strip_proj_root(base_path / selected_participant)
    logger.info(f"Selected participant: {stripped_participant}")
    return base_path / selected_participant

def choose_session(participant_path: Path) -> Optional[Path]:
    """Prompt user to choose a session for the selected participant using inquirer."""
    sessions = list_subdirectories(participant_path)
    if not sessions:
        stripped_participant_path = strip_proj_root(participant_path)
        logger.warning(f"No available sessions found for participant {stripped_participant_path} (all have COMPLETED.txt or none exist).")
        print("No available sessions found for the selected participant.")
        return None

    session_names = [session.name for session in sessions]

    questions = [
        inquirer.List(
            'session',
            message="Select a session",
            choices=session_names
        )
    ]
    answers = inquirer.prompt(questions)
    selected_session = answers['session']

    stripped_session = strip_proj_root(participant_path / selected_session)
    logger.info(f"Selected session: {stripped_session}")
    return participant_path / selected_session

def create_rpe_folder(session_path: Path) -> Path:
    """Create an RPE folder inside the chosen session directory if it doesn't exist."""
    rpe_folder = session_path / 'RPE'
    if not rpe_folder.exists():
        rpe_folder.mkdir()
        stripped_rpe_folder = strip_proj_root(rpe_folder)
        logger.info(f"Created RPE folder: {stripped_rpe_folder}")
    else:
        stripped_rpe_folder = strip_proj_root(rpe_folder)
        logger.info(f"RPE folder already exists: {stripped_rpe_folder}")
    return rpe_folder

def save_set_file(rpe_folder: Path) -> None:
    """Save a set file in the RPE folder with the appropriate set number."""
    existing_files = list(rpe_folder.glob("set*.txt"))
    set_number = len(existing_files) + 1
    set_filename = rpe_folder / f"set{set_number}.txt"
    
    with open(set_filename, 'w') as f:
        f.write(f"Set number {set_number}")
    
    stripped_set_filename = strip_proj_root(set_filename)
    logger.info(f"Created set file: {stripped_set_filename}")

def main() -> None:
    logger.info("Starting the data collection utility")
    base_path = RAW_DATA_DIR  # Use RAW_DATA_DIR from config.py
    
    try:
        participant_path = choose_participant(base_path)
        if participant_path is None:
            logger.info("No participants available. Exiting.")
            return

        session_path = choose_session(participant_path)
        if session_path is None:
            logger.info("No sessions available for the selected participant. Exiting.")
            return
        
        rpe_folder = create_rpe_folder(session_path)
        save_set_file(rpe_folder)
        
        logger.info("Data collection process completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
