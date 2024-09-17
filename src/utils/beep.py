import threading

import pygame
from loguru import logger

from src.config import SOUNDS_DIR

# Initialize the pygame mixer
pygame.mixer.init()


def beep():
    try:
        # Load the sound
        sound = pygame.mixer.Sound(str(SOUNDS_DIR / "beep.wav"))
        # Play the sound asynchronously
        sound.play()
    except Exception as e:
        logger.error(f"Failed to play sound: {e}")


def beep_async():
    # Run the beep in a separate thread to avoid blocking GUI
    threading.Thread(target=beep, daemon=True).start()
