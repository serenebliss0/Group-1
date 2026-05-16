from pathlib import Path
from .logger import get_logger 
import pygame

logger = get_logger("Pygame")
BASE_DIR = Path(__file__).resolve().parent.parent

class Mixer():
    def __init__(self):

        try:
            pygame.init()
            logger.info("Pygame initialized syccessfully")

        except Exception as e:
            logger.error(f"Pygame failed to initialize: {e} ")

        try:
            pygame.mixer.init()
            logger.info("Pygame mixer initialized successfully")

        except Exception as e:
            logger.error("Pygame mixer failed to initialize: {e}")

    def play_intro_sound(self):
        
        audio_path = BASE_DIR / "assets" / "sounds" / "demo_intro.wav"

        print(audio_path)

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)

        input("playing...")
        logger.info("A sound was played")

    def on_close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()


class AudioManager:
    def __init__(self):
        pygame.mixer.init()

    def play_intro(self):
        pygame.mixer.music.load("assets/sounds/demo_intro.wav")
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def shutdown(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()

#Implementation test
if __name__ == "__main__":
    mixer = Mixer()
    audio_manager = AudioManager()
    mixer.play_intro_sound()
    audio_manager.stop_music()
    audio_manager.shutdown()