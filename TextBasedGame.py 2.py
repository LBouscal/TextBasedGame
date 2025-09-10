# TextBasedGame.py
# Author: Layshla Bouscal
# Description: Text-based haunted mansion adventure game for SNHU IT-140.
# The player must collect all 6 relics before facing the villain in the attic to win.

def show_instructions():
    """Display the game's instructions and available commands."""
    print("""
    Haunted Mansion Text Adventure
    Lightning crackles. The door slams shut behind you. You are trapped in Mistress Elira’s cursed mansion.
    Your only hope: collect all 6 ancient relics before she claims your soul...

    Commands:
      go north | go south | go east | go west
      get [item name]
      map
      exit
    """)

def show_map():
    """Display a simple ASCII map for visualizing the mansion."""
    print("""
          [Library]
              |
          [Foyer]---[Dining Room]---[Guest Room]---[Chapel]---[Attic]
             |              |
        [Basement]   [Conservatory]
    """)
    print("Rooms with relics will reveal themselves as you explore.\n")

# Room descriptions shown upon entering each location
room_descriptions = {
    'Foyer': "Thunder shakes the mansion as the door slams shut behind you. The haunted foyer is thick with dread.",
    'Library': "Cobwebbed shelves and flickering candlelight reveal the cursed mirror glinting in the gloom.",
    'Dining Room': "Dusty china, overturned chairs, and a whisper of cold air greet you in the ruined dining room.",
    'Conservatory': "Twisted plants and cracked windows tangle the conservatory in shadows and silver moonlight.",
    'Guest Room': "A faded portrait stares at you with hollow eyes—the ghost locket glimmers atop the pillow.",
    'Chapel': "Crumbling pews and melted wax hint at ancient rituals. A sacred candle burns with an eerie blue flame.",
    'Basement': "Each step creaks louder than the last. A protective amulet lies half-buried in the dirt.",
    'Attic': "Cobwebs thicken. Mistress Elira’s chilling presence presses close—the air is heavy with doom."
}

# Item descriptions shown when the player finds an item in a room
item_descriptions = {
    'Cursed Mirror': "A mirror with a cracked frame shivers as you approach, your reflection warped by shadows.",
    'Spell Book': "A dusty tome, its pages fluttering as if caught in a phantom breeze, rests on the table.",
    'Silver Dagger': "A silver dagger gleams with an unnatural light, its blade cold as ice.",
    'Ghost Locket': "A locket floats inches above the pillow, glowing with a pale, spectral light.",
    'Sacred Candle': "A candle burns with blue flame, filling the chapel with an ancient, spicy scent.",
    'Protective Amulet': "A weathered amulet hums quietly in the gloom—your only defense against Elira’s wrath."
}

# The mansion layout and which item is found in which room
rooms = {
    'Foyer': {
        'North': 'Library',
        'East': 'Dining Room',
        'South': 'Basement'
    },
    'Library': {
        'South': 'Foyer',
        'East': 'Conservatory',
        'item': 'Cursed Mirror'
    },
    'Dining Room': {
        'West': 'Foyer',
        'East': 'Guest Room',
        'item': 'Spell Book'
    },
    'Conservatory': {
        'West': 'Library',
        'South': 'Guest Room',
        'item': 'Silver Dagger'
    },
    'Guest Room': {
        'West': 'Dining Room',
        'North': 'Conservatory',
        'East': 'Chapel',
        'item': 'Ghost Locket'
    },
    'Chapel': {
        'West': 'Guest Room',
        'South': 'Attic',
        'item': 'Sacred Candle'
    },
    'Basement': {
        'North': 'Foyer',
        'item': 'Protective Amulet'
    },
    'Attic': {
        'North': 'Chapel'
    }
}

# Dictionary to track which room each item is originally found in
item_locations = {
    'Cursed Mirror': 'Library',
    'Spell Book': 'Dining Room',
    'Silver Dagger': 'Conservatory',
    'Ghost Locket': 'Guest Room',
    'Sacred Candle': 'Chapel',
    'Protective Amulet': 'Basement'
}

