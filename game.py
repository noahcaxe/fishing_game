import pygame
import random
import os

pygame.init()

BASE_DIR = os.path.dirname(__file__)

def load_image(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        print(f"Image not found: {path}")
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return None

# Create a window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Fishing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
player_x = window_width // 2 - 50
player_y = window_height - 120
player_width = 100
player_height = 120

# Fishing variables
fishing = False
fish_caught = False
fish_list = []
FISH_SPAWN_TIME = 100  # Time interval for fish spawning
fish_timer = 0
score = 0

time_limit = 60  # Game time in seconds
time_start = pygame.time.get_ticks()

# Load images
background_image = load_image("images/beach_background.png")
if background_image:
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

player_img = load_image("images/stickman.png")
if player_img:
    player_img = pygame.transform.scale(player_img, (player_width, player_height))

rod_img = load_image("images/rod.png")
if rod_img:
    rod_img = pygame.transform.scale(rod_img, (30, 100))

fish_img = load_image("images/fish.png")
if fish_img:
    fish_img = pygame.transform.scale(fish_img, (40, 30))

def spawn_fish():
    water_zone_start = int(window_height * 0.3)  # Only spawn in the water (30% from the top)
    fish_y = random.randint(water_zone_start, window_height - 50)
    fish_x = random.choice([-40, window_width + 40])  # Spawn outside left or right screen
    direction = 1 if fish_x < 0 else -1  # Set direction
    speed = random.uniform(2, 4) * direction  # Set speed with direction
    fish_list.append([fish_x, fish_y, speed])

font = pygame.font.Font(None, 36)

running = True
clock = pygame.time.Clock()
while running:
    window.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
        player_x += 5
    
    if keys[pygame.K_SPACE] and not fishing:
        fishing = True
    
    if keys[pygame.K_UP] and fishing:
        for fish in fish_list[:]:
            if player_x < fish[0] < player_x + player_width:
                fish_list.remove(fish)
                fish_caught = True
                score += 1
                print("+1 point")
        fishing = False
    
    # Update fish spawn timer
    fish_timer += 1
    if fish_timer >= FISH_SPAWN_TIME:
        spawn_fish()
        fish_timer = 0
    
    # Update fish movement
    for fish in fish_list[:]:
        fish[0] += fish[2]  # Move fish left or right
        if fish[0] < -50 or fish[0] > window_width + 50:
            fish_list.remove(fish)  # Remove fish if it goes off screen
    
    # Draw background
    if background_image:
        window.blit(background_image, (0, 0))
    
    # Draw player
    if player_img:
        window.blit(player_img, (player_x, player_y))
    
    # Draw rod
    if rod_img and fishing:
        rod_x = player_x + (player_width // 2) - (rod_img.get_width() // 2)
        rod_y = player_y - rod_img.get_height()
        window.blit(rod_img, (rod_x, rod_y))
    
    # Draw fish
    for fish in fish_list:
        window.blit(fish_img, (fish[0], fish[1]))
    
    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    window.blit(score_text, (10, 10))
    
    # Display timer
    time_elapsed = (pygame.time.get_ticks() - time_start) // 1000
    time_remaining = max(0, time_limit - time_elapsed)
    timer_text = font.render(f"Time: {time_remaining}", True, BLACK)
    window.blit(timer_text, (window_width // 2 - 40, 10))
    
    if time_remaining <= 0:
        running = False
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
