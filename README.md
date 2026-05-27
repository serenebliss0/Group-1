# What Remains?

> *"It's ugly, isn't it?"*
> *Keep looking.*

**What Remains?** is a psychological narrative game about perception, waste, and becoming. You play as a citizen of a city making environmental decisions. Until you realize you are not a citizen at all.

Inspired by an untitled scrap metal bull sculpture at the **Yemisi Shyllon Museum of Art, Pan-Atlantic University, Lagos**. A creature built entirely from discarded electronics that somehow became something alive.

Built for **COS 102: Introduction to Problem Solving**, Pan-Atlantic University, 2025/2026.

---

## The Game

The city is dying. You make choices. The choices have weight.

There are three endings.
The ending you get depends on how you treated the city.

---

## Tech Stack

| Layer | Tool |
| --- | --- |
| Language | Python 3.11 |
| GUI | Tkinter |
| Local database | SQLite via `sqlite3` |
| Global leaderboard | Supabase |
| Audio and Input Handling | pygame-ce |
| Image handling | Pillow |
| Auth | bcrypt |
| Environment | python-dotenv |
| Design | Figma |
| Internal File Handlers | pathlib, sys |
| Version control | Git + GitHub |
| Keybinds | JSON |
| Log Handlers | RotatingFileHandler |
| User Env Variables | getpass, os, sys |
| Github Workflow | pylint, pytest |
| Installer | pyinstaller, Inno Setup |


---

## Project Structure

```
Group-1/
├── the-app/
│   └── src/
│       └── the-app-name/
│           ├── main.py                      # App entry point (Tkinter controller)
│           ├── app.py
│           ├── runtime_paths.py
│           ├── settings.json
│
│           ├── backend/
│           │   ├── audio.py                 # Game audio system
│           │   ├── database.py              # SQLite + Supabase sync
│           │   ├── data_handler.py
│           │   ├── events.py
│           │   ├── game_state.py
│           │   ├── input_manager.py
│           │   ├── keybinds.json
│           │   ├── logger.py                # Central logging system
│           │   ├── logic.py                 # Core game logic + flow control
│           │   ├── login_handler.py
│           │   ├── map_renderer.py
│           │   ├── runtime_paths.py
│           │   ├── save_data.json
│           │   ├── scenarios.json
│           │   ├── session.py
│           │   ├── session.json
│           │   ├── settings.json
│           │   ├── settings_handler.py
│           │   ├── signup_handler.py
│           │   ├── theme.py
│           │   ├── world.py
│           │   └── saves/
│           │       └── serenebliss0.json
│
│           ├── frontend/
│           │   ├── splash.py
│           │   ├── login.py
│           │   ├── signup.py
│           │   ├── main_menu.py
│           │   ├── menu.py
│           │   ├── settings.py
│           │   ├── leaderboard_screen.py
│           │   ├── game_screen.py
│           │   ├── scene1.py
│           │   ├── scene2.py              
│           │   ├── act1.py
│           │   ├── prelude1.py
│           │   ├── prelude2.py
│           │   ├── prelude3.py
│           │   ├── prelude4.py
│           │   ├── prelude5.py
│           │   ├── ending_screen.py
│           │   ├── end_screen.py
│           │   ├── game_over.py
│           │   ├── win_screen.py
│           │   ├── pause.py
│           │   ├── pause_menu.py
│           │   ├── dialogue.py
│           │   ├── dialogue_overlay.py
│           │   ├── tutorial_overlay.py
│           │   ├── typewriter.py
│           │   ├── runtime_paths.py
│           │   ├── input_recv_example.py
│           │   ├── scenarios.json         # duplicated runtime copy (bundled)
│           │   └── __init__.py
│
│           ├── assets/
│           │   ├── scenarios.json
│           │   ├── scenarios.csv
│           │   ├── images/
│           │   │   ├── map.png
│           │   │   ├── factory_fixed.png
│           │   │   ├── player.png
│           │   │   ├── splash.png
│           │   │   ├── main_menu assets...
│           │   │   └── icons...
│           │   ├── fonts/
│           │   └── sounds/
│           │       └── demo_intro.wav
│
│           ├── logs/
│           │   ├── app_debug.log
│           │   └── game.log
│
│           ├── main.py.cpython-314.pyc    # (IGNORE - build artifact)
│           └── app.py.cpython-314.pyc     # (IGNORE - build artifact)
│
├── tests/
│   └── test_database.py
│
├── requirements.txt
├── scenarios.csv
└── .github/
    └── workflows/
        └── python-ci.yml
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installer
[Check out the Releases tab](https://github.com/serenebliss0/Group-1/releases)

### Manual Installation

```bash
# Clone the repo
git clone https://github.com/serenebliss0/Group-1.git
cd Group-1

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```



### Running the Game

```bash
cd the-app/src/the-app-name
python main.py
```

### Running Tests

```bash
pytest tests/ -v
```

---

## Team — Group 1

| Name | Role | Owns |
| --- | --- | --- |
| Oluwasemire Ajayi | Backend Lead, Frontend, DB, Figma | `database.py`, `login_handler.py`, `scene.py`, `splash.py`, `signup_handler.py`, `logic.py`, `input_handler.py` |
| Joseph Nnabueze | Backend, Figma | `end_screen.py` |
| Chianugo Onyia | Frontend, Database | `menu.py`, `memory.py` , `scene2.py`|
| Chimdike Agugoesi | Frontend, Figma Lead | `splash.py`, `act_intro.py` , `Leaderboard.py`|
| Marvelous Moses-Okorie | Database, Frontend | `leaderboard_screen.py`, local score display, `prologue.py` |
| Osinachi Justin-Sonde | Assets, Settings | `settings.py`, keybind reader |
| Kamsiyochi Ekenulo | Assets, Audio | Asset loader, sound manager, `logic.py` |

---

## Supervisors

| Supervisor 1 | Supervisor 2 |
| --- | --- |
| Chukwudi Ofoma | Pascal Iloba |

---

## Submission

- **Deadline:** Sunday, 24 May 2026 — 11:59 PM
- **GitHub:** this repository
- **Figma:** [Figma Design](https://www.figma.com/team_invite/redeem/1S6kFAwjXLnyI9cwW9bfLz?t=BlFt4Gxj9DvQ7M5h-21)
- **One-page summary:** [One Page Word doc](https://github.com/serenebliss0/Group-1/blob/main/what-remains-one-pager.docx)

---
