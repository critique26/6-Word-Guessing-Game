"""
WORD GUESSING GAME (PYTHON QUEST)
Group 6 Project - Refactored using Python Lists & Pygame GUI
"""

import pygame
import random

pygame.init()

# Setup Screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Word Guessing Game - Python Quest")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 80)
large_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 38)
small_font = pygame.font.Font(None, 28)

# Color Palette (Pastel Galaxy Theme)
BG = (24, 14, 28)
PANEL = (48, 28, 48)
PANEL_LIGHT = (72, 40, 68)
WHITE = (255, 248, 253)
PURPLE = (235, 170, 220)
GREEN = (145, 230, 190)
RED = (255, 125, 160)
YELLOW = (255, 225, 170)
GRAY = (205, 180, 200)
PASTEL_PINK = (255, 190, 220)
SOFT_PINK = (255, 215, 235)

# ==============================================================================
# DATA STRUCTURES (MANDATORY LIST TRANSFORMATIONS)
# ==============================================================================

# 1 & 2. Nested List: [Hint, Answer, Category] records (10+ Questions)
master_questions = [
    ["A popular programming language used to create this game", "python", "Basics"],
    ["A collection of key-value pairs in Python", "dictionary", "Data Structures"],
    ["A function used to display text on the screen", "print", "Basics"],
    ["A loop that repeats while a condition is true", "while", "Control Flow"],
    ["A loop commonly used to repeat through a sequence", "for", "Control Flow"],
    ["A keyword used to define a function", "def", "Functions"],
    ["A data type that stores True or False", "boolean", "Data Types"],
    ["A function used to get text input from the user", "input", "Basics"],
    ["A data type used for whole numbers without decimals", "integer", "Data Types"],
    ["A keyword used to make conditional decisions", "if", "Control Flow"],
    ["An ordered sequence of items surrounded by brackets", "list", "Data Structures"],
    ["A immutable sequence enclosed in parentheses", "tuple", "Data Structures"],
    ["Step-by-step procedure or formula for solving a problem", "algorithm", "CS Concepts"]
]

# 3. List 2: Active deck of remaining questions for the session
active_pool = []

# 4. List 3: Real-time record of used letter guesses in the current round
used_letters = []

# 5. List 4: Match history list storing [Word, Result, Attempt Count] records
game_history = []

# 6. List 5: High score leaderboard containing [Player Name, Score] nested lists
leaderboard = [
    ["Alex", 50],
    ["Jordan", 30],
    ["Sam", 20]
]

# State Variables
player_name = ""
game_state = "name_input"  # States: name_input, instructions, playing, correct, wrong, gameover, win, history, leaderboard
current_q = []
word = ""
hint = ""
category = ""
guess = ""
lives = 5
score = 0


# ==============================================================================
# HELPER FUNCTIONS & LIST OPERATIONS
# ==============================================================================

def reset_game():
    """Resets game session state and builds a fresh active question pool."""
    global active_pool, used_letters, game_history, lives, score, game_state
    
    lives = 5
    score = 0
    used_letters = []
    game_history = []
    
    # Copy master list and shuffle
    active_pool = list(master_questions)
    random.shuffle(active_pool)
    
    load_next_question()
    game_state = "instructions"


def load_next_question():
    """Pops the next question from the active pool list."""
    global current_q, word, hint, category, guess, used_letters, game_state
    
    if len(active_pool) > 0:
        # LIST OPERATOR: pop() removes and returns element from list
        current_q = active_pool.pop()
        hint = current_q[0]      # Indexing
        word = current_q[1]      # Indexing
        category = current_q[2]  # Indexing
        guess = ""
        used_letters = []
    else:
        update_leaderboard()
        game_state = "win"


def process_guess():
    """Evaluates user guess and updates player state & history lists."""
    global score, lives, game_state
    
    clean_guess = guess.lower().strip()
    
    # LIST SEARCH & TRAVERSAL: Track used character inputs
    for char in clean_guess:
        if char not in used_letters:
            used_letters.append(char)  # LIST OPERATOR: append()
            
    if clean_guess == word:
        score += 10
        # LIST OPERATOR: append() record to nested game_history list
        game_history.append([word, "CORRECT", len(used_letters)])
        game_state = "correct"
    else:
        lives -= 1
        if lives <= 0:
            game_history.append([word, "FAILED", len(used_letters)])
            update_leaderboard()
            game_state = "gameover"
        else:
            game_state = "wrong"


def update_leaderboard():
    """Adds current score and sorts the high score leaderboard list."""
    global leaderboard
    if player_name.strip() != "":
        leaderboard.append([player_name, score])
        # LIST OPERATOR: sort() with lambda key for descending numerical order
        leaderboard.sort(key=lambda x: x[1], reverse=True)


# ==============================================================================
# DRAWING HELPERS
# ==============================================================================

def draw_text(text, font_type, color, x, y, center=False):
    image = font_type.render(str(text), True, color)
    if center:
        rect = image.get_rect(center=(x, y))
        screen.blit(image, rect)
    else:
        screen.blit(image, (x, y))


