from Models.Model import *

from typing import *


class Board:
    def __init__(self, size_x=None, size_y=None) -> None:
        if size_x is None or size_y is None:
            size_x = 10
            size_y = 20
        self.MIN_X = 0
        self.MAX_X = size_x - 1
        self.MIN_Y = 0
        self.MAX_Y = size_y - 1
        self.state = [[None for j in range(size_x)] for i in range(size_y)]
        self.active_piece = None
        self.pieces: List[Model] = []

    def display(self, projection=None):
        """Prints entire board"""
        self.update_state()
        for j, row in enumerate(reversed(self.state)):
            for i, column in enumerate(row):
                field = column
                if (projection is not None and projection) and (i, self.MAX_Y - j) in projection:
                    if field is not None:
                        print('1', end=' ')
                    else:
                        print('x', end=' ')
                else:
                    print(f"{'0' if field is None else '1'}", end=' ')
            print()

    def reset_state(self):
        """Resets all state fields to None"""
        for row in range(len(self.state)):
            for column in range(len(self.state[row])):
                self.state[row][column] = None

    def update_state(self):
        """Updates display state with all pieces on board."""
        self.reset_state()
        for piece in self.pieces:
            coordinates = piece.get_block_positions()
            for coor in coordinates:
                x, y = coor
                self.state[y][x] = piece

    def get_all_occupied_coordinates(self):
        all_coordinates = []
        for piece in self.pieces:
            all_coordinates += piece.get_block_positions()
        print(all_coordinates)

    def add_piece(self, piece: Model):
        """Adds new piece to the board. Returns False if there are collisions between new piece and piece that are
        already on the board. Returns True if piece can be added. """
        new_piece_coordinates = piece.get_block_positions()
        for coordinates in new_piece_coordinates:
            if not self.piece_encompasses_coordinates(coordinates):
                continue
            else:
                print('GAME OVER')
                return False
        self.pieces.append(piece)
        piece.parent_board = self

        return True

    def get_all_highest_piece_blocks(self):
        """Returns block with greatest y for every column."""
        self.reset_state()
        self.update_state()

        active_piece_blocks = self.active_piece.get_block_positions()
        result_blocks = {}
        for i in range(self.MAX_X + 1):
            result_blocks[i] = (i, -1)
        for x in range(self.MAX_X):
            for y in range(self.MAX_Y, self.MIN_Y - 1, -1):
                if self.state[y][x] is not None and (x, y) not in active_piece_blocks:
                    result_blocks[x] = (x, y)
                    break
        return result_blocks

    def piece_encompasses_coordinates(self, coordinates) -> Model or bool:
        """Returns piece on certain coordinates or False if there's isn't a piece at those coordinates."""
        if len(coordinates) != 2:
            raise IndexError("Coordinates consist of x and y")
        for piece in self.pieces:
            if piece.encompasses_coordinates(coordinates):
                return piece
        return False

    def is_inside(self, coordinates: tuple) -> bool:
        """Checks if coordinates are inside the board."""
        if len(coordinates) != 2:
            raise IndexError("Coordinates consist of x and y")
        x, y = coordinates
        if (self.MIN_X <= x <= self.MAX_X) and (self.MIN_Y <= y <= self.MAX_Y):
            return True
        else:
            return False

    def tetris(self):
        """Checks for tetris and makes appropriate changes to the board."""

        self.update_state()
        tetris_rows = []

        # find all full rows
        for j, row in enumerate(reversed(self.state)):
            tetris_in_row = True
            current_row = self.MAX_Y - j
            for column in row:
                field = column
                if field is None:
                    tetris_in_row = False
                    break
                else:
                    continue
            if tetris_in_row:
                tetris_rows.append(current_row)
            tetris_rows.sort()
            tetris_rows.reverse()
        print('Tetris rows', tetris_rows)

        # delete blocks in tetris rows
        for piece in self.pieces:
            remaining_blocks = []
            for block in piece.blocks:
                if block.y not in tetris_rows:
                    remaining_blocks.append(block)
            piece.blocks = remaining_blocks

        # move every piece above tetris row down
        for row in tetris_rows:
            for piece in self.pieces:
                for block in piece.blocks:
                    if block.y > row:
                        block.translate(0, -1)
