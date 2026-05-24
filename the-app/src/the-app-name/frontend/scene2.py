import tkinter as tk
import json
from pathlib import Path
from PIL import Image, ImageTk

from .pause import PauseMenu
from .dialogue_overlay import DialogueOverlay


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

        self.ZOOM = 2.2
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
        self.time_left = 10 * 60
        self.timer_running = False

        # ---------------- FIX SYSTEM ---------------- #
        self.fixed_nodes = set()
        self.fixed_images = {}

        # ---------------- LOAD DATA ---------------- #
        with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
            self.scenarios = {item["id"]: item for item in json.load(f)}

        # ---------------- UI ---------------- #
        self._build_ui()
        self._bind_inputs()
        self._start_timer()

    # ==================================================
    def _build_ui(self):

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.configure(scrollregion=(0, 0, self.map_width, self.map_height))
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

        self.info_box = tk.Label(
            self,
            text="",
            bg="#2a1a10",
            fg=CREAM,
            font=("Courier", 11),
            wraplength=250,
            justify="left"
        )
        self.info_box.place_forget()

        # ---------------- FIXED COORDINATES ---------------- #
        self.interactive_nodes = [
            {"id": 1, "x": 1350, "y": 300, "radius": 70},  # Factory Pollution (adjusted right)
            {"id": 2, "x": 1500, "y": 400, "radius": 70},  # Oil Spill (adjusted right)

            {"id": 3, "x": 200, "y": 550, "radius": 70},
            {"id": 4, "x": 1200, "y": 900, "radius": 70},
            {"id": 5, "x": 1000, "y": 500, "radius": 70},
            {"id": 6, "x": 900, "y": 520, "radius": 70},
            {"id": 7, "x": 1500, "y": 700, "radius": 70},
            {"id": 8, "x": 1050, "y": 750, "radius": 70},
            {"id": 9, "x": 360, "y": 200, "radius": 70},
            {"id": 10, "x": 800, "y": 800, "radius": 70}
        ]

        self.player_avatar = self.canvas.create_oval(
            self.player_x - 12,
            self.player_y - 12,
            self.player_x + 12,
            self.player_y + 12,
            fill=EMBER,
            outline=CREAM,
            width=2
        )

        self._update_camera()

    # ==================================================
    def _bind_inputs(self):
        self.bind_all("<w>", lambda e: self._move(0, -self.move_speed))
        self.bind_all("<s>", lambda e: self._move(0, self.move_speed))
        self.bind_all("<a>", lambda e: self._move(-self.move_speed, 0))
        self.bind_all("<d>", lambda e: self._move(self.move_speed, 0))
        self.bind_all("<e>", lambda e: self._interact())
        self.bind_all("<Escape>", lambda e: self._open_pause())

    # ==================================================
    def _start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True
        self._tick_timer()

    def _tick_timer(self):
        m = self.time_left // 60
        s = self.time_left % 60

        self.timer_label.config(text=f"{m:02d}:{s:02d}")

        if self.time_left > 0:
            self.time_left -= 1
            self.after(1000, self._tick_timer)

    # ==================================================
    def _move(self, dx, dy):
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
    def _update_camera(self):
        w = self.canvas.winfo_width() or 1200
        h = self.canvas.winfo_height() or 800

        sx = (self.player_x - w / 2) / self.map_width
        sy = (self.player_y - h / 2) / self.map_height

        self.canvas.xview_moveto(max(0, min(1, sx)))
        self.canvas.yview_moveto(max(0, min(1, sy)))

    # ==================================================
    def _check_proximity(self):
        for node in self.interactive_nodes:

            dist = ((self.player_x - node["x"]) ** 2 +
                    (self.player_y - node["y"]) ** 2) ** 0.5

            data = self.scenarios.get(node["id"])

            if dist < 150 and data:
                self.info_box.config(text=f"{data['name']}\n\n{data['text']}")
                self.info_box.place(x=20, y=80)
                return

        self.info_box.place_forget()

    # ==================================================
    def _interact(self):
        for node in self.interactive_nodes:

            dist = ((self.player_x - node["x"]) ** 2 +
                    (self.player_y - node["y"]) ** 2) ** 0.5

            if dist <= node["radius"] + 20:

                data = self.scenarios.get(node["id"])
                if data:
                    self._show_fix_menu(node, data)
                return

    # ==================================================
    def _show_fix_menu(self, node, data):
        win = tk.Toplevel(self)
        win.title(data["name"])
        win.geometry("320x220")
        win.config(bg=BG)

        tk.Label(
            win,
            text=data["text"],
            bg=BG,
            fg=CREAM,
            wraplength=280
        ).pack(pady=10)

        def fix():
            self._fix_node(node)
            win.destroy()

        tk.Button(
            win,
            text="FIX",
            bg="green",
            fg="white",
            command=fix
        ).pack(pady=10)

    # ==================================================
    def _fix_node(self, node):

        if node["id"] in self.fixed_nodes:
            return

        self.fixed_nodes.add(node["id"])

        img = Image.open(
            Path(__file__).resolve().parent.parent / "assets/images/factory_fixed.png"
        ).resize((80, 80))

        tk_img = ImageTk.PhotoImage(img)
        self.fixed_images[node["id"]] = tk_img

        self.canvas.create_image(node["x"], node["y"], image=tk_img)

    # ==================================================
    def _open_pause(self):
        PauseMenu(self, self.controller)