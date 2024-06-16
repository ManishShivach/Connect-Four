import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_peice(board, col, row, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    global ROW_COUNT
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# printing our fliped board
def print_board(board):
    print(np.flip(board, 0))

# Game Algorithm
def game_algorithm(board, piece):
    # check horizontal location for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical location for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            
    # check diagonals location for win
    # positively slope
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            
    # negatively slope
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board, x):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), int(RADIUS))
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), x - int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2) + SQUARESIZE), int(RADIUS))
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), x - int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2) + SQUARESIZE), int(RADIUS))

    pygame.display.update()


gameover = False
turn = 0

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
heigth = (ROW_COUNT + 1) * SQUARESIZE

size = (width, heigth)
RADIUS = int(SQUARESIZE/2 * 0.9)

board = create_board()
print_board(board)

# Pygame
pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board, heigth)
pygame.display.update()

MyFont = pygame.font.SysFont('monospace', 75)

# Game Loop
while not gameover:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posball_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posball_x, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posball_x, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:    
            # Ask for player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_peice(board, col, row, 1)

                    if game_algorithm(board, 1):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = MyFont.render('PLAYER 1 WINS!!', 1, GREEN)
                        screen.blit(label, (20, 10))
                        gameover = True

            # Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_peice(board, col, row, 2)

                    if game_algorithm(board, 2):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = MyFont.render('PLAYER 1 WINS!!', 0, GREEN)
                        screen.blit(label, (20, 10))
                        gameover = True
            
            print_board(board)
            draw_board(board, heigth)
            pygame.display.update()
            # alternating the turn between the players
            turn += 1
            turn = turn % 2

            if gameover:
                pygame.time.wait(3000)

