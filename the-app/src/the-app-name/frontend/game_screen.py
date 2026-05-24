"""Core explorable world — camera, movement, interactions."""

import tkinter as tk
import time

from backend import collisions, events, game_state
from backend.map_renderer import MapRenderer
from backend.theme import (
    ASH,
    BG,
    CREAM,
    DIM,
    EMBER,
    FOG,
    FONT_UI,
    INTERACT_RADIUS,
    MAP_HEIGHT,
    MAP_WIDTH,
    MUTED_GREEN,
    PLAYER_SIZE,
    PLAYER_SPEED,
    ROAD,
    WATER_CLEAN,
    WATER_TOXIC,
)
from backend.world import INTERACTABLES, OBSTACLES, load_scenarios
from frontend.dialogue import DialogueOverlay
from frontend.pause_menu import PauseOverlay
from frontend.tutorial_overlay import TutorialOverlay, should_show_tutorial

# keysym -> internal movement key
_KEYSYMS_PRESS = {
    "w": "w", "W": "w",
    "s": "s", "S": "s",
    "a": "a", "A": "a",
    "d": "d", "D": "d",
    "Up": "up", "Down": "down", "Left": "left", "Right": "right",
}


class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.state = game_state.GameState()
        self.scenarios = load_scenarios()
        self.map_renderer = MapRenderer()
        self.keys_pressed = set()
        self.paused = False
        self.in_dialogue = False
        self._tutorial_open = False
        self._tick_id = None
        self._play_start = time.time()
        self._layer_ids = {}
        self._interact_markers = {}
        self._proximity_glow = {}
        self._keys_bound = False
        self._total_interactables = len(INTERACTABLES)

        self.canvas = tk.Canvas(
            self, bg=BG, highlightthickness=0, bd=0,
            scrollregion=(0, 0, MAP_WIDTH, MAP_HEIGHT),
            xscrollincrement=1,
            yscrollincrement=1,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.configure(takefocus=1)
        self.canvas.bind("<Button-1>", self._focus_game)
        self.canvas.bind("<Enter>", self._focus_game)

        self.hud = tk.Frame(self, bg=BG)
        self.hud.place(relx=0.02, rely=0.02)
        self.score_label = tk.Label(
            self.hud, text="", bg=BG, fg=FOG, font=FONT_UI, anchor="w"
        )
        self.score_label.pack(anchor="w")
        self.controls_hint = tk.Label(
            self.hud,
            text="WASD / Arrows — move   ·   E — interact   ·   ESC — pause",
            bg=BG,
            fg=DIM,
            font=("Courier", 8),
        )
        self.controls_hint.pack(anchor="w", pady=(4, 0))

        self.prompt_label = tk.Label(self, text="", bg=BG, fg=EMBER, font=FONT_UI)
        self.prompt_label.place(relx=0.5, rely=0.88, anchor="center")

        self._build_world()
        pw, ph = PLAYER_SIZE, PLAYER_SIZE
        self.player_w, self.player_h = pw, ph
        self.player_x = MAP_WIDTH // 2 - pw / 2
        self.player_y = MAP_HEIGHT // 2 - ph / 2
        self.player_id = self.canvas.create_oval(
            self.player_x, self.player_y,
            self.player_x + pw, self.player_y + ph,
            fill=EMBER, outline=CREAM, width=2, tags="player",
        )
        self.canvas.tag_raise("player")
        self.after(50, self._update_camera)

        self._memorial = {
            "id": "memorial",
            "scenario_id": 11,
            "x": 1240, "y": 1240, "w": 120, "h": 120, "event_id": "",
        }

    def _focus_game(self, event=None):
        try:
            self.canvas.focus_force()
        except tk.TclError:
            pass

    def _build_world(self):
        self.canvas.delete("all")
        self._layer_ids = {}
        self._interact_markers = {}
        self._proximity_glow = {}
        self.map_renderer.draw_base(self.canvas, self._layer_ids)
        self._create_interact_markers()

    def _create_interact_markers(self):
        for obj in INTERACTABLES:
            oid = obj["id"]
            if oid in self.state.triggered_interactables:
                continue
            cx = obj["x"] + obj["w"] / 2
            cy = obj["y"] + obj["h"] / 2
            glow = self.canvas.create_oval(
                cx - 8, cy - 8, cx + 8, cy + 8,
                fill="", outline=DIM, width=1, dash=(3, 3),
                tags=("interact_glow", oid),
            )
            hit = self.canvas.create_rectangle(
                obj["x"], obj["y"], obj["x"] + obj["w"], obj["y"] + obj["h"],
                fill="", outline="", tags=("interact", oid),
            )
            self._interact_markers[oid] = hit
            self._proximity_glow[oid] = glow

    def _apply_world_visuals(self):
        flags = self.state.world_flags
        c = self.canvas
        if flags.get("river") and self._layer_ids.get("river"):
            c.itemconfig(self._layer_ids["river"], fill=WATER_CLEAN)
        if flags.get("pipe") and self._layer_ids.get("pipe_leak"):
            c.itemconfig(self._layer_ids["pipe_leak"], fill=DIM)
        if flags.get("tree") and self._layer_ids.get("tree"):
            c.itemconfig(self._layer_ids["tree"], fill=MUTED_GREEN)
        if flags.get("garbage") and self._layer_ids.get("garbage"):
            c.itemconfig(self._layer_ids["garbage"], fill=ROAD)
        if flags.get("lights"):
            for lid in self._layer_ids.get("streetlights", []):
                c.itemconfig(lid, fill="#c9b87a")
        if flags.get("filter") and self._layer_ids.get("purifier"):
            c.itemconfig(self._layer_ids["purifier"], outline=MUTED_GREEN)

    def _accepts_input(self):
        if self.controller._current_frame is not self:
            return False
        if self.paused or self.in_dialogue or self._tutorial_open:
            return False
        return True

    def on_show(self):
        self.state = game_state.GameState()
        user = getattr(self.controller, "current_user", None)
        if getattr(self.controller, "start_new_game", False):
            self.state.reset_run()
            self.controller.start_new_game = False
            self._build_world()
        elif user and game_state.has_save(user):
            data = game_state.load_game(user)
            if data:
                self.state.load_from_dict(data)
            self._rebuild_interact_markers()
        else:
            self._rebuild_interact_markers()

        self.player_x = self.state.player_x - self.player_w / 2
        self.player_y = self.state.player_y - self.player_h / 2
        self.player_id = self.canvas.create_oval(
            self.player_x, self.player_y,
            self.player_x + self.player_w, self.player_y + self.player_h,
            fill=EMBER, outline=CREAM, width=2, tags="player",
        )
        self.canvas.tag_raise("player")
        self._apply_world_visuals()
        self._update_hud()
        self._bind_keys()
        self.after(80, self._focus_game)
        self.after(120, self._update_camera)

        audio = getattr(self.controller, "audio", None)
        if audio:
            audio.play_ambient("ambient_wind")
        self._play_start = time.time()
        if self._tick_id:
            self.after_cancel(self._tick_id)
        self._game_tick()

        if should_show_tutorial():
            self._show_tutorial()
        else:
            self._focus_game()

    def _show_tutorial(self):
        self._tutorial_open = True
        TutorialOverlay(self, on_dismiss=self._tutorial_done).place(
            relx=0, rely=0, relwidth=1, relheight=1
        )
        self.lift()

    def _tutorial_done(self):
        self._tutorial_open = False
        self._focus_game()

    def on_hide(self):
        self._unbind_keys()
        if self._tick_id:
            self.after_cancel(self._tick_id)
            self._tick_id = None
        audio = getattr(self.controller, "audio", None)
        if audio:
            audio.stop_ambient()

    def _bind_keys(self):
        if self._keys_bound:
            return
        root = self.controller
        root.bind("<KeyPress>", self._on_key_press)
        root.bind("<KeyRelease>", self._on_key_release)
        self.canvas.bind("<KeyPress>", self._on_key_press)
        self.canvas.bind("<KeyRelease>", self._on_key_release)
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)
        self._keys_bound = True

    def _unbind_keys(self):
        if not self._keys_bound:
            return
        try:
            self.controller.unbind("<KeyPress>")
            self.controller.unbind("<KeyRelease>")
        except tk.TclError:
            pass
        for w in (self, self.canvas):
            try:
                w.unbind("<KeyPress>")
                w.unbind("<KeyRelease>")
            except tk.TclError:
                pass
        self._keys_bound = False
        self.keys_pressed.clear()

    def _on_key_press(self, event):
        if not self._accepts_input():
            return
        sym = event.keysym
        if sym in ("e", "E"):
            self._try_interact()
            return "break"
        if sym == "Escape":
            self._toggle_pause()
            return "break"
        mapped = _KEYSYMS_PRESS.get(sym)
        if mapped:
            self.keys_pressed.add(mapped)
            return "break"

    def _on_key_release(self, event):
        if not self._accepts_input():
            return
        mapped = _KEYSYMS_PRESS.get(event.keysym)
        if mapped:
            self.keys_pressed.discard(mapped)
            return "break"

    def _game_tick(self):
        if self._accepts_input():
            self._process_movement()
            self._check_proximity()
            elapsed = int(time.time() - self._play_start)
            self.state.playtime_seconds = max(self.state.playtime_seconds, elapsed)
        self._tick_id = self.after(16, self._game_tick)

    def _process_movement(self):
        dx = dy = 0.0
        speed = PLAYER_SPEED
        if "w" in self.keys_pressed or "up" in self.keys_pressed:
            dy -= speed
        if "s" in self.keys_pressed or "down" in self.keys_pressed:
            dy += speed
        if "a" in self.keys_pressed or "left" in self.keys_pressed:
            dx -= speed
        if "d" in self.keys_pressed or "right" in self.keys_pressed:
            dx += speed
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
        if dx or dy:
            ok, nx, ny = collisions.can_move(
                self.player_x, self.player_y, self.player_w, self.player_h,
                dx, dy, OBSTACLES, MAP_WIDTH, MAP_HEIGHT,
            )
            if ok:
                self.player_x, self.player_y = nx, ny
                self.state.player_x = nx + self.player_w / 2
                self.state.player_y = ny + self.player_h / 2
                self._sync_player()
                self._update_camera()

    def _sync_player(self):
        self.canvas.coords(
            self.player_id,
            self.player_x, self.player_y,
            self.player_x + self.player_w, self.player_y + self.player_h,
        )
        self.canvas.tag_raise("player")

    def _update_camera(self):
        self.update_idletasks()
        vw = max(self.canvas.winfo_width(), 1)
        vh = max(self.canvas.winfo_height(), 1)
        if vw >= MAP_WIDTH and vh >= MAP_HEIGHT:
            return
        cx = self.player_x + self.player_w / 2
        cy = self.player_y + self.player_h / 2
        max_x = max(MAP_WIDTH - vw, 1)
        max_y = max(MAP_HEIGHT - vh, 1)
        left = max(0, min(cx - vw / 2, max_x))
        top = max(0, min(cy - vh / 2, max_y))
        self.canvas.xview_moveto(left / max_x)
        self.canvas.yview_moveto(top / max_y)

    def _active_interactables(self):
        items = [
            o for o in INTERACTABLES
            if o["id"] not in self.state.triggered_interactables
        ]
        if len(self.state.triggered_interactables) >= 4:
            items.append(self._memorial)
        return items

    def _check_proximity(self):
        target = collisions.nearest_interactable(
            self.player_x, self.player_y, self.player_w, self.player_h,
            self._active_interactables(), INTERACT_RADIUS,
        )
        for oid, glow_id in self._proximity_glow.items():
            if oid in self.state.triggered_interactables:
                continue
            try:
                self.canvas.itemconfig(glow_id, outline=DIM)
            except tk.TclError:
                pass
        if target:
            self.prompt_label.config(text="[E]  Interact")
            oid = target["id"]
            if oid in self._proximity_glow:
                self.canvas.itemconfig(self._proximity_glow[oid], outline=EMBER, width=2)
        else:
            self.prompt_label.config(text="")

    def _try_interact(self):
        if not self._accepts_input():
            return
        target = collisions.nearest_interactable(
            self.player_x, self.player_y, self.player_w, self.player_h,
            self._active_interactables(), INTERACT_RADIUS,
        )
        if not target:
            return
        sid = target.get("scenario_id", 1)
        data = self.scenarios.get(sid)
        if not data:
            return
        audio = getattr(self.controller, "audio", None)
        if audio:
            audio.play_sfx("click")
        self.in_dialogue = True
        self.keys_pressed.clear()
        DialogueOverlay(
            self,
            data,
            on_close=self._dialogue_closed,
            on_choice=self._on_choice,
            audio=audio,
        ).place(relx=0, rely=0, relwidth=1, relheight=1)
        self.lift()

    def _rebuild_interact_markers(self):
        for mid in list(self._interact_markers.values()):
            try:
                self.canvas.delete(mid)
            except tk.TclError:
                pass
        for gid in list(self._proximity_glow.values()):
            try:
                self.canvas.delete(gid)
            except tk.TclError:
                pass
        self._interact_markers.clear()
        self._proximity_glow.clear()
        self._create_interact_markers()

    def start_new_run(self):
        self.state.reset_run()
        self._build_world()
        self.player_x = MAP_WIDTH // 2 - self.player_w / 2
        self.player_y = MAP_HEIGHT // 2 - self.player_h / 2
        if self.canvas.find_withtag("player"):
            self.canvas.delete("player")
        self.player_id = self.canvas.create_oval(
            self.player_x, self.player_y,
            self.player_x + self.player_w, self.player_y + self.player_h,
            fill=EMBER, outline=CREAM, width=2, tags="player",
        )
        self.canvas.tag_raise("player")
        self._update_camera()
        self._update_hud()

    def _on_choice(self, choice_index, scenario_row):
        if int(scenario_row.get("id", 0)) == 11:
            self._dialogue_closed()
            self._finish_game()
            return
        events.resolve_choice(choice_index, scenario_row, self.state)
        oid = None
        for obj in INTERACTABLES:
            if obj.get("scenario_id") == int(scenario_row.get("id", 0)):
                oid = obj["id"]
                break
        if oid:
            self.state.mark_interactable(oid)
            for mid in (self._interact_markers.pop(oid, None), self._proximity_glow.pop(oid, None)):
                if mid:
                    try:
                        self.canvas.delete(mid)
                    except tk.TclError:
                        pass
        self._apply_world_visuals()
        self._update_hud()
        user = getattr(self.controller, "current_user", None)
        if user and self.controller.db and self.state.run_id:
            delta = events.choice_delta(choice_index, scenario_row)
            key = ("a", "b", "c")[choice_index]
            self.controller.db.save_choice(
                self.state.run_id, int(scenario_row["id"]), key.upper(), delta
            )

    def _dialogue_closed(self):
        self.in_dialogue = False
        self._focus_game()

    def _update_hud(self):
        n = len(self.state.triggered_interactables)
        self.score_label.config(
            text=f"Restoration {self.state.restoration_percent()}%  ·  "
            f"Fragments {self.state.memory_fragments}  ·  "
            f"Explored {n}/{self._total_interactables}"
        )

    def _toggle_pause(self):
        if self.in_dialogue or self._tutorial_open:
            return
        for child in self.winfo_children():
            if isinstance(child, PauseOverlay):
                return
        self.paused = True
        self.keys_pressed.clear()
        PauseOverlay(
            self,
            self.controller,
            on_resume=self._resume_pause,
            on_save=self._save,
        ).place(relx=0, rely=0, relwidth=1, relheight=1)

    def _resume_pause(self):
        self.paused = False
        self._focus_game()

    def _save(self):
        user = getattr(self.controller, "current_user", None)
        if user:
            game_state.save_game(user, self.state)

    def _finish_game(self):
        self.paused = True
        self._unbind_keys()
        user = getattr(self.controller, "current_user", None) or "guest"
        ending = self.state.ending_key()
        score = self.state.restoration_percent()
        items = self.state.memory_fragments
        time_played = self.state.playtime_seconds
        if self.controller.db:
            run_id = self.controller.db.save_run(
                user, score, items, time_played, "normal", ending
            )
            self.state.run_id = run_id
        game_state.save_game(user, self.state)
        self.controller.pending_ending = ending
        self.controller.show_frame("EndingScreen")
