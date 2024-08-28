from src.config import SOUNDS_DIR
from playsound import playsound
import threading
from loguru import logger

def beep(sound_file= SOUNDS_DIR / 'beep.wav'):
    def _beep():
        try:
            playsound(sound_file)
        except Exception as e:
            logger.error(f"Failed to play sound: {e}")
    
    # Run the beep in a separate thread
    threading.Thread(target=_beep, daemon=True).start()