"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - # TODO add descriptions of public instance attributes as needed

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.current_inventory = [] #inintialise inventory
        self.event_log = EventList()  # Initialize event log to track game events

        
    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'], item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            return self.current_location_id
        else:
            return self._locations[loc_id]

    def pick_up_item(self, item_name: str) -> None:
        """
        Pick up an item from the current location and add it to the inventory.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.pick_up_item('lucky mug')
        You have picked up the lucky mug.

        >>> game.pick_up_item('nonexistent item')
        There is no such item here.
        """
        if item_name in self._locations[self.current_location_id].items:
            self.current_inventory.append(item_name)
            return
        else:
            print("There is no such item here.")
            return

    def drop_item(self, item_name: str) -> None:
        """
        Drop an item from the inventory at the current location.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.pick_up_item('lucky mug')
        You have picked up the lucky mug.
        >>> game.drop_item('lucky mug')
        You have dropped the lucky mug.

        >>> game.drop_item('nonexistent item')
        You don't have that item in your inventory.
        """
        if item_name in self.current_inventory:
            self.current_inventory.remove(item_name)
            return
        else:
            print("You don't have that item in your inventory.")
            return

    def look(self) -> None:
        """
        Display the full description of the current location.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.look()
        LOCATION 1: You are at the waterfilling station where students usually stop to refill their bottles. Today, it's eerily quiet except for the occasional drip from the faucet. A faint glimmer of your lucky mug catches your eye.

        >>> game.move("go east")
        >>> game.look()
        LOCATION 2: You stand at the common entrance of Robarts Library. The doors creak as students shuffle in and out. Flyers litter the ground, and you feel the pressure of looming deadlines in the air.

        """
        current_location = self.current_location_id
        print(f"LOCATION {current_location}: {self._locations[current_location].long_description}")
        return

    def inventory(self) -> None:
        """
        Display the items currently in the player's inventory.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.pick_up_item('lucky mug')
        >>> game.inventory()
        Inventory: lucky mug
        """
        print(f"Inventory: {self.current_inventory}")
        return

    def score(self) -> None:
        """
        Calculate and Display the player's current score.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.pick_up_item('lucky mug')
        >>> game.score()
        Your current inventory score is: 10
        """
        player_score = 0
        for item in self.current_inventory:
            score = self._items[item].target_points
            player_score += score
        return player_score
    
    def undo(self) -> None:
        """
        Undo the last action and revert the game state to the previous event.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.move("go east")
        >>> game.undo()
        Last action undone. Returned to the waterfilling station.
        """
        if self.event_log.is_empty() or self.event_log.first == self.event_log.last:
            print("No actions to undo.")
            return
        
        self.event_log.remove_last_event()

        if self.event_log.last:
            self.current_location = self._locations[self.event_log.last.id_num]
            print(f"Last action undone. Returned to {self.current_location.name}.")
        else:
            print("You are back at the starting location.")


    def log(self) -> None:
        """
        Display a chronological list of all events (locations visited, commands chosen).

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.move("go east")
        >>> game.move("go east")
        >>> game.log()
        Location: 1, Command: None
        Location: 2, Command: go east
        Location: 3, Command: go east
        """
        self.event_log.display_events()

    def quit(self) -> None:
        """
        Quit the game.

        >>> game = AdventureGame('game_data.json', 1)
        >>> game.quit()
        Game has been quit.
        """
        print("Game has been quit.")
        exit()

    # Add any other necessary methods here to support the above functionalities.




if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 9)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
