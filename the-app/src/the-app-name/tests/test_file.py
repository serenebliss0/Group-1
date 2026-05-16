import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import Database

# ── Local DB tests only — no Supabase in CI ──

def test_database_initializes():
    db = Database()
    assert db.conn is not None
    db.close()

def test_save_run_returns_id():
    db = Database()
    run_id = db.save_run("test_user", 80, 5, 120, "normal", "green")
    assert isinstance(run_id, int)
    assert run_id > 0
    db.close()

def test_get_top_scores_returns_list():
    db = Database()
    scores = db.get_local_top_scores()
    assert isinstance(scores, list)
    db.close()

def test_save_and_retrieve_run():
    db = Database()
    db.save_run("pytest_runner", 95, 8, 200, "hard", "green")
    scores = db.get_local_top_scores()
    assert scores is not None
    assert isinstance(scores, list)
    names = [s["player_name"] for s in scores]
    assert "pytest_runner" in names
    db.close()

def test_save_choice():
    db = Database()
    run_id = db.save_run("choice_tester", 60, 3, 90, "normal", "ruin")
    assert run_id is not None
    db.save_choice(run_id, 1, "A", -20)
    choices = db.get_run_choices(run_id)
    assert choices is not None
    assert len(choices) == 1
    assert choices[0]["choice_key"] == "A"
    db.close()