import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Generate a simple Sudoku grid (placeholder)
def generate_grid():
    return [[random.randint(1, 9) if random.random() < 0.3 else 0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid(win, grid, selected):
    win.fill(WHITE)
    for i in range(GRID_SIZE + 1):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)
    
    font = pygame.font.Font(None, 40)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                text = font.render(str(grid[r][c]), True, BLACK)
                win.blit(text, (c * CELL_SIZE + 15, r * CELL_SIZE + 10))
    
    if selected:
        pygame.draw.rect(win, BLUE, (selected[1] * CELL_SIZE, selected[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def is_valid(grid, row, col, num):
    for i in range(GRID_SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    box_x, box_y = col // 3 * 3, row // 3 * 3
    for i in range(3):
        for j in range(3):
            if grid[box_y + i][box_x + j] == num:
                return False
    return True

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    grid = generate_grid()
    selected = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected = (y // CELL_SIZE, x // CELL_SIZE)
            elif event.type == pygame.KEYDOWN and selected:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    row, col = selected
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
        
        draw_grid(win, grid, selected)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
