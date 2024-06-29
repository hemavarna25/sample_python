import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1400  # Increased width for dashboard
HEIGHT = 800
ROWS = 5
COLS = 6
CELL_SIZE = HEIGHT // ROWS  # Cell size adjusted to keep grid square
LINE_WIDTH = 9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SCORE_FONT_SIZE = 30
DASHBOARD_WIDTH = 200  # Width of the dashboard
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = WHITE
BUTTON_TEXT_HOVER_COLOR = BLACK

# Function to draw the grid lines
def draw_grid():
    for i in range(1, COLS):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
    for i in range(1, ROWS):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (HEIGHT, i * CELL_SIZE), LINE_WIDTH)

# Function to draw the X's and O's with strike effect for the winner
def draw_markers(board, winner):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20), 
                                 ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
                pygame.draw.line(screen, RED, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20), 
                                 (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 20, LINE_WIDTH)

    # Draw strike effect for the winning player's marks
    if winner:
        if winner == 'X':
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] == 'X':
                        pygame.draw.line(screen, BLACK, (col * CELL_SIZE + 10, row * CELL_SIZE + 10),
                                         ((col + 1) * CELL_SIZE - 10, (row + 1) * CELL_SIZE - 10), 5)
                        pygame.draw.line(screen, BLACK, ((col + 1) * CELL_SIZE - 10, row * CELL_SIZE + 10),
                                         (col * CELL_SIZE + 10, (row + 1) * CELL_SIZE - 10), 5)
        elif winner == 'O':
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] == 'O':
                        pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 20, 5)

# Function to check for a win
def check_win(board):
    # Check rows
    for row in board:
        if all(cell == 'X' for cell in row):
            return 'X'
        elif all(cell == 'O' for cell in row):
            return 'O'
    # Check columns
    for col in range(COLS):
        if all(board[row][col] == 'X' for row in range(ROWS)):
            return 'X'
        elif all(board[row][col] == 'O' for row in range(ROWS)):
            return 'O'
    # Check diagonals
    if all(board[i][i] == 'X' for i in range(ROWS)) or all(board[i][ROWS - i - 1] == 'X' for i in range(ROWS)):
        return 'X'
    elif all(board[i][i] == 'O' for i in range(ROWS)) or all(board[i][ROWS - i - 1] == 'O' for i in range(ROWS)):
        return 'O'
    return None

# Function to check for a draw
def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Function to reset the game
def reset_game():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to get AI move
def get_ai_move(board):
    available_moves = [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == ' ']
    return random.choice(available_moves)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Variables
board = reset_game()
current_player = 'X'
game_over = False
score_X = 0
score_O = 0
player_X_name = ""
player_O_name = ""
login_done = False
total_games = 0

# Reset Button
reset_button_rect = pygame.Rect(WIDTH - DASHBOARD_WIDTH + 40, 500, BUTTON_WIDTH, BUTTON_HEIGHT)

# Function to display login screen
def login_screen():
    global player_X_name, player_O_name, login_done
    input_box_X = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50)
    input_box_O = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_X = color_inactive
    color_O = color_inactive
    active_X = False
    active_O = False
    font = pygame.font.Font(None, 32)
    player_X_name = ''
    player_O_name = ''

    while not login_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_X.collidepoint(event.pos):
                    active_X = True
                    active_O = False
                elif input_box_O.collidepoint(event.pos):
                    active_X = False
                    active_O = True
                else:
                    active_X = False
                    active_O = False
                color_X = color_active if active_X else color_inactive
                color_O = color_active if active_O else color_inactive
            if event.type == pygame.KEYDOWN:
                if active_X:
                    if event.key == pygame.K_RETURN:
                        active_X = False
                        color_X = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        player_X_name = player_X_name[:-1]
                    else:
                        player_X_name += event.unicode
                if active_O:
                    if event.key == pygame.K_RETURN:
                        active_O = False
                        color_O = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        player_O_name = player_O_name[:-1]
                    else:
                        player_O_name += event.unicode
                if event.key == pygame.K_RETURN and player_X_name and player_O_name:
                    login_done = True

        screen.fill((30, 30, 30))
        txt_surface_X = font.render(player_X_name, True, color_X)
        txt_surface_O = font.render(player_O_name, True, color_O)
        screen.blit(txt_surface_X, (input_box_X.x + 5, input_box_X.y + 5))
        screen.blit(txt_surface_O, (input_box_O.x + 5, input_box_O.y + 5))
        pygame.draw.rect(screen, color_X, input_box_X, 2)
        pygame.draw.rect(screen, color_O, input_box_O, 2)
        prompt_X = font.render('Player X Name:', True, WHITE)
        prompt_O = font.render('Player O Name:', True, WHITE)
        screen.blit(prompt_X, (input_box_X.x, input_box_X.y - 30))
        screen.blit(prompt_O, (input_box_O.x, input_box_O.y - 30))

        pygame.display.flip()

# Main game loop
login_screen()
while True:
    winner = check_win(board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and current_player == 'X' and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < HEIGHT:  # Only allow clicks inside the game grid
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    if check_win(board) == 'X':
                        score_X += 1
                        game_over = True
                    elif check_draw(board):
                        game_over = True
                    current_player = 'O'

        if not game_over and current_player == 'O':
            row, col = get_ai_move(board)
            board[row][col] = 'O'
            if check_win(board) == 'O':
                score_O += 1
                game_over = True
            elif check_draw(board):
                game_over = True
            current_player = 'X'

        if game_over:
            total_games += 1

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board = reset_game()
                game_over = False
                current_player = 'X'

        if game_over and event.type == pygame.MOUSEBUTTONDOWN and reset_button_rect.collidepoint(event.pos):
            board = reset_game()
            game_over = False
            current_player = 'X'

    # Draw everything
    screen.fill(WHITE)
    draw_grid()
    draw_markers(board, winner)  # Pass winner to draw_markers function

    # Draw dashboard
    pygame.draw.rect(screen, (200, 200, 200), (HEIGHT, 0, DASHBOARD_WIDTH, HEIGHT))

    # Draw Reset Button
    pygame.draw.rect(screen, BUTTON_COLOR if not reset_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_HOVER_COLOR, reset_button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Reset", True, BUTTON_TEXT_COLOR if not reset_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_TEXT_HOVER_COLOR)
    text_rect = text.get_rect(center=reset_button_rect.center)
    screen.blit(text, text_rect)

    # Draw scores
    font = pygame.font.Font(None, SCORE_FONT_SIZE)
    score_text = font.render(f"{player_X_name}: {score_X}   {player_O_name}: {score_O}", True, BLACK)
    screen.blit(score_text, (HEIGHT + 20, 50))


    # Draw current player
    current_player_text = font.render(f"Current Player: {current_player}", True, BLACK)
    screen.blit(current_player_text, (HEIGHT + 20, 150))

    if winner:
        font = pygame.font.Font(None, 50)
        winner_text = font.render(f"{player_X_name if winner == 'X' else player_O_name} Wins!", True, RED if winner == 'X' else BLUE)
        winner_rect = winner_text.get_rect(center=(HEIGHT // 2, HEIGHT // 2))
        screen.blit(winner_text, winner_rect)
    elif game_over:
        font = pygame.font.Font(None, 50)
        draw_text = font.render("It's a Draw!", True, GREEN)
        draw_rect = draw_text.get_rect(center=(HEIGHT // 2, HEIGHT // 2))
        screen.blit(draw_text, draw_rect)

    pygame.display.flip()
