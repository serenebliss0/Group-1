import tkinter as tk
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets" / "images"

# Design System Tokens
BG = "#1a0a00"       # Ruin Dark Background
EMBER = "#C8541A"    # Primary Accent
FOG = "#b8a99a"      # Subdued Text
CREAM = "#f5ead8"    # Body Text
DIM = "#4a3728"      # Ash Secondary Text

class SceneScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        
        # Map Coordinates Configuration
        self.map_width = 3840
        self.map_height = 2160
        
        # Player position initialization (Centered in the virtual world matrix)
        self.player_x = 1920
        self.player_y = 1080
        self.move_speed = 12
        
        # Load Scenario Content CSV Database 
        self.scenarios = self._load_scenarios()
        
        self._build_ui()
        self._bind_inputs()
        
    def _load_scenarios(self):
        scenarios = {}
        csv_path = Path(__file__).resolve().parent.parent.parent / "scenarios.csv"
        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    scenarios[int(row['id'])] = row
        except Exception:
            # Fallback mock data if file initialization framework breaks
            scenarios[1] = {
                "name": "The Phone Board",
                "text": "This circuit board was a phone. It stopped charging in 2022. It ended up in a pile in Alaba Market...",
                "choice_a": "Examine closer", "choice_b": "Ignore it", "choice_c": "Leave district"
            }
        return scenarios

    def _build_ui(self):
        # 1. Setup Camera Viewport Window Canvas Frame
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.configure(scrollregion=(0, 0, self.map_width, self.map_height))
        
        # 2. Add Static Environmental Background Assets or Vector representations
        # Act I - Calm, structured, peaceful layout tone
        self.canvas.create_rectangle(100, 100, 3740, 2060, outline=DIM, width=2, dash=(4,4))
        
        # Scattered Invisible Interactive Elements hinted by context outlines
        self.interactive_nodes = [
            {"id": 1, "x": 1500, "y": 900, "radius": 40, "triggered": False, "obj_id": None},
            {"id": 2, "x": 2400, "y": 1300, "radius": 40, "triggered": False, "obj_id": None}
        ]
        
        for node in self.interactive_nodes:
            node["obj_id"] = self.canvas.create_oval(
                node["x"] - node["radius"], node["y"] - node["radius"],
                node["x"] + node["radius"], node["y"] + node["radius"],
                outline=DIM, fill="", width=1
            )
            
        # 3. Create Player Representation Element Tracker
        self.player_avatar = self.canvas.create_oval(
            self.player_x - 12, self.player_y - 12,
            self.player_x + 12, self.player_y + 12,
            fill=EMBER, outline=CREAM, width=2
        )
        
        # Initial Viewport Tracking Center Lock
        self._update_camera()

    def _bind_inputs(self):
        # Bind WASD Movements mapping
        self.bind_all("<w>", lambda e: self._move(0, -self.move_speed))
        self.bind_all("<s>", lambda e: self._move(0, self.move_speed))
        self.bind_all("<a>", lambda e: self._move(-self.move_speed, 0))
        self.bind_all("<d>", lambda e: self._move(self.move_speed, 0))
        
        # Interaction System key mappings
        self.bind_all("<e>", lambda e: self._check_interaction())
        self.bind_all("<Tab>", lambda e: self._check_interaction())
        
        # System State Pause execution keybind
        self.bind_all("<Escape>", lambda e: self._open_pause_menu())

    def _move(self, dx, dy):
        """Processes target steps checking bounding box collisions with map borders."""
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        if 0 <= new_x <= self.map_width:
            self.player_x = new_x
        if 0 <= new_y <= self.map_height:
            self.player_y = new_y
            
        self.canvas.coords(
            self.player_avatar,
            self.player_x - 12, self.player_y - 12,
            self.player_x + 12, self.player_y + 12
        )
        self._update_camera()
        self._check_proximity_hints()

    def _update_camera(self):
        """Centres the canvas viewport scroll coordinates tracking the player position."""
        self.update_idletasks()
        win_w = self.canvas.winfo_width() or 1200
        win_h = self.canvas.winfo_height() or 800
        
        scroll_x = (self.player_x - (win_w / 2)) / self.map_width
        scroll_y = (self.player_y - (win_h / 2)) / self.map_height
        
        self.canvas.xview_moveto(max(0.0, min(scroll_x, 1.0)))
        self.canvas.yview_moveto(max(0.0, min(scroll_y, 1.0)))

    def _check_proximity_hints(self):
        """Slightly shifts item outlines color dynamically when approaching."""
        for node in self.interactive_nodes:
            distance = ((self.player_x - node["x"])**2 + (self.player_y - node["y"])**2)**0.5
            if distance < 120:
                self.canvas.itemconfig(node["obj_id"], outline=FOG)
            else:
                self.canvas.itemconfig(node["obj_id"], outline=DIM)

    def _check_interaction(self):
        """Examines nearest item matrices coordinates to spawn modal dialog overlays."""
        for node in self.interactive_nodes:
            distance = ((self.player_x - node["x"])**2 + (self.player_y - node["y"])**2)**0.5
            if distance <= node["radius"] + 15:
                self._launch_dialog(node["id"])
                return

    def _launch_dialog(self, scenario_id):
        data = self.scenarios.get(scenario_id, self.scenarios[1])
        DialogueOverlay(self, data)

    def _open_pause_menu(self):
        PauseOverlay(self, self.controller)


