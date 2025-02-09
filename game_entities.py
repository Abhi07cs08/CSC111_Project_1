"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: The unique identifier for the location.
        - brief_description: A short description of the location, shown on subsequent visits.
        - long_description: A detailed description of the location, shown on the first visit or when 'look' is used.
        - available_commands: A dictionary mapping valid movement commands (e.g., 'go east') to destination location IDs.
        - items: A list of items currently present in the location.
        - visited: A boolean indicating whether the player has visited this location before.


    Representation Invariants:
        - id_num must be unique for each location.
        - available_commands keys must be valid movement directions ('go north', 'go south', 'go east', 'go west').
        - items must contain only valid item names that exist in the game's item list.
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        The location is initialized with a unique ID, descriptions, available commands, items, and a visited flag.
        The brief description is used for subsequent visits, while the long description is shown on the first visit
        or when the player uses the 'look' command. Available commands define where the player can move from this
        location, and items list the objects present in this location.
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item.
        - start_position: The ID of the location where the item is initially found.
        - target_position: The ID of the location where the item needs to be delivered to score points.
        - target_points: The number of points awarded when the item is delivered to its target position.

    Representation Invariants:
        - start_position >= 0
        - target_position >= 0
        - target_points >= 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str  # The name of the item, e.g., "lucky mug", "USB drive".
    start_position: int  # The location ID where the item starts in the game.
    target_position: int  # The location ID where the item should be delivered.
    target_points: int  # The number of points awarded when the item is delivered to the target position.



# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
