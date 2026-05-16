import json

#open up keybinds.json
with open("backend/keybinds.json", "r") as file:
    keybinds = json.load(file)

print(keybinds["move_up"])