def draw_panel(rect, color=PANEL):
    pygame.draw.rect(screen, color, rect, border_radius=20)


def draw_background():
    screen.fill(BG)
    random.seed(23)
    for _ in range(120):
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        size = random.choice([1, 1, 2])
        pygame.draw.circle(screen, SOFT_PINK, (x, y), size)
    random.seed()


# ==============================================================================
# MAIN GAME LOOP
# ==============================================================================

running = True

while running:
    # --------------------------------------------------------------------------
    # INPUT HANDLING & EVENT LOOP
    # --------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # STATE 1: NAME INPUT
            if game_state == "name_input":
                if event.key == pygame.K_RETURN and player_name.strip() != "":
                    reset_game()
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isalnum() and len(player_name) < 12:
                    player_name += event.unicode

            # STATE 2: INSTRUCTIONS
            elif game_state == "instructions":
                if event.key == pygame.K_RETURN:
                    game_state = "playing"

            # STATE 3: PLAYING
            elif game_state == "playing":
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN and guess.strip() != "":
                    process_guess()
                elif event.unicode.isalpha() and len(guess) < 20:
                    guess += event.unicode

            # STATE 4 & 5: FEEDBACK (CORRECT / WRONG)
            elif game_state in ["correct", "wrong"]:
                if event.key == pygame.K_RETURN:
                    if game_state == "correct":
                        load_next_question()
                        if game_state != "win":
                            game_state = "playing"
                    else:
                        guess = ""
                        game_state = "playing"

            # STATE 6, 7, 8: END SCREENS (GAMEOVER / WIN / LEADERBOARD / HISTORY)
            elif game_state in ["gameover", "win", "leaderboard", "history"]:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_l:
                    game_state = "leaderboard"
                elif event.key == pygame.K_h:
                    game_state = "history"

    # --------------------------------------------------------------------------
    # RENDERING & SCREEN STATES
    # --------------------------------------------------------------------------
    draw_background()

    # --- STATE: NAME INPUT ---
    if game_state == "name_input":
        draw_text("WORD GUESSING GAME", title_font, PURPLE, WIDTH // 2, HEIGHT // 2 - 140, True)
        draw_text("Enter Player Name to Begin:", font, WHITE, WIDTH // 2, HEIGHT // 2 - 50, True)
        
        draw_panel(pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2, 500, 70), PANEL_LIGHT)
        draw_text(player_name + "_", large_font, YELLOW, WIDTH // 2, HEIGHT // 2 + 35, True)
        
        draw_text("Press ENTER when ready", small_font, GRAY, WIDTH // 2, HEIGHT // 2 + 100, True)

    # --- STATE: INSTRUCTIONS ---
    elif game_state == "instructions":
        draw_text("HOW TO PLAY", title_font, PASTEL_PINK, WIDTH // 2, 100, True)
        
        draw_panel(pygame.Rect(WIDTH // 2 - 350, 180, 700, 360))
        instructions = [
            "1. Read the clue and category for the word.",
            "2. Type your full word guess using the keyboard.",
            "3. Press [ENTER] to submit your answer.",
            "4. Each incorrect guess costs 1 Life (5 Max).",
            "5. Correct answers earn +10 points.",
            "6. Your used characters will be tracked live!"
        ]
        
        # LIST TRAVERSAL: Loop over instructions list
        for i, line in enumerate(instructions):
            draw_text(line, font, WHITE, WIDTH // 2 - 310, 210 + (i * 50))
            
        draw_text("PRESS ENTER TO START GAME", font, GREEN, WIDTH // 2, HEIGHT - 100, True)

    # --- STATE: PLAYING ---
    elif game_state == "playing":
        # Header Stats
        draw_text("PLAYER: " + player_name, font, PASTEL_PINK, 60, 40)
        draw_text("CATEGORY: " + category, font, YELLOW, WIDTH // 2 - 100, 40)
        
        # LIST OPERATOR: len() on question pool
        total_q = len(master_questions)
        remaining_q = len(active_pool) + 1
        draw_text(f"REMAINING: {remaining_q}/{total_q}", font, WHITE, WIDTH - 280, 40)

        # Question Panel
        draw_panel(pygame.Rect(60, 90, WIDTH - 120, 140))
        draw_text("💡 HINT:", font, YELLOW, 90, 110)
        draw_text(hint, font, WHITE, 90, 150)
        draw_text(f"Word length: {len(word)} letters", small_font, GRAY, 90, 190)

        # Guess Input Box
        draw_text("YOUR ANSWER:", small_font, SOFT_PINK, 60, 250)
        draw_panel(pygame.Rect(60, 280, WIDTH - 120, 70), PANEL_LIGHT)
        draw_text(guess + "_", large_font, YELLOW, 90, 315)

        # Used Characters Collection Display (Requirement 10)
        draw_panel(pygame.Rect(60, 370, WIDTH - 120, 80))
        draw_text("CHARACTER HISTORY (USED):", small_font, GRAY, 80, 380)
        
        # LIST TRAVERSAL & SEARCH: Render used letters string
        used_str = " ".join([c.upper() for c in used_letters])
        draw_text(used_str if used_str else "None", font, PURPLE, 80, 410)

        # Bottom HUD
        draw_panel(pygame.Rect(60, 470, WIDTH - 120, 80))
        draw_text(f"❤️ Lives: {lives}", font, RED, 100, 495)
        draw_text(f"⭐ Score: {score}", font, YELLOW, WIDTH // 2 - 80, 495)
        draw_text("ENTER = Submit | ESC = Quit", small_font, GRAY, WIDTH - 320, 500)

    # --- STATE: CORRECT ---
    elif game_state == "correct":
        draw_text("CORRECT!", title_font, GREEN, WIDTH // 2, HEIGHT // 2 - 80, True)
        draw_text(f"The answer was: {word}", font, WHITE, WIDTH // 2, HEIGHT // 2, True)
        draw_text("+10 POINTS", large_font, YELLOW, WIDTH // 2, HEIGHT // 2 + 60, True)
        draw_text("PRESS ENTER FOR NEXT QUESTION", small_font, GRAY, WIDTH // 2, HEIGHT - 100, True)

    # --- STATE: WRONG ---
    elif game_state == "wrong":
        draw_text("WRONG ANSWER!", title_font, RED, WIDTH // 2, HEIGHT // 2 - 80, True)
        draw_text(f"Lives remaining: {lives}", font, WHITE, WIDTH // 2, HEIGHT // 2, True)
        draw_text("PRESS ENTER TO TRY AGAIN", small_font, GRAY, WIDTH // 2, HEIGHT - 100, True)

    # --- STATE: GAME OVER / WIN ---
    elif game_state in ["gameover", "win"]:
        title_str = "VICTORY!" if game_state == "win" else "GAME OVER"
        title_color = GREEN if game_state == "win" else RED
        
        draw_text(title_str, title_font, title_color, WIDTH // 2, 120, True)
        draw_text(f"Final Score: {score}", large_font, YELLOW, WIDTH // 2, 200, True)

        draw_panel(pygame.Rect(WIDTH // 2 - 250, 270, 500, 160))
        draw_text("[R] Play Again", font, WHITE, WIDTH // 2, 300, True)
        draw_text("[L] View Leaderboard", font, WHITE, WIDTH // 2, 340, True)
        draw_text("[H] View Match History", font, WHITE, WIDTH // 2, 380, True)
        draw_text("ESC - Quit Game", small_font, GRAY, WIDTH // 2, HEIGHT - 80, True)

    # --- STATE: LEADERBOARD SCREEN ---
    elif game_state == "leaderboard":
        draw_text("TOP PLAYERS LEADERBOARD", title_font, YELLOW, WIDTH // 2, 100, True)
        
        draw_panel(pygame.Rect(WIDTH // 2 - 300, 180, 600, 320))
        
        # LIST TRAVERSAL: Display top 5 sorted leaderboard records
        for idx, record in enumerate(leaderboard[:5]):
            # Indexing inner record list
            p_name, p_score = record[0], record[1]
            draw_text(f"{idx + 1}. {p_name}", font, WHITE, WIDTH // 2 - 240, 210 + (idx * 50))
            draw_text(f"{p_score} pts", font, PASTEL_PINK, WIDTH // 2 + 140, 210 + (idx * 50))

        draw_text("Press [R] to Play Again | [H] View History | [ESC] Quit", small_font, GRAY, WIDTH // 2, HEIGHT - 80, True)

    # --- STATE: MATCH HISTORY SCREEN ---
    elif game_state == "history":
        draw_text("SESSION MATCH HISTORY", title_font, PURPLE, WIDTH // 2, 100, True)
        
        draw_panel(pygame.Rect(WIDTH // 2 - 350, 180, 700, 340))
        draw_text("Word", font, YELLOW, WIDTH // 2 - 280, 200)
        draw_text("Result", font, YELLOW, WIDTH // 2 - 30, 200)
        draw_text("Guesses Used", font, YELLOW, WIDTH // 2 + 170, 200)
        
        # LIST TRAVERSAL: Render match history records
        for idx, record in enumerate(game_history[-5:]):
            res_color = GREEN if record[1] == "CORRECT" else RED
            draw_text(record[0], font, WHITE, WIDTH // 2 - 280, 250 + (idx * 50))
            draw_text(record[1], font, res_color, WIDTH // 2 - 30, 250 + (idx * 50))
            draw_text(str(record[2]), font, WHITE, WIDTH // 2 + 210, 250 + (idx * 50))

        draw_text("Press [R] to Play Again | [L] View Leaderboard | [ESC] Quit", small_font, GRAY, WIDTH // 2, HEIGHT - 80, True)

    pygame.display.update()
    clock.tick(60)

pygame.quit()