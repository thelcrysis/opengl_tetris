from Models.Block import *
from typing import *


class Model:
    def __init__(self, x_pos, y_pos) -> None:
        # self.vertices = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.min_y = None
        self.max_y = None
        self.min_x = None
        self.max_x = None

        # Board the piece belongs to
        self.parent_board = None

        self.blocks = []
        for block_coordinates in self.template:
            new_block = Block(*block_coordinates)
            new_block.translate(x_pos, y_pos)
            self.blocks.append(new_block)

        self.update_minmax()
        self.rotation_info = 0

    def update_minmax(self):
        self.min_x = min(self.blocks, key=lambda a: a.x).x
        self.max_x = max(self.blocks, key=lambda a: a.x).x
        self.min_y = min(self.blocks, key=lambda a: a.y).y
        self.max_y = max(self.blocks, key=lambda a: a.y).y

    def down(self):
        """Drops a piece one position down."""
        return self.translate(0, -1)

    def left(self):
        """Moves a piece one position to the left"""
        return self.translate(-1, 0)

    def right(self):
        """Moves a piece one position to the right"""
        return self.translate(1, 0)

    def translate(self, delta_x, delta_y):
        """Translates a piece by delta x and delta y, if there is broken constraint (collision or out of bounds)
        return False """
        if self.parent_board is None:
            raise ReferenceError("Piece isn't assigned to a board")
        block_coordinates = self.get_block_positions().copy()
        for block in block_coordinates:
            x, y = block
            if not self.parent_board.is_inside((x + delta_x, y + delta_y)):
                return False

            # Checks collision with other pieces
            check_collision = self.parent_board.piece_encompasses_coordinates((x + delta_x, y + delta_y))
            if check_collision != False and check_collision is not self:
                return False
        for block in self.blocks:
            block.translate(delta_x, delta_y)

        self.x_pos = x + delta_x
        self.y_pos = y + delta_y

        self.update_minmax()
        return True

    def rotate_CW(self):
        """Rotate a piece clockwise."""
        if self.parent_board is None:
            raise ReferenceError("Piece isn't assigned to a board")

        next_rotation = self.next_rotation()
        new_template = self.templates[next_rotation]
        new_block_coordinates = new_template.copy()

        for block_coor in new_block_coordinates:
            x, y = block_coor
            if not self.parent_board.is_inside((x + self.x_pos, y + self.y_pos)):
                print('After rotation piece would go out of bounds!!!')
                return False

            # Checks collision with other pieces
            check_collision = self.parent_board.piece_encompasses_coordinates((x + self.x_pos, y + self.y_pos))
            if check_collision != False and check_collision is not self:  # might cause a bug
                return False

        self.blocks.clear()
        for block_coor in new_block_coordinates:
            block = Block(*block_coor)
            block.translate(self.x_pos, self.y_pos)
            self.blocks.append(block)

        self.update_minmax()
        self.rotation_info = next_rotation
        return True

    def next_rotation(self):
        rotated = self.rotation_info + 1
        if rotated == 4:
            rotated = 0
        return rotated

    def get_block_positions(self):
        """Returns all block coordinates for the piece."""
        coordinates = []
        for block in self.blocks:
            coordinates.append((block.x, block.y))
        return coordinates.copy()

    def project_piece_drop_location(self) -> List[Tuple]:
        """Calculates where piece would fall on board if instant drop is used, return list of blocks' coordinates"""
        # projects where piece would fall on board if instant drop is used
        greatest_y_columns = self.parent_board.get_all_highest_piece_blocks()
        x_min, x_max = self.min_x, self.max_x
        block_positions = self.get_block_positions()

        # find all lowest blocks for active piece
        lowest_block_per_y = {}
        for i in range(x_min, x_max + 1):
            lowest_block_per_y[i] = self.parent_board.MAX_Y + 1
        for block in block_positions:
            x, y = block
            if y < lowest_block_per_y[x]:
                lowest_block_per_y[x] = y

        lowest_block_positions = []
        for key in lowest_block_per_y:
            value = lowest_block_per_y[key]
            lowest_block_positions.append((key, value))

        # calculates distance between the piece and it's projection
        min_block_projection_distance = None
        for block in lowest_block_positions:
            x, y = block
            block_projection_distance = y - greatest_y_columns[x][1]  # index 1 = y
            if min_block_projection_distance is None:
                min_block_projection_distance = block_projection_distance
            if block_projection_distance < min_block_projection_distance:
                min_block_projection_distance = block_projection_distance
        if min_block_projection_distance <= 1:
            return block_positions
        # update block projection's coordinates
        projection = []
        for block in block_positions:
            x, y = block
            projection.append((x, y - min_block_projection_distance + 1))
        return projection

    def encompasses_coordinates(self, coordinates: tuple) -> bool:
        """Checks if a piece encompasses certain coordinates"""
        x, y = coordinates
        for block in self.blocks:
            if block.x == x and block.y == y:
                return True
        return False

    def __str__(self) -> str:
        pass
