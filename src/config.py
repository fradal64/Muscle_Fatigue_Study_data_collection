from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJ_ROOT / 'raw_data'
PARTECIPANT_MAPPING_FILE = PROJ_ROOT / 'participant_mapping.csv'