def check_rooms(rooms_dict):
    """Checks if all exits in the mansion layout point to real rooms."""
    room_names = set(rooms_dict.keys())
    error_found = False
    for room, details in rooms_dict.items():
        for direction in ['North', 'South', 'East', 'West']:
            target = details.get(direction)
            if target and target not in room_names:
                print(f"Error: {room} -> {direction} points to undefined room: {target}")
                error_found = True
    if not error_found:
        print("Room dictionary integrity check: PASSED. All exits lead to real rooms.\n")

def show_status(current_room, inventory, rooms_dict):
    """
    Show the player's current room name, description, inventory,
    missing relics, each exit with its direction and destination,
    and any collectible item in the room.
    """
    print('-' * 60)
    print(f"You are in the {current_room}.")
    print(room_descriptions.get(current_room, ''))
    print(f'Inventory: {inventory}')

    # Show missing relics
    all_items = set(item_locations.keys())
    missing_items = all_items - set(inventory)
    if missing_items:
        # Extra flavor if only one missing!
        if len(missing_items) == 1:
            print(f"You're almost there! Only one relic remains: {list(missing_items)[0]}")
        else:
            print(f"Missing Relics: {sorted(list(missing_items))}")
    else:
        print("You have collected all the relics! Head to the Attic!")

    # Show available exits for the current room, including destination
    exits = [(direction, rooms_dict[current_room][direction])
             for direction in ['North', 'South', 'East', 'West']
             if direction in rooms_dict[current_room]]
    if exits:
        print("Exits:")
        for direction, destination in exits:
            print(f"  {direction}: leads to the {destination}")
    else:
        print("Exits: None")

    # Show collectible item if present and not already collected
    item = rooms_dict[current_room].get('item')
    if item and item not in inventory:
        print(f"\n{item_descriptions.get(item, 'You see ' + item + ' here.')}")
        print(f"Type: get {item.lower()}  to claim it.")
    print('-' * 60)

def move_room(current_room, direction, rooms_dict):
    """Move to a new room if the direction is valid; otherwise, stay in the current room."""
    direction = direction.strip().capitalize()
    if direction in rooms_dict[current_room]:
        return rooms_dict[current_room][direction]
    else:
        print("A cold wind howls—there’s no path that way.")
        return current_room

def main():
    # Run the room dictionary check before starting the game
    check_rooms(rooms)
    inventory = []  # Tracks which relics the player has collected
    current_room = 'Foyer'  # Player starts in the Foyer
    show_instructions()  # Show instructions at game start

    # Main gameplay loop
    while True:
        show_status(current_room, inventory, rooms)

        # End game conditions: player enters attic
        if current_room == 'Attic':
            if len(inventory) == 6:
                print("\nThe relics pulse with ghostly light! Mistress Elira screams and dissolves into mist.")
                print("The portal opens—you stagger free, soul intact. You survived the haunted mansion!")
            else:
                print("\nMistress Elira’s laughter echoes as darkness closes in...")
                print("Your soul is lost to the mansion forever. Game over.")
            break  # End the game after win/loss message

        command = input("Enter your move: ").strip().lower()

        if command == 'exit':
            # Show possible exits and where they lead before exiting
            exits = [(direction, rooms[current_room][direction])
                     for direction in ['North', 'South', 'East', 'West']
                     if direction in rooms[current_room]]
            if exits:
                print("\nIf you continued, you could have gone:")
                for direction, destination in exits:
                    print(f"  {direction}: to the {destination}")
            print("\nYou close your eyes, wishing this was all a nightmare. Thanks for playing.")
            break
        elif command == 'map':
            show_map()
        elif command.startswith('go '):
            # Handle movement command
            direction = command[3:]
            current_room = move_room(current_room, direction, rooms)
        elif command.startswith('get '):
            # Handle item pickup command
            item = rooms[current_room].get('item')
            requested = command[4:].strip().lower()
            if item and item.lower() == requested and item not in inventory:
                inventory.append(item)
                print(f"\nYou claim the {item}. A chill passes through you—was that a whisper of approval or warning?")
            elif item and item in inventory:
                # Tell player where they found the item
                location = item_locations.get(item, 'somewhere mysterious')
                print(f"You already claimed the {item}. You found it in the {location}.")
            else:
                print("There’s nothing like that here. The shadows mock your mistake.")
        else:
            print("The spirits do not understand your words. Try another command...")

    print("\nA final echo of thunder rolls through the haunted halls. Game over.")

# Program entry point
if __name__ == '__main__':
    main()