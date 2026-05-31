import csv
import os
from datetime import datetime

# ==================================
# TEXT-BASED ADVENTURE GAME WEEK 6
# The goal is to find the golden shell
# ==================================

DEBUG = True
RECORD_FILE = "waikiki_records.csv"

# ----------- Inventory ------------
inventory = []
max_items = 5

# ------------- Player -------------
player_health = 100
current_room = "beach"

# ------------- Rooms --------------
rooms = {
    "beach": {
        "description": "Warm sand, sunny skies, the perfect place to spend a day in Waikiki",
        "items": [
            {"name": "shovel", "type": "tool"},
            {"name": "sunscreen", "type": "protection"},
            {"name": "hot sand", "type": "danger"}
        ],
        "surrounding places": ["surf shop", "ocean", "beach bar"]
    },

    "surf shop": {
        "description": "A colorful store full of island keepsakes",
        "items": [
            {"name": "box", "type": "treasure"},
            {"name": "fan", "type": "protection", "uses": 1}
        ],
        "surrounding places": ["beach"]
    },

    "ocean": {
        "description": "Bright blue waters, refreshing to swim in the sun",
        "items": [
            {"name": "snorkel", "type": "tool"},
            {"name": "sea urchin", "type": "danger"}
        ],
        "surrounding places": ["beach"]
    },

    "beach bar": {
        "description": "A cool place to hang out and enjoy the beachfront view",
        "items": [
            {"name": "refreshing drink", "type": "protection"}
        ],
        "surrounding places": ["beach"]
    }
}

# -------- Record Functions --------

def save_record(name, result, score):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file_exists = os.path.exists(RECORD_FILE)

        with open(RECORD_FILE, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Name", "Timestamp", "Result", "Score"])

            writer.writerow([name, timestamp, result, score])

    except Exception as e:
        print("Error saving record:", e)


def show_leaderboard():

    try:

        if not os.path.exists(RECORD_FILE):
            return

        records = []

        with open(RECORD_FILE, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

        records.sort(
            key=lambda x: int(x["Score"]),
            reverse=True
        )

        print("\n===== LEADERBOARD =====")

        for position, record in enumerate(records, start=1):

            print(
                f"{position}. "
                f"{record['Name']} | "
                f"{record['Result']} | "
                f"{record['Score']} | "
                f"{record['Timestamp']}"
            )

    except Exception as e:
        print("Error loading leaderboard:", e)


# -------- Functions ---------

def show_help():
    print("""
Commands:
inventory
pickup <item>
drop <item>
use <item>
examine <item>
go to the <room>
look
help
quit
""")


def show_room():
    room = rooms[current_room]

    print("\n==", current_room.upper(), "==")
    print(room["description"])

    show_room_items()

    print("Surrounding places:", ", ".join(room["surrounding places"]))


def show_room_items():
    room = rooms[current_room]

    if not room["items"]:
        print("No items here.")
        return

    print("Items in the room:")
    for item in room["items"]:
        print("–", item["name"])


def show_inventory():
    if len(inventory) == 0:
        print("Your inventory is empty")
        return

    print("Inventory:")
    for item in inventory:
        print("–", item["name"], f"({item['type']})")


def pick_up(item_name):
    room = rooms[current_room]

    if len(inventory) >= max_items:
        print("Your inventory is full")
        return

    for item in room["items"]:
        if item["name"].lower() == item_name.lower():
            inventory.append(item)
            room["items"].remove(item)
            print(f"You picked up the {item_name}.")
            return

    print("This item is not found here")


def drop(item_name):
    room = rooms[current_room]

    for item in inventory:
        if item["name"].lower() == item_name.lower():
            inventory.remove(item)
            room["items"].append(item)
            print(f"You dropped the {item_name}.")
            return

    print("You don't have that item")


def examine(item_name):
    for item in inventory:
        if item["name"].lower() == item_name.lower():
            print(f"{item_name} is a {item['type']} item.")
            return

    for item in rooms[current_room]["items"]:
        if item["name"].lower() == item_name.lower():
            print(f"{item_name} is a {item['type']} item.")
            return

    print(" This item cannot be found here")


def use(item_name):
    global player_health

    for item in inventory:
        if item["name"].lower() == item_name.lower():

            if item["type"] == "protection":
                player_health += 20
                if player_health > 100:
                    player_health = 100

                print("You used it!")
                print("Health:", player_health)

                inventory.remove(item)
                return

            elif item["type"] == "treasure":
                print("You opened the box but it is empty")
                inventory.remove(item)
                return

            elif item["type"] == "danger":
                player_health -= 30
                print("Ouch!")
                print("Health:", player_health)

                if player_health <= 0:
                    print("Oh no, it seems you had a heatstroke, game over :(")

                    save_record(player_name, "LOSS", 0)
                    show_leaderboard()

                    quit()

                inventory.remove(item)
                return

            elif item["name"] == "shovel" and current_room == "beach":
                print("You dig in the sand but there is nothing")
                return

            elif item["name"] == "snorkel" and current_room == "ocean":
                print("You dive into the beautiful blue water...")
                print("Suddenly you see a shiny golden shell!")
                print("YOU WIN!")

                save_record(player_name, "WIN", player_health)
                show_leaderboard()

                quit()

            else:
                print("You can't use that here")
                return

    print("You don't have that item")


def move(room_name):
    global current_room

    if room_name in rooms[current_room]["surrounding places"]:
        current_room = room_name
        show_room()
    else:
        print("You can't go there")


player_name = input("Enter your name: ")

if DEBUG:

    debug_choice = input("Run debug mode? (yes/no): ").lower()

    if debug_choice == "yes":

        save_record(
            player_name,
            "DEBUG",
            100
        )

        show_leaderboard()

        quit()

# ------------- Game start --------------

print("Aloha! Welcome to Waikiki beach!")
print("Somewhere around here is a golden shell. It is your goal to find it!")
show_help()
show_room()

# ------------ Main loop --------------

while True:

    command = input("\n> ").lower().split()

    if len(command) == 0:
        continue

    action = command[0]

    if action == "inventory":
        show_inventory()

    elif action == "pickup":
        if len(command) < 2:
            print("Pick up what?")
        else:
            item_name = " ".join(command[1:])
            pick_up(item_name)

    elif action == "drop":
        if len(command) < 2:
            print("Drop what?")
        else:
            item_name = " ".join(command[1:])
            drop(item_name)

    elif action == "use":
        if len(command) < 2:
            print("Use what?")
        else:
            item_name = " ".join(command[1:])
            use(item_name)

    elif action == "examine":
        if len(command) < 2:
            print("Examine what?")
        else:
            item_name = " ".join(command[1:])
            examine(item_name)

    elif action == "go":
        if len(command) < 4:
            print("Go where? Try: go to the beach")
        else:
            room_name = " ".join(command[3:])
            move(room_name)

    elif action == "look":
        show_room()

    elif action == "help":
        show_help()

    elif action == "quit":
        print("Thanks for playing!")
        break

    else:
        print("Unknown command")