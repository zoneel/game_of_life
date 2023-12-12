# Game of Life Simulation

This project is a Python-based implementation of Conway's Game of Life using Pygame. The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. The game operates on a grid where cells live, die, or multiply based on simple rules.



## Design Patterns
- **Observer Pattern**: Implemented for handling user inputs such as mouse clicks and key presses. Each button's action is observed, allowing for distinct responses.
  
- **State Pattern**: Utilized for managing the game state, transitioning between generations, and updating cell states based on predefined rules.
  
- **Command Pattern**: Applied for defining button functionalities independently, allowing for encapsulation and ease of modification.

These design patterns enhance code organization, maintainability, and separation of concerns. They facilitate easier expansion and modification of the codebase, promoting a more structured and manageable Game of Life implementation in Pygame.

---

### Key Features
- **Grid Visualization:** Renders a grid representing the cells in the Game of Life.
- **Interactive Controls:** Pause/Resume functionality using a dedicated button and keyboard shortcuts.
- **Save/Load State:** Ability to save the current state of the grid and load it for future sessions.

### Running the Simulation
To run the simulation, ensure you have Python installed along with the necessary libraries. Execute the `game_of_life.py` script to start the simulation.

### Controls
- **Start/Stop Button:** Click the "Start/Stop" button to toggle between pausing and resuming the simulation.
- **Keyboard Shortcuts:**
  - `CTRL + S`: Save the current state of the simulation.
  - `CTRL + L`: Load a previously saved state of the simulation.

## Code Structure
The codebase comprises several functions responsible for rendering the grid, managing the game state, handling user input, and controlling the simulation loop.

---

Feel free to expand on this template by adding installation instructions, troubleshooting tips, or any other relevant information for users to better understand and use your Game of Life simulation.
