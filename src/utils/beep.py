import threading

from loguru import logger
from playsound import playsound

from src.config import SOUNDS_DIR


def beep(sound_file=SOUNDS_DIR / "beep.wav"):
    def _beep():
        try:
            playsound(sound_file)
        except Exception as e:
            logger.error(f"Failed to play sound: {e}")

    # Run the beep in a separate thread
    threading.Thread(target=_beep, daemon=True).start()
