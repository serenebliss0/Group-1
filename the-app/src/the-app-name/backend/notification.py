from plyer import notification
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets" / "images"
icon_path = BASE_DIR / "assets" / "images" / "mynd_logo.ico"

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="What Remains?",
        app_icon=icon_path,
        timeout=5
    )



if __name__ == '__main__':
    send_notification(
        "Eco Alert",
        "You recycled 5 bottles!"
    )