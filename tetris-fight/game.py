import random
import time

import pygame

from colors import BLACK, PIECE_COLORS, GREY
from configs import GRID_WIDTH, GRID_HEIGHT, TITLE, BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from shapes import Piece, SHAPES


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.full_screen = self.init_display()
        self.pieces_screen = self.full_screen.subsurface((
            50,
            50,
            BLOCK_SIZE * GRID_WIDTH,
            BLOCK_SIZE * GRID_HEIGHT
        ))
        self.sunk_pieces = dict()
        self.current_piece = None
        self.auto_drop_count = 0

    def game_over(self):
        self.running = False

    def start(self):
        pressing = None
        while self.running:
            if self.current_piece is None:
                if self.purge_full_rows():
                    self.draw()
                    self.clock.tick(50)
                    self.drop_pieces()
                    self.clock.tick(200)
                    self.draw()
                    self.clock.tick(50)
                    continue
                self.new_round()
                pressing = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYUP:
                    if event.key == pressing:
                        pressing = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.left(self.grid)
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.right(self.grid)
                    if event.key == pygame.K_DOWN:
                        pressing = pygame.K_DOWN
                    if event.key == pygame.K_SPACE:
                        self.current_piece.rotate(self.grid)

            if pressing is pygame.K_DOWN:
                self.clock.tick(100)
                self.current_piece.down(self.grid)

            self.auto_drop_count += 1
            if self.auto_drop_count % 100 == 0 and not self.current_piece.down(self.grid):
                self.sunk_pieces[self.current_piece.get_id()] = self.current_piece
                self.current_piece = None

            self.draw()
            self.clock.tick(100)
        pygame.quit()

    def purge_full_rows(self):
        has_full_row = False
        for i in range(len(self.grid)):
            reverse_i = len(self.grid) - i - 1
            is_full = True
            piece_positions = dict()
            for j in range(len(self.grid[0])):
                piece_id = self.grid[reverse_i][j]
                if piece_id == 0:
                    is_full = False
                    break
                if piece_id not in piece_positions:
                    piece_positions[piece_id] = list()
                piece_positions[piece_id].append((reverse_i, j))
            if is_full:
                print("full row")
                has_full_row = True
                for piece_id, positions in piece_positions.items():
                    piece = self.sunk_pieces[piece_id]
                    if piece is not None:
                        print("purge shape: ", positions)
                        if piece.purge_shape(self.grid, positions):
                            del self.sunk_pieces[piece_id]
                        print("purge shape done")
                        # pieces.append(piece)
                break

        return has_full_row

    def drop_pieces(self):
        while True:
            has_down = False
            for _, piece in self.sunk_pieces.items():
                if piece.down(self.grid):
                    has_down = True
            if not has_down:
                break

    def draw(self):
        self.full_screen.fill(GREY)
        self.pieces_screen.fill(BLACK)
        if self.current_piece is not None:
            self.current_piece.draw(self.pieces_screen)
        for piece in self.sunk_pieces.values():
            piece.draw(self.pieces_screen)
        pygame.display.flip()

    def new_round(self):
        self.current_piece = self.generate_piece(self.grid)
        if self.current_piece is None:
            self.game_over()

    @staticmethod
    def init_display():
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        return screen

    @staticmethod
    def generate_piece(grid):
        i = int(time.time() * 1000000)
        p = Piece(i, random.choice(SHAPES), random.choice(PIECE_COLORS), 5, 0)
        if not p.attach(grid):
            return None
        return p
