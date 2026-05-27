import pygame
import json
from pathlib import Path
from .logger import get_logger

logger = get_logger("Input Handler")

class InputManager:
    def __init__(self):
        pygame.joystick.init()
        pygame.key.set_repeat(0)
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP])

        base_dir = Path(__file__).resolve().parent
        with open(base_dir / "keybinds.json", "r") as f:
            self.keybinds = json.load(f)

        #only initialize joystick if a controller is detected
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.pressed = set()
        self.easter_egg_triggered = False
        logger.info("Input Handler has started")

    def update(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        self.pressed.clear()

        for action, key_name in self.keybinds.items():
            try:
                key_code = pygame.key.key_code(key_name)

                if keys[key_code]:
                    self.pressed.add(action)

                    # store raw key for combos
                    self.combo_buffer.append(key_name.lower())

            except Exception as e:
                print(e)

        # keep buffer small
        self.combo_buffer = self.combo_buffer[-self.combo_limit]

        # Easter egg combo
        if "f12" in self.combo_buffer and "tab" in self.combo_buffer:
            if not self.easter_egg_triggered:
                self.easter_egg_triggered = True
                print("EASTER EGG UNLOCKED") ###Rem later

    def is_pressed(self, action):
        return action in self.pressed