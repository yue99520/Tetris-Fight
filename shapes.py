# 方塊形狀
from typing import List, Tuple

import numpy
import pygame

from configs import BLOCK_SIZE

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]


class Piece:
    def __init__(self, _id, shape, color, px, py):
        self.id = _id
        self.shape = numpy.array(shape)
        self.color = color
        self.x = px
        self.y = py
        self.attached = False

    def get_id(self):
        return self.id

    def left(self, grid):
        x = self.x - 1
        return self.move_to(grid, x, self.y)

    def right(self, grid):
        x = self.x + 1
        return self.move_to(grid, x, self.y)

    def down(self, grid):
        y = self.y + 1
        return self.move_to(grid, self.x, y)

    def rotate(self, grid):
        attached = self.attached
        if self.attached:
            self.detach(grid)

        current_shape = self.shape
        right_shape = self.__get_right_rotation_shape(current_shape)
        rotate_result = False
        self.shape = right_shape
        if not self.check_collision(grid, self.x, self.y):
            rotate_result = True
        else:
            self.shape = current_shape

        if attached:
            self.attach(grid)
        return rotate_result

    def purge_shape(self, grid, positions: List[Tuple[int, int]]):
        attached = self.attached
        if self.attached:
            self.detach(grid)

        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                x = self.x + j
                y = self.y + i
                if cell:
                    for position in positions:
                        if y == position[0] and x == position[1]:
                            self.shape[i][j] = 0
        is_zero_shape = True
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell != 0:
                    is_zero_shape = False
                    break
        if is_zero_shape:
            return True
        if attached:
            self.attach(grid)
        return False

    def move_to(self, grid, x, y):
        attached = self.attached
        if self.attached:
            self.detach(grid)

        move_result = False
        if not self.check_collision(grid, x, y):
            self.x = x
            self.y = y
            move_result = True

        if attached:
            self.attach(grid)
        return move_result

    def attach(self, grid):
        if self.attached:
            return True
        elif self.__write_grid(grid, self.id):
            self.attached = True
            return True
        return False

    def detach(self, grid):
        if not self.attached:
            return True
        elif self.__write_grid(grid, 0):
            self.attached = False
            return True
        return False

    def __write_grid(self, grid, value):
        todos = list()
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                x = self.x + j
                y = self.y + i
                if cell:
                    if x < 0 or x >= len(grid[0]):
                        return False
                    elif y < 0 or y >= len(grid):
                        return False
                    elif value != 0 and grid[y][x] == 0 or value == 0 and grid[y][x] == self.id:
                        todos.append((y, x, value))
                    else:
                        return False
        for y, x, value in todos:
            grid[y][x] = value
        return True

    @staticmethod
    def __get_right_rotation_shape(shape):
        right = numpy.zeros((len(shape[0]), len(shape)), dtype=int)
        for i in range(len(shape)):
            new_i = len(shape) - i - 1
            for j in range(len(shape[0])):
                right[j][new_i] = shape[i][j]
        return right

    def check_collision(self, grid, x, y):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    if x + j < 0 or x + j >= len(grid[0]):
                        return True
                    if y + i < 0 or y + i >= len(grid):
                        return True
                    if grid[y + i][x + j] != 0:
                        return True
        return False

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, (0, 0, 0),  # 黑色邊框
                                     ((self.x + j) * BLOCK_SIZE,
                                      (self.y + i) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

                    # 內部矩形（略小，填充顏色）
                    pygame.draw.rect(screen, self.color,
                                     ((self.x + j) * BLOCK_SIZE + 1,
                                      (self.y + i) * BLOCK_SIZE + 1,
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))
