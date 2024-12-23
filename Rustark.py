# g = unpowered generator
# G = powered generator
# * = undiscovered space. it is dark without the power. every space you move to illuminates 4 squares around you, and adds the discovered spaces to the map
# c = crate. once unlocked you can take stuff in/out
# ! = player
# h = hints that are scattered around

# commands: help, move, solve, read, exit


# find a flashlight that makes you see 9 squares instead

# started writing Player.move()

class Player:
    """
    Represents a player in a Rustark game.
    Has an inventory list, achievements list, position in list form [row, col], and letter.
    """
    def __init__(self):
        self._inventory = []
        self._achievements = []
        self._position = [0, 9]
        self._letter = "!"

    def get_inventory(self):
        """Returns the player's inventory."""
        return self._inventory

    def get_achievements(self):
        """Returns the player's achievements."""
        return self._achievements

    def get_position(self):
        """Returns the player's position."""
        return self._position

    def get_letter(self):
        """Returns letter"""
        return self._letter

    def move(self, game, map, new_pos):
        """
        Moves the player to the given position ([row, col]) and returns True if the move is possible.
        Otherwise, returns False.
        """
        if new_pos in game.find_adjacent_pos(self._position):  # new_pos is adjacent to player
            if type(map[new_pos[1]][new_pos[0]]) is Empty:  # new_pos is empty
                self._position = new_pos
                return True
        return False


class Item:
    """
    Represents an item found in a Crate within a Rustark game.
    Has a name (str).
    """
    def __init__(self, name):
        self._name = name

    def get_name(self):
        """Returns the item's name."""
        return self._name


class Generator:
    """
    Represents a generator in a Rustark game.
    Has boolean isPowered, position in list form [row, col], boolean isFound, and letter.
    """
    def __init__(self, pos, found):
        self._isPowered = False
        self._position = pos
        self._isFound = found
        self._letter = "g"

    def get_is_powered(self):
        """Returns True if the generator is powered, and False otherwise."""
        return self._isPowered

    def get_position(self):
        """Returns the generator's position."""
        return self._position

    def get_is_found(self):
        """Returns True if the generator has been found, and False otherwise."""
        return self._isFound

    def get_letter(self):
        """Returns letter"""
        return self._letter


class Crate:
    """
    Represents a crate in a Rustark game.
    Has contents list, position in list form [row, col], boolean isFound, and letter.
    """
    def __init__(self, contents, pos, found):
        self._contents = contents
        self._position = pos
        self._isFound = found
        self._letter = "c"

    def get_contents(self):
        """Returns the crate's contents."""
        return self._contents

    def get_position(self):
        """Returns the crate's position."""
        return self._position

    def get_is_found(self):
        """Returns True if the crate has been found, False otherwise."""

    def get_letter(self):
        """Returns letter"""
        return self._letter


class Hint:
    """
    Represents a hint in a Rustark game.
    Has text (str), position in list form [row, col], boolean isFound, and letter.
    """
    def __init__(self, text, pos, found):
        self._text = text
        self._position = pos
        self._isFound = found
        self._letter = "h"

    def get_text(self):
        """Returns the hint's text"""
        return self._text

    def get_position(self):
        """Returns the hint's position."""
        return self._position

    def get_is_found(self):
        """Returns True if the hint has been found, False otherwise"""

    def get_letter(self):
        """Returns letter"""
        return self._letter


class Empty:
    """
    Represents an empty space in a Map.
    Has a letter and boolean isFound.
    """
    def __init__(self, found):
        self._letter = "-"
        self._isFound = found

    def get_letter(self):
        """Returns letter"""
        return self._letter

    def get_is_found(self):
        """Returns True if the space has been found, otherwise False."""
        return self._isFound


class Achievement:
    """
    Represents an achievement in a Rustark game.
    Has a boolean isAchieved, title (str), and description (str).
    """
    def __init__(self, title, desc):
        self._isAchieved = False
        self._title = title
        self._description = desc

    def get_is_achieved(self):
        """Returns True if the achievement has been achieved, and False otherwise."""
        return self._isAchieved

    def get_title(self):
        """Returns the achievement's title."""
        return self._title

    def get_description(self):
        """Returns the achievement's description."""
        return self._description


