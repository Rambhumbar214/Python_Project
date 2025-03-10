import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic vs. Zombie")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

# Set up sprite groups
all_sprites = pygame.sprite.Group()
cars = pygame.sprite.Group()

# Player (Zombie) class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep the player within the screen boundaries
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

# Car (Obstacle) class
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(3, 6)

    def update(self, *args, **kwargs):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH)
            self.speed = random.randint(3, 6)

# Create player instance
player = Player()
all_sprites.add(player)

# Create car instances
for _ in range(5):
    car = Car()
    all_sprites.add(car)
    cars.add(car)

# Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # End the game on close

    keys = pygame.key.get_pressed()
    all_sprites.update(keys)

    # Check for collisions
    if pygame.sprite.spritecollide(player, cars, False):
        running = False  # End the game on collision

    # Fill the screen with white
    window.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(window)

    # Update the display
    pygame.display.flip()

pygame.quit()

# Run the game
if __name__ == "__main__":
    run_game()
