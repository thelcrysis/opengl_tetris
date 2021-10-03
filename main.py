from typing import Tuple

from Models.Block import *
from Models.Cube import *
from Models.L import *
from Models.reverseL import *
from Models.I import *
from Models.T import *
from Board import *

import glm
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from time import sleep
from threading import Thread
from random import randint

global sleep_time  # wait time between two drops
sleep_time = 1
global input_queue  # input queue
input_queue = []


def print_board(board):
    """Prints entire board"""
    for row in reversed(board):
        for column in row:
            field = column
            print(f"{'0' if field is None else '1'}", end=' ')
        print()


def turn_clock():
    global sleep_time, input_queue
    while True:
        sleep(sleep_time)
        input_queue.append('s')
        print('Print queue is now:', input_queue)


def random_piece() -> Model:
    """Returns a random piece."""
    pieces = [Cube, L, reverseL, I, T]
    return pieces[randint(0, len(pieces) - 1)]


def draw_line(c1: tuple, c2: tuple, color: Tuple[float] = None):
    if color is not None and len(color) != 3:
        raise ArgumentError("Wrong number of color arguments!")
    x1, y1 = c1
    x2, y2 = c2
    if color is not None:
        glColor3f(*color)
    else:
        glColor3ub(150, 150, 150)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_block_frame(c1: tuple, size: int = 30, dont_draw: str = '0000', color: Tuple[float] = None):
    #       2 dd
    # c2 ·------· c3
    #    |      |
    #  1 |      | 3 dd
    # dd |      |
    # c1 ·------· c4
    #       4 dd

    x1, y1 = c1
    c2 = (x1, y1 + size)
    c3 = (x1 + size, y1 + size)
    c4 = (x1 + size, y1)

    glLineStipple(1, 0xAAAA)
    glEnable(GL_LINE_STIPPLE)
    if dont_draw[0] == '0':
        draw_line(c1, c2, color)
    if dont_draw[1] == '0':
        draw_line(c2, c3, color)
    if dont_draw[2] == '0':
        draw_line(c3, c4, color)
    if dont_draw[3] == '0':
        draw_line(c4, c1, color)
    glDisable(GL_LINE_STIPPLE)


def draw_background_table(x_0: int, y_0: int, start_point: Tuple[int] = (30, 30), size: int = 30, color: Tuple = None):
    x = start_point[0]
    y = start_point[1]
    for j in range(y_0):
        for i in range(x_0):
            if j == 0:
                if i == 0:
                    draw_block_frame((x, y), color=color)
                else:
                    draw_block_frame((x, y), dont_draw='1000', color=color)
            else:
                if i == 0:
                    draw_block_frame((x, y), dont_draw='0001', color=color)
                else:
                    draw_block_frame((x, y), dont_draw='1001', color=color)
            x += size
        y += size
        x = start_point[0]


def draw_block(x_0: int, y_0: int, start_point: Tuple[int] = (30, 30), size: int = 30, color: Tuple = None):
    if color is None:
        color = (94, 32, 193)

    start_x, start_y = start_point
    v1 = (start_x + size * x_0 + 1, start_y + size * y_0 + 1)
    v2 = (start_x + size * x_0 + 1, start_y + size * (y_0 + 1))
    v3 = (start_x + size * (x_0 + 1), start_y + size * (y_0 + 1))
    v4 = (start_x + size * (x_0 + 1), start_y + size * y_0 + 1)

    glColor3ub(*color);
    glBegin(GL_POLYGON)
    glVertex2i(*v1)
    glVertex2i(*v2)
    glVertex2i(*v3)
    glVertex2i(*v4)
    glEnd()


def draw_board(board: Board):
    pass


def draw_scene():
    draw_background_table(10, 20)
    draw_block(0, 0)
    draw_block(0, 1)
    draw_block(1, 1)
    draw_block(2, 1)
    pass


def myKeyboard(key, x, y):
    if key == b'\x1b':
        print('ESC')
        glutLeaveMainLoop()
    elif key == b'a' or key == b'A':
        print('A')
    elif key == b'd' or key == b'D':
        print('D')
    elif key == b'w' or key == b'W':
        print('W')
    elif key == b'\r':
        print('ENTER')


def myReshape(width, height):
    glDisable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width - 1, 0, height - 1, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def myDisplay():
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_scene()
    glutSwapBuffers()


def main():
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 1000)
    glutInitWindowPosition(0, 0)
    glutInit()

    window = glutCreateWindow("OpenGL")

    clock_thread = Thread(target=turn_clock)
    clock_thread.start()

    glutReshapeFunc(myReshape)
    glutKeyboardFunc(myKeyboard)
    glutDisplayFunc(myDisplay)
    glutMainLoop()

    # active_piece = None
    # board = Board()

    # while True:
    #     # os.system("clear")
    #     if active_piece is None:
    #         board.tetris()
    #         board.display()
    #         print("ACTIVE PIECE IS NONE")
    #         new_piece_type = random_piece()
    #         active_piece = new_piece_type(4, 13)
    #         board.active_piece = active_piece
    #         print(active_piece.title)
    #         out = board.add_piece(active_piece)
    #         if out == False:
    #             print("GAME OVER!")
    #             break
    #     projection = active_piece.project_piece_drop_location()
    #     print('PROJECTION', projection)
    #
    #     board.display(projection)
    #     board.get_all_occupied_coordinates()
    #     command = input()
    #     if command not in ['a', 'd', '', 'r', 'f']:
    #         raise ValueError("Command not available")
    #     if command == 'a':
    #         out_l = active_piece.left()
    #         out_d = active_piece.down()
    #         if out_l and out_d == False:
    #             active_piece = None
    #     elif command == 'd':
    #         out_r = active_piece.right()
    #         out_d = active_piece.down()
    #         if out_r and out_d == False:
    #             active_piece = None
    #     elif command == '':
    #         out = active_piece.down()
    #         if out == False:
    #             active_piece = None
    #     elif command == 'r':
    #         out = active_piece.rotate_CW()
    #     elif command == 'f':
    #         while active_piece.down():
    #             pass
    #         active_piece = None


if __name__ == '__main__':
    main()
