from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TILE_EMPTY = 0
TILE_SOLID = 1
TILE_SPIKE = 2
TILE_GOAL = 3


class Level:
    def __init__(self, level_index):
        path = PROJECT_ROOT / f"level{level_index + 1}.map"
        tokens = path.read_text().split()
        self.width = int(tokens[0])
        self.height = int(tokens[1])
        values = [int(token) for token in tokens[2:]]
        values += [TILE_EMPTY] * (self.width * self.height - len(values))
        self.tiles = [values[y * self.width:(y + 1) * self.width] for y in range(self.height)]

    def tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return TILE_EMPTY
