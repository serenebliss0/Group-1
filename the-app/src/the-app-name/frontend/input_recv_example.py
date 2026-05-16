import json
import tkinter as tk

with open("backend/keybinds.json", "r") as file:
    keybinds = json.load(file)

player_x = 100
player_y = 100

root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

player = canvas.create_rectangle(
    player_x,
    player_y,
    player_x + 50,
    player_y + 50
)

def move_player(event):
    global player_x, player_y

    key = event.keysym.lower()

    if key == keybinds["move_up"]:
        player_y -= 10

    elif key == keybinds["move_down"]:
        player_y += 10

    elif key == keybinds["move_left"]:
        player_x -= 10

    elif key == keybinds["move_right"]:
        player_x += 10

    elif key == keybinds["interact"]:
        canvas.itemconfig(player, fill="red")

    canvas.coords(
        player,
        player_x,
        player_y,
        player_x + 50,
        player_y + 50
    )

root.bind("<KeyPress>", move_player)

root.mainloop()