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

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class InfoButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 102, 255), self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class GameState:
    def __init__(self, n_cells_x, n_cells_y):
        self.n_cells_x = n_cells_x
        self.n_cells_y = n_cells_y
        self.game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

    def next_generation(self):
        new_state = np.copy(self.game_state)
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                n_neighbors = np.sum(self.game_state[x-1:x+2, y-1:y+2]) - self.game_state[x, y]
                if self.game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif self.game_state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1
        self.game_state = new_state

class Grid:
    def __init__(self, width, height, n_cells_x, n_cells_y):
        self.width = width
        self.height = height
        self.cell_width = width // n_cells_x
        self.cell_height = height // n_cells_y

    def draw(self, screen):
        for y in range(0, self.height, self.cell_height):
            for x in range(0, self.width, self.cell_width):
                cell = pygame.Rect(x, y, self.cell_width, self.cell_height)
                pygame.draw.rect(screen, (128, 128, 128), cell, 1)

class Game:
    def __init__(self, width, height, n_cells_x, n_cells_y):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.grid = Grid(width, height, n_cells_x, n_cells_y)
        self.game_state = GameState(n_cells_x, n_cells_y)
        self.button = Button((width - 200) // 2, height - 60, 485, 50, "Start/Stop", self.toggle_pause)
        self.info_button = InfoButton(10, height - 60, 400, 50, "CTRL+S to Save | CTRL+L to Load game")
        self.paused = False
        self.tick_interval = 0.1
        self.last_tick = pygame.time.get_ticks()

    def run(self):
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_tick) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            if not self.paused and delta_time >= self.tick_interval:
                self.last_tick = current_time
                self.game_state.next_generation()

            self.screen.fill((255, 255, 255))
            self.grid.draw(self.screen)
            self.draw_cells()
            self.button.draw(self.screen)
            self.info_button.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def handle_click(self, pos):
        if self.button.rect.collidepoint(pos):
            self.button.action()

        else:
            x, y = pos[0] // self.grid.cell_width, pos[1] // self.grid.cell_height
            self.game_state.game_state[x, y] = not self.game_state.game_state[x, y]

    def handle_key(self, key):
        if key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_game_state("saved_game_state.pickle")
        elif key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.load_game_state("saved_game_state.pickle")

    def draw_cells(self):
        for y in range(self.game_state.n_cells_y):
            for x in range(self.game_state.n_cells_x):
                cell = pygame.Rect(x * self.grid.cell_width, y * self.grid.cell_height,
                                   self.grid.cell_width, self.grid.cell_height)
                if self.game_state.game_state[x, y] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), cell)

    def toggle_pause(self):
        self.paused = not self.paused

    def save_game_state(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.game_state.game_state, file)

    def load_game_state(self, filename):
        with open(filename, 'rb') as file:
            self.game_state.game_state = pickle.load(file)

game = Game(800, 600, 40, 30)
game.run()


