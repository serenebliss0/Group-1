"""Game audio via pygame.mixer — music, ambient, SFX."""

from pathlib import Path

from .game_state import load_settings
from .logger import get_logger

logger = get_logger("Audio")

try:
    import pygame
except ImportError:
    pygame = None

BASE_DIR = Path(__file__).resolve().parent.parent
SOUNDS_DIR = BASE_DIR / "assets" / "sounds"


class GameAudio:
    """Single audio manager attached to the main app."""

    def __init__(self):
        self.settings = load_settings()
        self._music_loaded = False
        self._ambient_channel = None
        if pygame is None:
            logger.warning("pygame not available")
            return
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
        except Exception as e:
            logger.error(f"Mixer init failed: {e}")

    def _path(self, name):
        for ext in (".wav", ".ogg", ".mp3"):
            p = SOUNDS_DIR / f"{name}{ext}"
            if p.exists():
                return p
        return None

    def set_music_volume(self, vol):
        self.settings["music_volume"] = max(0.0, min(1.0, vol))
        if pygame and pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.settings["music_volume"])

    def set_sfx_volume(self, vol):
        self.settings["sfx_volume"] = max(0.0, min(1.0, vol))

    def play_music(self, name="demo_intro", loop=-1):
        if not pygame or not pygame.mixer.get_init():
            return
        path = self._path(name)
        if not path:
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(self.settings["music_volume"])
            pygame.mixer.music.play(loop)
            self._music_loaded = True
        except Exception as e:
            logger.error(f"Music play failed: {e}")

    def play_ambient(self, name="ambient_wind"):
        if not pygame or not pygame.mixer.get_init():
            return
        path = self._path(name)
        if not path:
            return
        try:
            snd = pygame.mixer.Sound(str(path))
            snd.set_volume(self.settings["sfx_volume"] * 0.5)
            self._ambient_channel = snd.play(-1)
        except Exception as e:
            logger.error(f"Ambient failed: {e}")

    def play_sfx(self, name="click"):
        if not pygame or not pygame.mixer.get_init():
            return
        path = self._path(name)
        if not path:
            return
        try:
            snd = pygame.mixer.Sound(str(path))
            snd.set_volume(self.settings["sfx_volume"])
            snd.play()
        except Exception as e:
            logger.error(f"SFX failed: {e}")

    def stop_music(self):
        if pygame and pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def stop_ambient(self):
        if self._ambient_channel:
            try:
                self._ambient_channel.stop()
            except Exception:
                pass
            self._ambient_channel = None

    def on_close(self):
        self.stop_ambient()
        self.stop_music()
        if pygame and pygame.mixer.get_init():
            pygame.mixer.quit()

    # Back-compat with logic.Mixer
    def play_intro_sound(self):
        self.play_music("demo_intro")
