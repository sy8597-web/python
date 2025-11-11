# ...existing code...
print('aaa')
# ...existing code...
import pygame
import random
import sys

# Tetris for Pygame - simple implementation

CELL = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL * COLUMNS
HEIGHT = CELL * ROWS
FPS = 60

SHAPES = {
    'I': [[1,1,1,1]],
    'O': [[1,1],
          [1,1]],
    'T': [[0,1,0],
          [1,1,1]],
    'S': [[0,1,1],
          [1,1,0]],
    'Z': [[1,1,0],
          [0,1,1]],
    'J': [[1,0,0],
          [1,1,1]],
    'L': [[0,0,1],
          [1,1,1]],
}

COLORS = {
    'I': (0,240,240),
    'O': (240,240,0),
    'T': (160,0,240),
    'S': (0,240,0),
    'Z': (240,0,0),
    'J': (0,0,240),
    'L': (240,160,0),
    None: (20,20,20)
}

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.shape = [row[:] for row in SHAPES[kind]]
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = rotate(self.shape)

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.score = 0
        self.lines = 0

    def valid(self, piece, dx=0, dy=0):
        for r, row in enumerate(piece.shape):
            for c, val in enumerate(row):
                if val:
                    x = piece.x + c + dx
                    y = piece.y + r + dy
                    if x < 0 or x >= COLUMNS or y < 0 or y >= ROWS:
                        return False
                    if self.grid[y][x] is not None:
                        return False
        return True

    def place(self, piece):
        for r, row in enumerate(piece.shape):
            for c, val in enumerate(row):
                if val:
                    x = piece.x + c
                    y = piece.y + r
                    if 0 <= y < ROWS:
                        self.grid[y][x] = piece.kind
        cleared = self.clear_lines()
        self.lines += cleared
        self.score += [0,40,100,300,1200][cleared]

    def clear_lines(self):
        new = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = ROWS - len(new)
        while len(new) < ROWS:
            new.insert(0, [None for _ in range(COLUMNS)])
        self.grid = new
        return cleared

    def is_game_over(self):
        return any(cell is not None for cell in self.grid[0])

def draw_grid(surface, board):
    for y in range(ROWS):
        for x in range(COLUMNS):
            cell = board.grid[y][x]
            color = COLORS[cell]
            rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (40,40,40), rect, 1)

def draw_piece(surface, piece):
    for r, row in enumerate(piece.shape):
        for c, val in enumerate(row):
            if val:
                x = piece.x + c
                y = piece.y + r
                rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
                pygame.draw.rect(surface, COLORS[piece.kind], rect)
                pygame.draw.rect(surface, (60,60,60), rect, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + 200, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    board = Board()
    current = Piece(random.choice(list(SHAPES.keys())))
    next_piece = Piece(random.choice(list(SHAPES.keys())))
    fall_time = 0
    fall_speed = 0.5  # seconds per step
    running = True
    paused = False

    while running:
        dt = clock.tick(FPS) / 1000.0
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused
                if paused:
                    continue
                if event.key == pygame.K_LEFT:
                    if board.valid(current, dx=-1):
                        current.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if board.valid(current, dx=1):
                        current.x += 1
                elif event.key == pygame.K_DOWN:
                    if board.valid(current, dy=1):
                        current.y += 1
                elif event.key == pygame.K_SPACE:
                    # hard drop
                    while board.valid(current, dy=1):
                        current.y += 1
                    board.place(current)
                    current = next_piece
                    next_piece = Piece(random.choice(list(SHAPES.keys())))
                    if not board.valid(current):
                        running = False
                elif event.key == pygame.K_z:
                    # rotate left
                    old = [row[:] for row in current.shape]
                    current.rotate(); current.rotate(); current.rotate()
                    if not board.valid(current):
                        current.shape = old
                elif event.key == pygame.K_x:
                    # rotate right
                    old = [row[:] for row in current.shape]
                    current.rotate()
                    if not board.valid(current):
                        current.shape = old

        if not paused:
            if fall_time >= fall_speed:
                fall_time = 0
                if board.valid(current, dy=1):
                    current.y += 1
                else:
                    board.place(current)
                    current = next_piece
                    next_piece = Piece(random.choice(list(SHAPES.keys())))
                    if not board.valid(current):
                        running = False

        # draw
        screen.fill((10,10,10))
        play_surface = pygame.Surface((WIDTH, HEIGHT))
        play_surface.fill((10,10,10))
        draw_grid(play_surface, board)
        draw_piece(play_surface, current)
        screen.blit(play_surface, (0,0))

        # sidebar
        sx = WIDTH + 20
        screen.fill((20,20,20), rect=pygame.Rect(WIDTH,0,200,HEIGHT))
        lbl = font.render("Next:", True, (255,255,255))
        screen.blit(lbl, (sx, 10))
        # draw next piece small
        for r, row in enumerate(next_piece.shape):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(sx + c*CELL//2, 40 + r*CELL//2, CELL//2, CELL//2)
                    pygame.draw.rect(screen, COLORS[next_piece.kind], rect)
                    pygame.draw.rect(screen, (60,60,60), rect, 1)

        score_lbl = font.render(f"Score: {board.score}", True, (255,255,255))
        lines_lbl = font.render(f"Lines: {board.lines}", True, (255,255,255))
        screen.blit(score_lbl, (sx, 140))
        screen.blit(lines_lbl, (sx, 170))
        help1 = font.render("Arrows: move", True, (200,200,200))
        help2 = font.render("Z/X: rotate", True, (200,200,200))
        help3 = font.render("Space: drop", True, (200,200,200))
        help4 = font.render("P: pause", True, (200,200,200))
        screen.blit(help1, (sx, 220))
        screen.blit(help2, (sx, 250))
        screen.blit(help3, (sx, 280))
        screen.blit(help4, (sx, 310))

        if paused:
            p = font.render("PAUSED", True, (255,255,255))
            screen.blit(p, (WIDTH//2 - 30, HEIGHT//2))
        pygame.display.flip()

    # game over
    over_font = pygame.font.SysFont(None, 48)
    text = over_font.render("GAME OVER", True, (255, 50, 50))
    screen.blit(text, (WIDTH//2 - 120, HEIGHT//2 - 24))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()