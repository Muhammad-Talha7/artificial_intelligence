import pygame
import numpy as np
import time
from collections import deque

GRID_SIZE = 10
CELL_SIZE = 70
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)  # Start point color
RED = (255, 0, 0)    # End point color
BLUE = (0, 0, 255)   # Path color
YELLOW = (255, 255, 0)  # Visited block color

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Editor")

# Create a 20x20 maze with boundary walls
maze = np.full((GRID_SIZE, GRID_SIZE), '#', dtype=str)
for i in range(1, GRID_SIZE-1):
    for j in range(1, GRID_SIZE-1):
        maze[i][j] = ' '

start_selected = False
end_selected = False
start_pos = None
end_pos = None
path = []
visited_nodes = []

def draw_grid():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (row, col) == start_pos:
                color = GREEN
            elif (row, col) == end_pos:
                color = RED
            elif (row, col) in path:
                color = BLUE
            elif (row, col) in visited_nodes:
                color = YELLOW
            else:
                color = BLACK if maze[row][col] == '#' else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GREY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def toggle_wall(pos):
    global start_selected, end_selected, start_pos, end_pos
    col, row = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if 1 <= row < GRID_SIZE-1 and 1 <= col < GRID_SIZE-1:  # Ignore boundary
        if not start_selected:
            start_pos = (row, col)
            maze[row][col] = 'A'
            start_selected = True
        elif not end_selected and (row, col) != start_pos:
            end_pos = (row, col)
            maze[row][col] = 'B'
            end_selected = True
        elif (row, col) != start_pos and (row, col) != end_pos:
            maze[row][col] = '#' if maze[row][col] == ' ' else ' '

def bfs_solve():
    global path, visited_nodes
    if not start_selected or not end_selected:
        return

    # Initialize queue with (position, path_taken)
    queue = deque([(start_pos, [start_pos])])
    visited = set()

    # Direction order: right, up, down, left
    directions = [(0, 1), (-1, 0), (1, 0), (0, -1)]

    while queue:
        current, curr_path = queue.popleft()

        if current in visited:
            continue
        visited.add(current)
        visited_nodes.append(current)

        draw_grid()
        pygame.display.flip()
        time.sleep(0.5)  # Delay for visualization

        if current == end_pos:
            path = curr_path
            return

        row, col = current
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            neighbor = (new_row, new_col)
            if (1 <= new_row < GRID_SIZE-1 and 1 <= new_col < GRID_SIZE-1 and
                maze[new_row][new_col] != '#' and neighbor not in visited):
                queue.append((neighbor, curr_path + [neighbor]))

def main():
    running = True
    while running:
        draw_grid()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    toggle_wall(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to print the maze
                    for row in maze:
                        print("".join(row))
                    print()
                elif event.key == pygame.K_s:  # Press 'S' to solve using BFS
                    bfs_solve()
    
    pygame.quit()

if __name__ == "__main__":
    main()