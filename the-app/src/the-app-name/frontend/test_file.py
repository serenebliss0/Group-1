#remove these lines when main.py has been impl'd!
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #for now, since this isnt run from main

from backend.database import Database
from backend.database import Leaderboard

# create instances once when the app starts
db = Database()
lb = Leaderboard()

#create test entry
# save locally
run_id = db.save_run("Serenity", 80, 5, 120, "normal", "green")

# save to supabase
lb.submit_score("Serenity", 80, 5, 120)
lb.submit_score("Victor-bobo", 80, 5, 120)
lb.submit_score("Kene-bobo", 80, 5, 120)


run_id = db.save_run("Victorbobo", 80, 5, 120, "normal", "green")

