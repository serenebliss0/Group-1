import tkinter as tk
import csv
from pathlib import Path
from backend.database import Database, Leaderboard

# Design System Tokens (consistent with scene2.py and main_menu.py)
BG = "#0C0904"       # Ruin Dark Background
EMBER = "#C8541A"    # Primary Accent
FOG = "#b8a99a"      # Subdued Text
CREAM = "#f5ead8"    # Body Text
DIM = "#4a3728"      # Ash Secondary Text

# Rank Colors for visual progression
GOLD = "#FFD700"
SILVER = "#C0C0C0"
BRONZE = "#CD7F32"

def get_real_name(username):
    """
    Search for names.csv in Group-1/names.csv by checking multiple parent paths.
    Resolves the player's username to their real name if a match is found.
    """
    if not username:
        return "N/A"
    
    clean_username = username.strip().lower().lstrip('@')
    
    possible_paths = [
        Path(__file__).resolve().parents[4] / "names.csv",
        Path(__file__).resolve().parents[3] / "names.csv",
        Path(__file__).resolve().parents[2] / "names.csv",
        Path(__file__).resolve().parents[1] / "names.csv",
        Path.cwd() / "names.csv",
    ]
    
    csv_path = None
    for p in possible_paths:
        if p.exists():
            csv_path = p
            break
            
    if not csv_path:
        return "N/A"
        
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            # 1. Look for exact matches first
            for row in rows:
                full_name = (row.get("Full Name") or "").strip()
                email = (row.get("Email") or "").strip().lower()
                git_user = (row.get("GitHub Username") or "").strip().lower().lstrip('@')
                email_prefix = email.split('@')[0] if email else ""
                
                if clean_username == git_user or clean_username == email_prefix:
                    return full_name
            
            # 2. Look for substring matches (minimum 3 chars)
            if len(clean_username) >= 3:
                for row in rows:
                    full_name = (row.get("Full Name") or "").strip()
                    email = (row.get("Email") or "").strip().lower()
                    git_user = (row.get("GitHub Username") or "").strip().lower().lstrip('@')
                    email_prefix = email.split('@')[0] if email else ""
                    
                    if (git_user and clean_username in git_user) or (git_user and git_user in clean_username) or \
                       (email_prefix and clean_username in email_prefix) or (email_prefix and email_prefix in clean_username):
                        return full_name
    except Exception:
        pass
    
    return "N/A"


class LeaderboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        
        self.canvas = tk.Canvas(
            self,
            bg=BG,
            height=826,
            width=1130,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Keep track of active interactive row hover tags and shapes
        self.hover_bindings = []

    def get_top_scores(self):
        """
        Fetches top scores from Supabase global leaderboard.
        Falls back to local sqlite runs database if offline.
        Returns a tuple of (list of scores, source_name_string).
        """
        scores = []
        source_name = "Global Archive [Supabase]"
        
        try:
            # Attempt to instantiate Supabase Leaderboard and query data
            lb = Leaderboard()
            scores = lb.get_top_scores(limit=10)
            
            # Check if we got back valid data
            if scores is None:
                raise ConnectionError("Supabase returned empty/no response.")
                
        except Exception as e:
            # Fallback to local SQLite runs
            print(f"Supabase connection failed, falling back to local SQLite. Error: {e}")
            try:
                db = Database()
                scores = db.get_local_top_scores(limit=10)
                db.close()
                source_name = "Local Terminal [SQLite]"
            except Exception as ex:
                print(f"Local database access failed: {ex}")
                scores = []
                source_name = "Offline Terminal [Unavailable]"
                
        return scores or [], source_name

    def draw_leaderboard(self, scores, source_name):
        """
        Clears the canvas and renders the leaderboard header, column labels,
        rows, percentages, progress bars, and navigation controls.
        """
        self.canvas.delete("all")
        
        # Title Header
        self.canvas.create_text(
            64.0, 98.71,
            anchor="nw",
            text="COS 102 · GROUP 1 · PAN-ATLANTIC UNIVERSITY · 2026",
            fill="#4A3820",
            font=("DM Mono", -9, "normal", "roman")
        )
        self.canvas.create_text(
            64.0, 130.0,
            anchor="nw",
            text="LEADERBOARD",
            fill=CREAM,
            font=("Playfair Display", -45, "bold", "roman")
        )
        
        # Display Connection Status Indicator
        status_color = EMBER if "SQLite" in source_name or "Unavailable" in source_name else "#2e7d32"
        self.canvas.create_rectangle(
            420, 142, 430, 152,
            fill=status_color, outline="",
        )
        self.canvas.create_text(
            440, 137,
            anchor="nw",
            text=source_name.upper(),
            fill=status_color,
            font=("DM Mono", -10, "bold")
        )
        
        # Subtitle
        self.canvas.create_text(
            64.0, 185.0,
            anchor="nw",
            text="Rankings of city survival runs. The city is saved through choices, and What Remains is measured.",
            fill=FOG,
            font=("DM Mono", -12, "normal", "italic")
        )
        
        # Refresh Button
        refresh_btn_bg = self.canvas.create_rectangle(
            946, 125, 1066, 160,
            fill="#1A0A00", outline=EMBER, width=1.5,
            tags="refresh_btn"
        )
        refresh_btn_text = self.canvas.create_text(
            1006, 142,
            text="REFRESH",
            fill=CREAM, font=("Courier", 10, "bold"),
            tags="refresh_btn"
        )
        
        self.canvas.tag_bind("refresh_btn", "<Button-1>", lambda e: self.update_ui())
        self.canvas.tag_bind("refresh_btn", "<Enter>", lambda e: self.canvas.itemconfig(refresh_btn_bg, fill=EMBER, outline=CREAM))
        self.canvas.tag_bind("refresh_btn", "<Leave>", lambda e: self.canvas.itemconfig(refresh_btn_bg, fill="#1A0A00", outline=EMBER))
        
        # Column Labels Header Row
        col_y = 230
        self.canvas.create_text(120, col_y, text="RANK", fill=EMBER, font=("Courier", 11, "bold"), anchor="w")
        self.canvas.create_text(220, col_y, text="PLAYER (USER)", fill=EMBER, font=("Courier", 11, "bold"), anchor="w")
        self.canvas.create_text(450, col_y, text="REAL NAME", fill=EMBER, font=("Courier", 11, "bold"), anchor="w")
        self.canvas.create_text(740, col_y, text="SCORE", fill=EMBER, font=("Courier", 11, "bold"), anchor="w")
        self.canvas.create_text(890, col_y, text="SURVIVAL %", fill=EMBER, font=("Courier", 11, "bold"), anchor="w")
        
        # Separator Line
        self.canvas.create_line(64, col_y + 18, 1066, col_y + 18, fill=DIM, width=1)
        
        # Renders the actual leaderboard rows
        start_y = 275
        row_height = 42
        
        if not scores:
            self.canvas.create_text(
                565, start_y + 100,
                text="No records found in database.",
                fill=DIM, font=("Courier", 14, "italic")
            )
        else:
            for idx, r in enumerate(scores):
                row_y = start_y + (idx * row_height)
                
                # Fetch row fields with safe defaults
                player_val = r.get("player_name", "Unknown")
                score_val = r.get("score", 0)
                real_name_val = get_real_name(player_val)
                
                # Treat score as percentage (constrained between 0 and 100)
                pct_val = max(0, min(100, int(score_val)))
                
                # Unique tags for row interactive effects
                tag = f"row_{idx}"
                
                # Background shape for high quality row separation
                bg_shape = self.canvas.create_rectangle(
                    64, row_y - 16, 1066, row_y + 20,
                    fill="#130D07", outline="#23170D", width=1,
                    tags=(tag, f"{tag}_bg")
                )
                
                # Distinct highlight text colors for top ranks
                rank_num = idx + 1
                if rank_num == 1:
                    rank_color = GOLD
                    rank_prefix = "★ "
                elif rank_num == 2:
                    rank_color = SILVER
                    rank_prefix = "✦ "
                elif rank_num == 3:
                    rank_color = BRONZE
                    rank_prefix = "✦ "
                else:
                    rank_color = CREAM
                    rank_prefix = "  "
                    
                # Rank Label
                self.canvas.create_text(
                    120, row_y,
                    text=f"{rank_prefix}{rank_num}",
                    fill=rank_color, font=("Courier", 11, "bold"),
                    anchor="w", tags=tag
                )
                
                # Player Username
                self.canvas.create_text(
                    220, row_y,
                    text=player_val,
                    fill=CREAM, font=("Courier", 11, "normal"),
                    anchor="w", tags=tag
                )
                
                # Real Name (Mapped from names.csv)
                self.canvas.create_text(
                    450, row_y,
                    text=real_name_val,
                    fill=FOG, font=("Courier", 11, "italic" if real_name_val == "N/A" else "normal"),
                    anchor="w", tags=tag
                )
                
                # Raw Score
                self.canvas.create_text(
                    740, row_y,
                    text=f"{score_val}",
                    fill=CREAM, font=("Courier", 11, "bold"),
                    anchor="w", tags=tag
                )
                
                # Visual percentage progress bar
                bar_x = 890
                bar_w = 80
                bar_h = 10
                
                # Progress bar container border
                self.canvas.create_rectangle(
                    bar_x, row_y - 5, bar_x + bar_w, row_y + 5,
                    fill="#1A0E05", outline=DIM, width=1,
                    tags=tag
                )
                # Filled progress representation block
                fill_w = int((pct_val / 100.0) * bar_w)
                if fill_w > 0:
                    self.canvas.create_rectangle(
                        bar_x + 1, row_y - 4, bar_x + fill_w - 1, row_y + 4,
                        fill=EMBER, outline="",
                        tags=tag
                    )
                
                # Percentage Text next to the bar
                self.canvas.create_text(
                    bar_x + bar_w + 12, row_y,
                    text=f"{pct_val}%",
                    fill=EMBER, font=("Courier", 11, "bold"),
                    anchor="w", tags=tag
                )
                
                # Setup Interactive bindings
                def make_enter_cb(bg_id=bg_shape):
                    return lambda event: self.canvas.itemconfig(bg_id, fill="#23170D", outline=EMBER)
                    
                def make_leave_cb(bg_id=bg_shape):
                    return lambda event: self.canvas.itemconfig(bg_id, fill="#130D07", outline="#23170D")
                
                self.canvas.tag_bind(tag, "<Enter>", make_enter_cb())
                self.canvas.tag_bind(tag, "<Leave>", make_leave_cb())

        # Draw a beautiful Back button on the Canvas
        back_btn_bg = self.canvas.create_rectangle(
            465, 720, 665, 765,
            fill="#1A0A00", outline=EMBER, width=1.5,
            tags="back_btn"
        )
        back_btn_text = self.canvas.create_text(
            565, 742,
            text="RETURN TO MENU",
            fill=CREAM, font=("Courier", 11, "bold"),
            tags="back_btn"
        )
        
        # Back Button bindings
        self.canvas.tag_bind("back_btn", "<Button-1>", lambda e: self.controller.show_frame("MainMenu"))
        self.canvas.tag_bind("back_btn", "<Enter>", lambda e: self.canvas.itemconfig(back_btn_bg, fill=EMBER, outline=CREAM))
        self.canvas.tag_bind("back_btn", "<Leave>", lambda e: self.canvas.itemconfig(back_btn_bg, fill="#1A0A00", outline=EMBER))

    def update_ui(self):
        """
        Invoked automatically when transitioning to this screen.
        Refreshes top scores from DB/Supabase and triggers canvas redraw.
        """
        scores, source_name = self.get_top_scores()
        self.draw_leaderboard(scores, source_name)
