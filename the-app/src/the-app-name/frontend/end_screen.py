import tkinter as tk
import sys

class EndScreen(tk.Frame):
    def __init__(self, parent, ending_type="THE RUIN", health=0, score=0, leaderboard_cb=None, play_again_cb=None):
        """
        Initializes the accurate End Screen based on design specs.
        """
        # Start with near-black for all to allow for the Green transition
        super().__init__(parent, bg="#0a0a0a")
        self.parent = parent
        self.ending_type = ending_type.upper()
        self.health = health
        self.score = score
        self.leaderboard_cb = leaderboard_cb
        self.play_again_cb = play_again_cb

        # Configure main layout to be left-aligned with padding
        self.grid_columnconfigure(0, weight=1)
        self.main_container = tk.Frame(self, bg="#0a0a0a")
        self.main_container.pack(fill="both", expand=True, padx=80, pady=60)

        self.build_screen()

    def build_screen(self):
        if self.ending_type == "THE GREEN":
            self.build_green()
        elif self.ending_type == "THE RUIN":
            self.build_ruin()
        elif self.ending_type == "THE THIRD":
            self.build_third()
        else:
            # Fallback
            tk.Label(self.main_container, text="UNKNOWN ENDING", fg="white", bg="#0a0a0a").pack()

    def create_header(self, title_text, title_color):
        """Helper to create the top 'ENDING . [TYPE]' and Main Title"""
        tk.Label(self.main_container, text=f"ENDING · {title_text}", fg="#888888", bg="#0a0a0a", 
                 font=("Helvetica", 10, "bold"), anchor="w").pack(fill="x")
        
        tk.Frame(self.main_container, bg="#333333", height=1).pack(fill="x", pady=(5, 20), width=200, anchor="w")
        
        title = tk.Label(self.main_container, text=title_text, fg=title_color, bg="#0a0a0a", 
                         font=("Helvetica", 48, "bold"), anchor="w")
        title.pack(fill="x", pady=(0, 30))
        return title

    def create_narrative(self, text):
        """Helper to create the narrative text block"""
        text_frame = tk.Frame(self.main_container, bg="#111111", padx=30, pady=30)
        text_frame.pack(fill="x", pady=(0, 40))
        
        # Using Crimson Pro as requested, fallback to Georgia/Serif
        tk.Label(text_frame, text=text, fg="#e0e0e0", bg="#111111", 
                 font=("Crimson Pro", 16, "italic"), justify="left", anchor="w").pack(fill="x")

    def create_stats_and_buttons(self, show_timer=False):
        """Helper to create the health/score readouts and buttons"""
        stats_frame = tk.Frame(self.main_container, bg="#0a0a0a")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Health
        health_frame = tk.Frame(stats_frame, bg="#0a0a0a")
        health_frame.pack(side="left", padx=(0, 40))
        tk.Label(health_frame, text="FINAL CITY HEALTH", fg="#888888", bg="#0a0a0a", font=("Helvetica", 10)).pack(anchor="w")
        tk.Label(health_frame, text=f"{self.health}%", fg="#4ade80" if self.ending_type == "THE GREEN" else "#ea580c", 
                 bg="#0a0a0a", font=("Helvetica", 24, "bold")).pack(anchor="w")

        # Score
        score_frame = tk.Frame(stats_frame, bg="#0a0a0a")
        score_frame.pack(side="left")
        tk.Label(score_frame, text="FINAL SCORE", fg="#888888", bg="#0a0a0a", font=("Helvetica", 10)).pack(anchor="w")
        tk.Label(score_frame, text=f"{self.score:,}", fg="#ea580c", bg="#0a0a0a", font=("Helvetica", 24, "bold")).pack(anchor="w")

        # Progress bar simulator
        bar_color = "#4ade80" if self.ending_type == "THE GREEN" else "#ea580c"
        bar_frame = tk.Frame(self.main_container, bg="#333333", height=8, width=400)
        bar_frame.pack(anchor="w", pady=(0, 20))
        bar_frame.pack_propagate(False)
        fill_width = int(400 * (self.health / 100))
        tk.Frame(bar_frame, bg=bar_color, height=8, width=fill_width).pack(side="left")

        # Optional Timer Text (For Ruin)
        if show_timer:
            tk.Label(self.main_container, text="Leaderboard opens automatically in 5 seconds.", 
                     fg="#888888", bg="#0a0a0a", font=("Helvetica", 12, "italic"), anchor="w").pack(fill="x", pady=(10, 20))

        # Buttons
        btn_frame = tk.Frame(self.main_container, bg="#0a0a0a")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        # Primary Button
        view_lb_btn = tk.Button(btn_frame, text="VIEW LEADERBOARD", bg="#d95319", fg="white", 
                                font=("Helvetica", 10, "bold"), width=20, relief="flat", command=self.leaderboard_cb)
        view_lb_btn.pack(side="left", padx=(0, 15), ipady=8)
        
        # Ghost Button
        play_btn = tk.Button(btn_frame, text="PLAY AGAIN", bg="#1a1a1a", fg="#a0a0a0", 
                             font=("Helvetica", 10, "bold"), width=15, relief="flat", command=self.play_again_cb)
        play_btn.pack(side="left", ipady=8)

    # --- ENDING SPECIFIC BUILDERS ---

    def build_green(self):
        title = self.create_header("THE GREEN", "#4ade80")
        narrative = ("You were made from what they threw away.\n"
                     "You became what they forgot was possible.\n\n"
                     "The city breathes again. For the first time, you walk into green space.\n"
                     "The circuit boards in your chest pulse with something that might be called hope.\n"
                     "Others will follow the path you have left.")
        self.create_narrative(narrative)
        self.create_stats_and_buttons()
        
        # Trigger the 3-second color bleed to deep forest green (#0f1a0f)
        self.fade_to_green(steps=30, current_step=0)

    def fade_to_green(self, steps, current_step):
        """Simulates a background color bleed over 3 seconds (3000ms)"""
        if current_step <= steps:
            # Interpolate between #0a0a0a (10,10,10) and #0f1f0f (15,31,15)
            r = int(10 + ((15 - 10) * (current_step / steps)))
            g = int(10 + ((31 - 10) * (current_step / steps)))
            b = int(10 + ((15 - 10) * (current_step / steps)))
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            self.config(bg=hex_color)
            self.main_container.config(bg=hex_color)
            # 3000ms total / 30 steps = 100ms per step
            self.after(100, lambda: self.fade_to_green(steps, current_step + 1))

    def build_ruin(self):
        self.create_header("THE RUIN", "#ea580c")
        narrative = ("What is remembered may still return.\n"
                     "But not today.\n\n"
                     "The city does not breathe. The plants around you die slowly.\n"
                     "The circuit boards in your chest have gone quiet.")
        self.create_narrative(narrative)
        self.create_stats_and_buttons(show_timer=True)
        
        # Leaderboard opens automatically in 5 seconds
        if self.leaderboard_cb:
            self.after(5000, self.leaderboard_cb)

    def build_third(self):
        # Pure greyscale, no score, no buttons
        self.config(bg="#1a1a1a")
        self.main_container.config(bg="#1a1a1a")
        
        tk.Label(self.main_container, text="Some people stood in front of the bull and felt nothing.", 
                 fg="#888888", bg="#1a1a1a", font=("Crimson Pro", 14, "italic")).pack(expand=True)
        
        # Museum guide animation placeholder (simple moving square crossing the screen)
        self.canvas = tk.Canvas(self, height=20, bg="#1a1a1a", highlightthickness=0)
        self.canvas.place(x=0, y=100, width=1920)
        self.guide = self.canvas.create_rectangle(0, 5, 10, 15, fill="#444444", outline="")
        self.animate_guide()

        # Game process closes (museum closes) after 8 seconds
        self.after(8000, self.close_game)

    def animate_guide(self):
        self.canvas.move(self.guide, 2, 0)
        self.after(20, self.animate_guide)

    def close_game(self):
        print("The museum closes. Disengaging process.")
        self.parent.destroy()
        sys.exit()


# TEST HARNESS

if __name__ == "__main__":
    root = tk.Tk()
    root.title("End Screen Test")
    root.geometry("1000x700")
    root.configure(bg="black")

    def open_leaderboard():
        print("Opening Leaderboard...")
        
    def restart():
        print("Restarting Game...")

    # Change "THE RUIN" to "THE GREEN" or "THE THIRD" to test different endings
    screen = EndScreen(
        root, 
        ending_type="THE GREEN", 
        health=82, 
        score=4280, 
        leaderboard_cb=open_leaderboard, 
        play_again_cb=restart
    )
    screen.pack(fill="both", expand=True)
    
    root.mainloop()