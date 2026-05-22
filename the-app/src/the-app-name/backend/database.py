import sqlite3
import os
from dotenv import load_dotenv
from supabase import create_client
from .logger import get_logger 

logger = get_logger("Database")
load_dotenv()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "game.db")

class Database:
    def __init__(self):
        try:
            #creates or connects to a db. It will create one if game.db is not found
            self.conn = sqlite3.connect(DB_PATH) 
            self.conn.row_factory = sqlite3.Row  # lets you access columns by name instead of idx
            self._init_tables()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"DB Initialization failed: {e}")
    def _init_tables(self):
        """Create tables if they don't exist."""
        try:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    items_collected INTEGER DEFAULT 0,
                    time_played INTEGER DEFAULT 0,
                    difficulty TEXT DEFAULT 'normal',
                    ending TEXT,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS choices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    scenario INTEGER NOT NULL,
                    choice_key TEXT NOT NULL,
                    delta INTEGER NOT NULL,
                    FOREIGN KEY (run_id) REFERENCES runs(id)
                );
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit() #save changes, just like git commits 
            logger.info("Created user tables sucessfully")
        except Exception as e:
            logger.error(f"Failed to initialize tables: {e}")

    def save_run(self, player_name, score, items_collected, time_played, difficulty, ending):
        """Save a completed run and return its run_id."""
        try:
            cursor = self.conn.execute(
                """INSERT INTO runs (player_name, score, items_collected, time_played, difficulty, ending)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (player_name, score, items_collected, time_played, difficulty, ending)
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Attempt to save run failed: {e}")

    def save_choice(self, run_id, scenario, choice_key, delta):
        """Log a single choice made during a run."""
        try:
            self.conn.execute(
                "INSERT INTO choices (run_id, scenario, choice_key, delta) VALUES (?, ?, ?, ?)",
                (run_id, scenario, choice_key, delta)
            )
            self.conn.commit()
            logger.info("Saved user choice")
        except Exception as e:
            logger.error(f"Failed to save user choice: {e}")

    def get_local_top_scores(self, limit=10):
        """Fetch top scores from local db."""
        try:
            cursor = self.conn.execute(
                "SELECT player_name, score, items_collected, time_played, ending FROM runs ORDER BY score DESC LIMIT ?",
                (limit,) #the command expects a tuple, that's why I used it here
            )
            logger.info("Pulled user's best scores locally")
            return [dict(row) for row in cursor.fetchall()] or []
        
        except Exception as e:
            logger.error(f"Unable to fetch local top scores: {e}")

    def get_password_hash(self, username):
        """Retrieve the stored password hash of an existing user"""
        try:
            cursor = self.conn.execute(
                "SELECT password FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            return row["password"] if row else None
        except Exception as e:
            logger.error(f"Failed to get user's password hash from database: {e}")


    def get_run_choices(self, run_id):
        """Get all choices for a specific run."""
        try:
            cursor = self.conn.execute(
                "SELECT scenario, choice_key, delta FROM choices WHERE run_id = ? ORDER BY scenario",
                (run_id,)
            )
            return [dict(row) for row in cursor.fetchall()] or []
        except Exception as e:
            logger.error("Failed to receive choices from DB: {e}")
    
    def create_user(self, username, password):
            """Add a new user to the local sqlite database"""
            try:
                self.conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                self.conn.commit()
                logger.info("User creation successful")
                return True
            except sqlite3.IntegrityError:
                # This happens if the username already exists
                print(f"Database Error: Username '{username}' is already taken.")
                logger.error("User attempt to input a value that violates DB integrity")
                return False
            except Exception as e:
                logger.error(f"An unexpected database error occurred: {e}")
                return False

    def close(self):
        self.conn.close()
        logger.warning("The connection to the database was closed")



# Impl supabase global leaderboard

class Leaderboard:
    def __init__(self):

        url ="https://lyoccpevhprftrknyuzf.supabase.co"
        key="sb_publishable_BO21GbbCvdcinxSUCKkzNw_i9h75QFx"
        try:
            url = os.getenv("SUPABASE_URL", "https://lyoccpevhprftrknyuzf.supabase.co")
            key = os.getenv("SUPABASE_KEY", "sb_publishable_BO21GbbCvdcinxSUCKkzNw_i9h75QFx")
        except Exception as e:
            logger.error(f"Unable to retrieve api key from env. Do you have your keys in .env?\n{e}")
        
        try:
            self.supabase = create_client(url, key)
            self.table = "scores"
        except Exception as e:
            logger.error(f"Unable to connect to supabase db: {e}")

    def submit_score(self, player_name, score, items_collected, time_played):
        """Insert a completed run into the global leaderboard."""
        data = {
            "player_name": player_name,
            "score": score,
            "items_collected": items_collected,
            "time_played": time_played,
        }
        response = self.supabase.table(self.table).insert(data).execute()
        return response.data

    def get_top_scores(self, limit=10):
        """Fetch top scores ordered by score descending."""
        response = (
            self.supabase.table(self.table)
            .select("player_name, score, items_collected, time_played, created_at")
            .order("score", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data  # list of dicts

    def get_player_best(self, player_name):
        """Fetch a specific player's personal best."""
        response = (
            self.supabase.table(self.table)
            .select("score, items_collected, time_played, created_at")
            .eq("player_name", player_name)
            .order("score", desc=True)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None
