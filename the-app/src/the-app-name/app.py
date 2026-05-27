import tkinter as tk
from tkinter import messagebox
import random

BG = "#0d0800"
ACCENT = "#C8541A"
TEXT = "#f5ead8"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What Remains")
        self.geometry("800x600")
        self.configure(bg=BG)

        self.player_health = 100
        self.player_energy = 100
        self.inventory = []
        self.current_level = None
        self.completed_levels = []
        
        self.armour_parts = {
            "head": "Rust Helmet",
            "torso": "Scrap Chest",
            "arms": "Wire Arms",
            "legs": "Metal Legs"
        }

        self.tutorial_done = False

        self.frames = {}
        for F in (HomeScreen, MapScreen, GameScreen, InventoryScreen, CustomizeScreen):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_frame("HomeScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "update_ui"):
            frame.update_ui()
        frame.tkraise()
        if page_name == "GameScreen":
            frame.focus_set()
            frame.start_level()

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(self, text="HOME BASE", font=("Arial", 24, "bold"), bg=BG, fg=ACCENT).pack(pady=20)

        self.stats_frame = tk.Frame(self, bg=BG)
        self.stats_frame.pack(pady=10)
        
        self.health_label = tk.Label(self.stats_frame, text="", font=("Arial", 14), bg=BG, fg=TEXT)
        self.health_label.pack()
        
        self.energy_label = tk.Label(self.stats_frame, text="", font=("Arial", 14), bg=BG, fg=TEXT)
        self.energy_label.pack()

        self.custom_label = tk.Label(self, text="", font=("Arial", 12), bg=BG, fg=TEXT)
        self.custom_label.pack(pady=10)

        btn_style = {"font": ("Arial", 14, "bold"), "bg": ACCENT, "fg": BG, "width": 15, "pady": 5}
        
        tk.Button(self, text="MAP", command=lambda: controller.show_frame("MapScreen"), **btn_style).pack(pady=10)
        tk.Button(self, text="INVENTORY", command=lambda: controller.show_frame("InventoryScreen"), **btn_style).pack(pady=10)
        tk.Button(self, text="CUSTOMIZE", command=lambda: controller.show_frame("CustomizeScreen"), **btn_style).pack(pady=10)

    def update_ui(self):
        self.health_label.config(text=f"Health: {self.controller.player_health}")
        self.energy_label.config(text=f"Energy: {self.controller.player_energy}")
        c = self.controller.armour_parts
        self.custom_label.config(text=f"Armour: {c['head']} | {c['torso']} | {c['arms']} | {c['legs']}")

class MapScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(self, text="MISSION MAP", font=("Arial", 24, "bold"), bg=BG, fg=ACCENT).pack(pady=20)

        self.buttons = {}
        self.levels = [
            ("Dump Site", None),
            ("Waterfront", "Dump Site"),
            ("Factory", "Waterfront"),
            ("Market", "Factory"),
            ("School", "Market"),
            ("Final Zone", "School")
        ]

        btn_style = {"font": ("Arial", 14, "bold"), "width": 20, "pady": 5}

        for lvl, req in self.levels:
            btn = tk.Button(self, text=lvl, command=lambda l=lvl: self.enter_level(l), **btn_style)
            btn.pack(pady=5)
            self.buttons[lvl] = btn

        tk.Button(self, text="BACK TO HOME", command=lambda: controller.show_frame("HomeScreen"), font=("Arial", 12, "bold"), bg=ACCENT, fg=BG).pack(pady=20)

    def update_ui(self):
        for lvl, req in self.levels:
            btn = self.buttons[lvl]
            if lvl in self.controller.completed_levels:
                btn.config(state="normal", bg="green", fg="white")
            elif req is None or req in self.controller.completed_levels:
                btn.config(state="normal", bg=ACCENT, fg=BG)
            else:
                btn.config(state="disabled", bg="gray", fg="darkgray")

    def enter_level(self, level):
        self.controller.current_level = level
        self.controller.show_frame("GameScreen")

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self.header_frame = tk.Frame(self, bg=BG)
        self.header_frame.pack(fill="x", pady=5, padx=10)

        self.info_label = tk.Label(self.header_frame, text="", font=("Arial", 14, "bold"), bg=BG, fg=TEXT)
        self.info_label.pack(side="left")

        self.score_label = tk.Label(self.header_frame, text="", font=("Arial", 14, "bold"), bg=BG, fg=TEXT)
        self.score_label.pack(side="right")

        self.canvas = tk.Canvas(self, width=780, height=500, bg="black", highlightthickness=2, highlightbackground=ACCENT)
        self.canvas.pack(pady=5)

        self.bind("<KeyPress-w>", lambda e: self.move(0, -10))
        self.bind("<KeyPress-s>", lambda e: self.move(0, 10))
        self.bind("<KeyPress-a>", lambda e: self.move(-10, 0))
        self.bind("<KeyPress-d>", lambda e: self.move(10, 0))
        self.bind("<space>", lambda e: self.shoot())

        self.player = None
        self.player_text = None
        self.wastes = []
        self.obstacles = []
        self.bullets = []
        self.collected = 0
        self.target_items = 5
        self.last_dir = (0, -10)
        
        self.time_left = 0
        self.timer_id = None
        self.bullet_loop_id = None

    def start_level(self):
        self.canvas.delete("all")
        self.wastes.clear()
        self.obstacles.clear()
        for b in self.bullets:
            self.canvas.delete(b['id'])
        self.bullets.clear()
        
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        if self.bullet_loop_id:
            self.after_cancel(self.bullet_loop_id)
            self.bullet_loop_id = None

        self.collected = 0
        lvl = self.controller.current_level
        
        if lvl == "Dump Site":
            self.target_items = 5
        elif lvl == "Waterfront":
            self.target_items = 6
        elif lvl == "Factory":
            self.target_items = 6
        elif lvl == "Market":
            self.target_items = 8
            self.time_left = 30
            self.tick_timer()
        elif lvl == "School" or lvl == "Final Zone":
            self.target_items = 10
            
        time_text = f" | Time: {self.time_left}s" if lvl == "Market" else ""
        self.info_label.config(text=f"Level: {lvl}{time_text}")
        self.update_score()

        self.player = self.canvas.create_rectangle(370, 230, 410, 270, fill=ACCENT)
        self.player_text = self.canvas.create_text(390, 250, text="ARMOUR", fill=BG, font=("Arial", 8, "bold"))

        self.generate_level(lvl)

        if not self.controller.tutorial_done:
            self.run_tutorial()
        else:
            self.bullet_loop()

    def generate_level(self, lvl):
        obs_count = 5
        if lvl == "Factory":
            self.obstacles.append(self.canvas.create_rectangle(200, 100, 240, 400, fill="gray"))
            self.obstacles.append(self.canvas.create_rectangle(500, 100, 540, 400, fill="gray"))
            obs_count = 2
            
        for _ in range(obs_count):
            ox = random.randint(50, 700)
            oy = random.randint(50, 450)
            obs = self.canvas.create_rectangle(ox, oy, ox+40, oy+40, fill="gray")
            self.obstacles.append(obs)

        for _ in range(self.target_items):
            wx = random.randint(50, 700)
            wy = random.randint(50, 450)
            color = "purple" if lvl in ["Waterfront", "Factory", "Market", "School", "Final Zone"] else "green"
            waste = self.canvas.create_rectangle(wx, wy, wx+20, wy+20, fill=color)
            self.wastes.append({"id": waste, "type": "breakable" if color == "purple" else "collectable"})

    def run_tutorial(self):
        messages = [
            "Welcome ARMOUR",
            "Use W A S D to move",
            "Collect waste to clean the environment",
            "Press SPACE to break down waste",
            "Complete 5 items to finish level"
        ]
        
        self.tut_label = tk.Label(self.canvas, text="", font=("Arial", 16, "bold"), bg="black", fg="yellow")
        self.tut_window = self.canvas.create_window(390, 100, window=self.tut_label)
        
        def show_msg(idx):
            if idx < len(messages):
                self.tut_label.config(text=messages[idx])
                self.after(2500, lambda: show_msg(idx+1))
            else:
                self.canvas.delete(self.tut_window)
                self.controller.tutorial_done = True
                self.bullet_loop()
                
        show_msg(0)

    def tick_timer(self):
        if self.controller.current_level == "Market" and self.time_left > 0:
            self.time_left -= 1
            self.info_label.config(text=f"Level: Market | Time: {self.time_left}s")
            if self.time_left <= 0 and self.collected < self.target_items:
                messagebox.showinfo("Time Up", "You failed to clean the market in time.")
                self.controller.show_frame("MapScreen")
                return
            self.timer_id = self.after(1000, self.tick_timer)

    def update_score(self):
        self.score_label.config(text=f"Collected: {self.collected}/{self.target_items}")

    def move(self, dx, dy):
        self.last_dir = (dx, dy)
        coords = self.canvas.coords(self.player)
        if not coords: return
        nx1, ny1, nx2, ny2 = coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy

        if nx1 < 0 or ny1 < 0 or nx2 > 780 or ny2 > 500:
            return

        for obs in self.obstacles:
            ox1, oy1, ox2, oy2 = self.canvas.coords(obs)
            if nx1 < ox2 and nx2 > ox1 and ny1 < oy2 and ny2 > oy1:
                return

        self.canvas.move(self.player, dx, dy)
        self.canvas.move(self.player_text, dx, dy)
        self.check_collisions()

    def shoot(self):
        coords = self.canvas.coords(self.player)
        if not coords: return
        bx = (coords[0] + coords[2]) / 2
        by = (coords[1] + coords[3]) / 2
        dx, dy = self.last_dir
        bullet = self.canvas.create_rectangle(bx-2, by-2, bx+2, by+2, fill="yellow")
        self.bullets.append({"id": bullet, "dx": dx*1.5, "dy": dy*1.5})

    def bullet_loop(self):
        for b in self.bullets[:]:
            self.canvas.move(b['id'], b['dx'], b['dy'])
            coords = self.canvas.coords(b['id'])
            if not coords or coords[0] < 0 or coords[1] < 0 or coords[2] > 780 or coords[3] > 500:
                self.canvas.delete(b['id'])
                self.bullets.remove(b)
                continue
                
            hit = False
            for w in self.wastes[:]:
                wx1, wy1, wx2, wy2 = self.canvas.coords(w['id'])
                if coords[0] < wx2 and coords[2] > wx1 and coords[1] < wy2 and coords[3] > wy1:
                    if w['type'] == "breakable":
                        self.canvas.itemconfig(w['id'], fill="green")
                        w['type'] = "collectable"
                    self.canvas.delete(b['id'])
                    if b in self.bullets:
                        self.bullets.remove(b)
                    hit = True
                    break
                    
            if not hit:
                for obs in self.obstacles:
                    ox1, oy1, ox2, oy2 = self.canvas.coords(obs)
                    if coords[0] < ox2 and coords[2] > ox1 and coords[1] < oy2 and coords[3] > oy1:
                        self.canvas.delete(b['id'])
                        if b in self.bullets:
                            self.bullets.remove(b)
                        break

        self.bullet_loop_id = self.after(50, self.bullet_loop)

    def check_collisions(self):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        for w in self.wastes[:]:
            wx1, wy1, wx2, wy2 = self.canvas.coords(w['id'])
            if px1 < wx2 and px2 > wx1 and py1 < wy2 and py2 > wy1:
                if w['type'] == "collectable":
                    self.canvas.delete(w['id'])
                    self.wastes.remove(w)
                    self.collected += 1
                    item_name = f"Scrap_{random.randint(100,999)}"
                    self.controller.inventory.append(item_name)
                    self.update_score()

                    if self.collected >= self.target_items:
                        lvl = self.controller.current_level
                        if lvl not in self.controller.completed_levels:
                            self.controller.completed_levels.append(lvl)
                        
                        if lvl == "School" or lvl == "Final Zone":
                            messagebox.showinfo("Digital Armour", "You have restored the environment. We are What Remains.")
                        else:
                            messagebox.showinfo("Level Completed", "Area cleaned successfully!")
                            
                        self.controller.show_frame("MapScreen")
                elif w['type'] == "breakable":
                    # Cannot collect until broken
                    pass

class InventoryScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(self, text="INVENTORY", font=("Arial", 24, "bold"), bg=BG, fg=ACCENT).pack(pady=20)

        self.listbox = tk.Listbox(self, width=50, height=15, bg="black", fg=TEXT, font=("Arial", 12))
        self.listbox.pack(pady=10)

        btn_style = {"font": ("Arial", 12, "bold"), "bg": ACCENT, "fg": BG, "width": 15}
        tk.Button(self, text="CLEAR", command=self.clear_inventory, **btn_style).pack(pady=5)
        tk.Button(self, text="BACK", command=lambda: controller.show_frame("HomeScreen"), **btn_style).pack(pady=5)

    def update_ui(self):
        self.listbox.delete(0, tk.END)
        for item in self.controller.inventory:
            self.listbox.insert(tk.END, item)

    def clear_inventory(self):
        self.controller.inventory.clear()
        self.update_ui()

class CustomizeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(self, text="CUSTOMIZE ARMOUR", font=("Arial", 24, "bold"), bg=BG, fg=ACCENT).pack(pady=20)

        self.options = {
            "head": ["Rust Helmet", "Titanium Visor", "Neon Mask"],
            "torso": ["Scrap Chest", "Copper Core", "Kevlar Vest"],
            "arms": ["Wire Arms", "Hydraulic Pistons", "Carbon Fiber"],
            "legs": ["Metal Legs", "Tread Tracks", "Spring Boots"]
        }

        self.vars = {}
        for part in ["head", "torso", "arms", "legs"]:
            frame = tk.Frame(self, bg=BG)
            frame.pack(pady=10)
            tk.Label(frame, text=f"{part.upper()}:", font=("Arial", 14, "bold"), bg=BG, fg=TEXT, width=10, anchor="e").pack(side="left", padx=10)
            
            var = tk.StringVar(value=self.controller.armour_parts[part])
            self.vars[part] = var
            menu = tk.OptionMenu(frame, var, *self.options[part], command=lambda val, p=part: self.update_part(p, val))
            menu.config(bg=ACCENT, fg=BG, font=("Arial", 12))
            menu.pack(side="left")

        tk.Button(self, text="BACK", command=lambda: controller.show_frame("HomeScreen"), font=("Arial", 12, "bold"), bg=ACCENT, fg=BG).pack(pady=30)

    def update_part(self, part, value):
        self.controller.armour_parts[part] = value

    def update_ui(self):
        for part, var in self.vars.items():
            var.set(self.controller.armour_parts[part])

if __name__ == "__main__":
    app = App()
    app.mainloop()
