import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MAP_PATH = BASE_DIR / "assets" / "images" / "game_map.jpg"

SPEED = 4
WIN_W = 1280
WIN_H = 720
PLAYER_SIZE = 24


class ActOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0C0904")
        self.controller = controller
        self.keys = set()
        self._tick_id = None

        # player starts in center of map
        img = Image.open(MAP_PATH)
        self.map_w, self.map_h = img.size
        self._map_img = ImageTk.PhotoImage(img)

        self.cam_x = self.map_w // 2 - WIN_W // 2
        self.cam_y = self.map_h // 2 - WIN_H // 2
        self.player_x = self.map_w // 2
        self.player_y = self.map_h // 2

        self.canvas = tk.Canvas(
            self, width=WIN_W, height=WIN_H,
            bg="#0C0904", highlightthickness=0
        )
        self.canvas.pack()

        # draw map
        self._map_id = self.canvas.create_image(
            0, 0, anchor="nw", image=self._map_img
        )

        # draw player
        self._player_id = self.canvas.create_oval(
            0, 0, PLAYER_SIZE, PLAYER_SIZE,
            fill="#D4581F", outline="#E8DCC8", width=2
        )

        self._update_canvas()

    def on_show(self):
        self.controller.bind("<KeyPress>", self._key_down)
        self.controller.bind("<KeyRelease>", self._key_up)
        self._tick()

    def on_hide(self):
        self.controller.unbind("<KeyPress>")
        self.controller.unbind("<KeyRelease>")
        if self._tick_id:
            self.after_cancel(self._tick_id)

    def _key_down(self, e):
        self.keys.add(e.keysym.lower())

    def _key_up(self, e):
        self.keys.discard(e.keysym.lower())

    def _tick(self):
        dx = dy = 0
        if "w" in self.keys or "up" in self.keys:    dy -= SPEED
        if "s" in self.keys or "down" in self.keys:  dy += SPEED
        if "a" in self.keys or "left" in self.keys:  dx -= SPEED
        if "d" in self.keys or "right" in self.keys: dx += SPEED

        # clamp player to map bounds
        self.player_x = max(0, min(self.map_w, self.player_x + dx))
        self.player_y = max(0, min(self.map_h, self.player_y + dy))

        # update camera to follow player
        self.cam_x = self.player_x - WIN_W // 2
        self.cam_y = self.player_y - WIN_H // 2
        self.cam_x = max(0, min(self.map_w - WIN_W, self.cam_x))
        self.cam_y = max(0, min(self.map_h - WIN_H, self.cam_y))

        self._update_canvas()
        self._tick_id = self.after(16, self._tick)

    def _update_canvas(self):
        # move map
        self.canvas.coords(self._map_id, -self.cam_x, -self.cam_y)
        # move player to screen center
        sx = self.player_x - self.cam_x - PLAYER_SIZE // 2
        sy = self.player_y - self.cam_y - PLAYER_SIZE // 2
        self.canvas.coords(
            self._player_id,
            sx, sy, sx + PLAYER_SIZE, sy + PLAYER_SIZE
        )