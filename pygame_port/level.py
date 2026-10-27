"""Loads a level from a .map file."""

from pathlib import Path

# __file__ is the location of this file (level.py). Going up two steps with
# .parent.parent gives the main project folder, where level1.map,
# level2.map and the font folder live.
PROJECT_FOLDER: Path = Path(__file__).parent.parent

# What each number in a .map file means.
EMPTY: int = 0
BLOCK: int = 1
SPIKE: int = 2
GOAL: int = 3

# Each tile is a 16 x 16 square in the game world.
TILE_SIZE: int = 16


class Level:
    """A grid of tiles, like a sheet of squared paper.

    self.tiles is a list of rows, and each row is a list of numbers.
    So self.tiles[2][5] is the tile in row 2, column 5 (counting from 0).
    """

    def __init__(self, level_number: int) -> None:
        # level_number starts at 0, but the files are named level1.map, level2.map, ...
        # The f before the quotes lets us put a value inside {} into the text.
        file_path: Path = PROJECT_FOLDER / f"level{level_number + 1}.map"

        # A .map file is just numbers separated by spaces and new lines.
        # The first two numbers are the width and height; the rest are the tiles, row by row.
        numbers: list[int] = []
        for word in file_path.read_text().split():
            numbers.append(int(word))

        self.width: int = numbers[0]      # number of columns
        self.height: int = numbers[1]     # number of rows
        tile_numbers: list[int] = numbers[2:]

        # "list[list[int]]" means a list of lists of whole numbers: a grid.
        self.tiles: list[list[int]] = []
        for row in range(self.height):
            row_of_tiles: list[int] = []
            for column in range(self.width):
                position_in_file: int = row * self.width + column
                if position_in_file < len(tile_numbers):
                    row_of_tiles.append(tile_numbers[position_in_file])
                else:
                    # If the file is missing some numbers, treat those tiles as empty.
                    row_of_tiles.append(EMPTY)
            self.tiles.append(row_of_tiles)

    def get_tile(self, column: int, row: int) -> int:
        """Return the tile at this grid position. Anywhere outside the map counts as empty."""
        if column < 0 or column >= self.width:
            return EMPTY
        if row < 0 or row >= self.height:
            return EMPTY
        return self.tiles[row][column]
