import tkinter as tk
import json
from pathlib import Path
from PIL import Image, ImageTk

from .pause import PauseMenu
from .game_over import GameOverScreen
from .win_screen import WinScreen


BG = "#1a0a00"
EMBER = "#C8541A"
CREAM = "#f5ead8"


class Scene2(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)

        self.controller = controller

        # ---------------- PATHS ---------------- #
        BASE_DIR = Path(__file__).resolve().parent
        SCENARIOS_PATH = BASE_DIR / "scenarios.json"
        ASSETS = BASE_DIR.parent / "assets" / "images"

        # ---------------- MAP ---------------- #
        self.map_img_raw = Image.open(ASSETS / "map.png")

        self.ZOOM = 2.5

        self.map_img_raw = self.map_img_raw.resize(
            (
                int(self.map_img_raw.width * self.ZOOM),
                int(self.map_img_raw.height * self.ZOOM)
            ),
            Image.Resampling.LANCZOS
        )

        self.map_img = ImageTk.PhotoImage(self.map_img_raw)
        self.map_width, self.map_height = self.map_img_raw.size

        # ---------------- PLAYER ---------------- #
        self.player_x = self.map_width // 2
        self.player_y = self.map_height // 2
        self.move_speed = 12

        # ---------------- TIMER ---------------- #
        self.default_time = 10*60
        self.time_left = self.default_time
        self.timer_running = False
        self.game_over = False

        # ---------------- STATE ---------------- #
        self.fixed_nodes = set()
        self.fixed_images = {}
        self.current_dialog_node = None

        # ---------------- LOAD DATA ---------------- #
        with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
            self.scenarios = json.load(f)

        # ---------------- UI ---------------- #
        self._build_ui()
        self._bind_inputs()
        self._start_timer()

    # ==================================================
    def reset_game(self):

        self.game_over = False
        self.timer_running = False
        self.time_left = self.default_time

        self.player_x = self.map_width // 2
        self.player_y = self.map_height // 2

        self.fixed_nodes.clear()
        self.fixed_images.clear()
        self.current_dialog_node = None

        self.info_box.place_forget()

        self.canvas.coords(
            self.player_avatar,
            self.player_x - 12,
            self.player_y - 12,
            self.player_x + 12,
            self.player_y + 12
        )

        self._start_timer()

    # ==================================================
    def _build_ui(self):

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.configure(
            scrollregion=(0, 0, self.map_width, self.map_height)
        )

        self.canvas.create_image(0, 0, image=self.map_img, anchor="nw")

        tk.Button(
            self,
            text="II",
            command=self._open_pause,
            bg="#0C0904",
            fg="#E8DCC8"
        ).place(x=20, y=20, width=40, height=40)

        self.timer_label = tk.Label(
            self,
            text="10:00",
            bg=BG,
            fg=CREAM,
            font=("Courier", 14, "bold")
        )
        self.timer_label.place(relx=0.98, rely=0.02, anchor="ne")

        self.info_box = tk.Frame(self, bg="#2a1a10")

        self.info_title = tk.Label(self.info_box, text="", bg="#2a1a10", fg=CREAM)
        self.info_title.pack()

        self.info_text = tk.Label(self.info_box, text="", bg="#2a1a10", fg=CREAM)
        self.info_text.pack()

        self.info_box.place_forget()

        self.interactive_nodes = [
            {
                "id": item["id"],
                "x": item["x"],
                "y": item["y"],
                "type": item.get("type", "clean"),
                "name": item["name"],
                "text": item["text"]
            }
            for item in self.scenarios
        ]

        self.player_avatar = self.canvas.create_oval(
            self.player_x - 12,
            self.player_y - 12,
            self.player_x + 12,
            self.player_y + 12,
            fill=EMBER,
            outline=CREAM
        )

        self._update_camera()   # ✅ NOW EXISTS

    # ==================================================
    def _update_camera(self):
        # FIXED METHOD (this was missing before)

        w = self.canvas.winfo_width() or 1200
        h = self.canvas.winfo_height() or 800

        sx = (self.player_x - w / 2) / self.map_width
        sy = (self.player_y - h / 2) / self.map_height

        self.canvas.xview_moveto(max(0, min(1, sx)))
        self.canvas.yview_moveto(max(0, min(1, sy)))

    # ==================================================
    def _bind_inputs(self):

        self.bind_all("<w>", lambda e: self._move(0, -self.move_speed))
        self.bind_all("<s>", lambda e: self._move(0, self.move_speed))
        self.bind_all("<a>", lambda e: self._move(-self.move_speed, 0))
        self.bind_all("<d>", lambda e: self._move(self.move_speed, 0))

        self.bind_all("<Escape>", lambda e: self._open_pause())

    # ==================================================
    def _start_timer(self):

        if self.timer_running:
            return

        self.timer_running = True
        self._tick_timer()

    def _tick_timer(self):

        if self.game_over:
            return

        m = self.time_left // 60
        s = self.time_left % 60

        self.timer_label.config(text=f"{m:02d}:{s:02d}")

        if self.time_left > 0:
            self.time_left -= 1
            self.after(1000, self._tick_timer)
        else:
            self._trigger_game_over()

    # ==================================================
    def _trigger_game_over(self):

        self.game_over = True

        missed = [
            n for n in self.interactive_nodes
            if n["type"] == "pollution" and n["id"] not in self.fixed_nodes
        ]

        GameOverScreen(self, self.controller, missed)

    # ==================================================
    def _trigger_win(self):

        self.game_over = True
        WinScreen(self, self.controller)

    # ==================================================
    def _check_win_condition(self):

        for n in self.interactive_nodes:
            if n["type"] == "pollution" and n["id"] not in self.fixed_nodes:
                return

        self._trigger_win()

    # ==================================================
    def _move(self, dx, dy):

        if self.game_over:
            return

        self.player_x += dx
        self.player_y += dy

        self.canvas.coords(
            self.player_avatar,
            self.player_x - 12,
            self.player_y - 12,
            self.player_x + 12,
            self.player_y + 12
        )

        self._update_camera()
        self._check_proximity()

    # ==================================================
    def _check_proximity(self):
        pass  # keep your existing logic here if you had it

    # ==================================================
    def _open_pause(self):
        PauseMenu(self, self.controller)