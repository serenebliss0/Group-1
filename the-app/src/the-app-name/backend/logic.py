from pathlib import Path
from .logger import get_logger 
import pygame
import getpass
import json

wtf_value = 0

logger = get_logger("Pygame")
BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = Path(__file__).resolve().parent / "session.json"
class GameEasterEggs():

    def save_session(username):
        with open(SESSION_FILE, "w") as f:
            json.dump({"current_user": username}, f)


    def load_session():
        if not SESSION_FILE.exists():
            return None

        with open(SESSION_FILE, "r") as f:
            data = json.load(f)

        return data.get("current_user")


    def clear_session():
        with open(SESSION_FILE, "w") as f:
            json.dump({"current_user": None}, f)

class Mixer():
    def __init__(self):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            logger.info("Pygame mixer initialized successfully")
        except Exception as e:
            logger.error(f"Pygame mixer failed to initialize: {e}")

    def play_intro_sound(self):
        audio_path = BASE_DIR / "assets" / "sounds" / "demo_intro.wav"
        try:
            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.play(-1)
            logger.info("Intro sound playing")
        except Exception as e:
            logger.error(f"Failed to play sound: {e}")

    def on_close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    def stop_music(self):
            pygame.mixer.music.stop()

    def shutdown(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        


class user_info:
    def get_real_username(self):
        username = getpass.getuser()
        print(username)


#Implementation test
if __name__ == "__main__":
    mixer = Mixer()
    mixer.play_intro_sound()
    
    user = user_info()
    user.get_real_username()