# ── OVERLAY INTERACTIVE WIDGET COMPONENTS ──

class DialogueOverlay(tk.Frame):
    def __init__(self, parent, data):
        # Uses place layout architecture to float atop the map window canvas cleanly
        super().__init__(parent, bg=BG, highlightbackground=EMBER, highlightthickness=1)
        self.data = data
        self.pack_propagate(False)
        self.place(relx=0.5, rely=0.5, width=640, height=360, anchor="center")
        
        # Frame Layout Labels specifications matching layout documents
        tk.Label(self, text=data['name'].upper(), bg=BG, fg=EMBER, font=("Courier", 11, "bold")).pack(pady=(20, 10))
        
        msg_box = tk.Text(self, bg=BG, fg=CREAM, font=("Courier", 10), wrap="word", relief="flat")
        msg_box.insert("1.0", data['text'])
        msg_box.configure(state="disabled")
        msg_box.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Decision Context Choice Action Triggers
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(fill="x", side="bottom", pady=20, padx=20)
        
        for idx, choice_key in enumerate(['choice_a', 'choice_b', 'choice_c']):
            if data.get(choice_key):
                tk.Button(
                    btn_frame, text=data[choice_key].upper(), bg=BG, fg=FOG,
                    activebackground=EMBER, activeforeground=CREAM, font=("Courier", 8),
                    relief="flat", borderwidth=1, command=self.close
                ).pack(side="left", expand=True, fill="x", padx=4)

    def close(self):
        self.destroy()


class PauseOverlay(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG, highlightbackground=DIM, highlightthickness=2)
        self.controller = controller
        self.place(relx=0.5, rely=0.5, width=300, height=400, anchor="center")
        
        tk.Label(self, text="GAME PAUSED", bg=BG, fg=CREAM, font=("Courier", 14, "bold")).pack(pady=30)
        
        buttons = [
            ("RESUME", self.close),
            ("SETTINGS", lambda: self.controller.show_frame("SettingsScreen")),
            ("MAIN MENU", lambda: self.controller.show_frame("MenuScreen")),
            ("QUIT GAME", parent.quit)
        ]
        
        for text, cmd in buttons:
            tk.Button(
                self, text=text, bg=BG, fg=FOG, activebackground=EMBER,
                activeforeground=CREAM, font=("Courier", 10, "bold"),
                relief="flat", width=20, command=cmd
            ).pack(pady=12, ipady=6)

    def close(self):
        self.destroy()