# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate

# Intall specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

# High-level logic
# 1. Create and init the simulation grid (Connect with tick)
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output 
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

# Deadline - 15th of December 2023
# Mail with: 
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them. 

import pygame
import numpy as np
import pickle

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Game state
game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
blue = (0,102,255)

# Button dimensions
button_width, button_height = 200, 50
button_x, button_y = (width - button_width) // 2, height - button_height - 10

def draw_button():
    pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Start/Stop", True, black)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def draw_info_text():
    font = pygame.font.Font(None, 24)
    text = font.render("CTRL+S to Save | CTRL+L to Load game", True, white)
    text_rect = text.get_rect(center=(width // 2, height - button_height - 30))
    
    # Create a rectangle behind the text
    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 15
    rect_x = (width - rect_width) // 2
    rect_y = height - button_height - 40
    
    pygame.draw.rect(screen, blue, (rect_x, rect_y, rect_width, rect_height))
    screen.blit(text, text_rect)

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = game_state[(x - 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y - 1) % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y)     % n_cells_y] + \
                          game_state[(x - 1) % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x)     % n_cells_x, (y + 1) % n_cells_y] + \
                          game_state[(x + 1) % n_cells_x, (y + 1) % n_cells_y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

running = True
paused = False
tick_interval = 0.5  # Time interval between ticks in seconds
last_tick = pygame.time.get_ticks()  # Time tracking for simulation

def save_game_state(filename):
    with open(filename, 'wb') as file:
        pickle.dump(game_state, file)

def load_game_state(filename):
    global game_state
    with open(filename, 'rb') as file:
        game_state = pickle.load(file)

def toggle_pause():
    global paused
    paused = not paused

running = True
while running:
    current_time = pygame.time.get_ticks()
    # Calculate time passed since the last tick
    delta_time = (current_time - last_tick) / 1000.0  # Convert milliseconds to seconds

    if not paused and delta_time >= tick_interval:
        last_tick = current_time
        next_generation()

    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button()
    draw_info_text()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                toggle_pause()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_game_state("saved_game_state.pickle")
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                load_game_state("saved_game_state.pickle")

pygame.quit()