class Map:
    """
    Represents a map in a Rustark game.
    Has a map (list of lists).
    """
    def __init__(self):
        # initialize to empty map
        self._game_map = []
        for x in range(10):
            row = []
            for y in range(10):
                row.append(Empty(False))
            self._game_map.append(row)

    def get_map(self):
        """Returns the map"""
        return self._game_map

    def get_object_by_position(self, pos):
        """Returns the object at a given position in form [row, col]"""
        return self._game_map[pos[1]][pos[0]]

    def add_object(self, obj, pos):
        """Adds a given object to the given position (list form [row, col]) on the map"""
        self._game_map[pos[1]][pos[0]] = obj

    def remove_object(self, pos):
        """Replaces the object at the given position ([row, col]) with an Empty object."""
        self._game_map[pos[1]][pos[0]] = Empty(True)

class Rustark:
    """
    Represents a game of Rustark.
    Has a player and various related objects.
    """
    def __init__(self):
        self._player = Player()
        self._game_map = Map()

        self.initialize_map()

    def get_player(self):
        """Returns the player."""
        return self._player

    def get_map(self):
        """Returns the map."""
        return self._game_map.get_map()

    def initialize_map(self):
        """Adds necessary objects to map"""
        game_map = self._game_map

        # add player
        game_map.add_object(self._player, [0, 9])

        # add generators
        game_map.add_object(Generator([0, 7], False), [0, 7])
        game_map.add_object(Generator([8, 5], False), [8, 5])
        game_map.add_object(Generator([1, 1], False), [1, 1])

        # add hints
        game_map.add_object(Hint("oh no! one of the wires for the generator ahead is broken. I wonder which one...", [0, 8], True), [0, 8])

        # add crates
        game_map.add_object(Crate([Item("wire")], [1, 8], True), [1, 8])

    @staticmethod
    def find_adjacent_pos(pos):
        """Returns a list of lists of board positions adjacent to the player's current position."""
        pos_list = []
        potential_pos = [[pos[0] + 1, pos[1] + 1],  # diagonal moves
                         [pos[0] - 1, pos[1] - 1],
                         [pos[0] + 1, pos[1] - 1],
                         [pos[0] - 1, pos[1] + 1],
                         [pos[0] + 1, pos[1]],  # straight moves
                         [pos[0] - 1, pos[1]],
                         [pos[0], pos[1] - 1],
                         [pos[0], pos[1] + 1]]

        for pos in potential_pos:
            if 0 <= pos[0] <= 9 and 0 <= pos[1] <= 9:
                pos_list.append(pos)

        return pos_list

    def make_move(self, new_pos):
        """Takes a new_pos list in form [row, col] and implements the consequences if possible."""
        prev_pos = self._player.get_position()
        if self._player.move(self, self.get_map(), new_pos) is True:  # new_pos is empty and in range
            self._game_map.add_object(self._player, new_pos)
            self._game_map.remove_object(prev_pos)

    def interact(self, item_letter):
        """
        Interacts with an item (if possible) given its letter and implements the consequences.
        Returns False if not possible, otherwise returns data relevant to interaction.
        """
        in_range_positions = self.find_adjacent_pos(self._player.get_position())
        interactables_dict = {}
        for pos in in_range_positions:
            interactable = self.get_map()[pos[1]][pos[0]]
            letter = interactable.get_letter()
            if letter != "-":
                interactables_dict[letter] = interactable

        if item_letter in interactables_dict:
            if item_letter == "h":
                return interactables_dict["h"].get_text()
            elif item_letter == "c":
                return "crate"
            elif item_letter == "g":
                return "generator, unpowered"
            elif item_letter == "G":
                return "generator, powered"
        return False

    def display_map(self):
        """Prints the map according to what the player has discovered."""
        row_count = 0
        for row in self.get_map():
            col_count = 0
            row_str = "[ "

            for col in row:
                if col_count == 9:
                    row_str += f"{col.get_letter()} "
                else:
                    row_str += f"{col.get_letter()}  "
                col_count += 1
            print(f"{row_str}] {row_count}")
            row_count += 1
        print("  0  1  2  3  4  5  6  7  8  9")

    def display_situation(self):
        """Prints the current situation based on where the player is located on the map."""
        pos = self._player.get_position()
        current_space = self._game_map.get_object_by_position(pos)
        letter = current_space.get_letter()

        print(f"You are at {pos}.")
        if letter == "!":
            print("Nothing to see here...")
        elif letter == "h":
            print(f"A faded paper reads: {current_space.get_text()}")


def main():
    game = Rustark()
    game.display_map()
    game.make_move([1, 9])

    game.display_map()
    print(game.interact("h"))

    # game.display_situation()


if __name__ == "__main__":
    main()
