import pygame
import random

pygame.init()

#create a window

window_width = 800 
window_height = 600 
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Fishing Game")

# colors
WHITE = (255, 255, 255)

#game variables
player_x = window_width // 2
player_y = window_height - 100
player_width = 50
player_height = 50

#Download images 
background_image = pygame.image.load("beach_background.png")
background_image = pygame.transform.scale(background_image, (window_width, window_height))
player_img = pygame.image.load("stickman.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))
rod_img = pygame.image.load("rod.png")
rod_img = pygame.transform.scale(rod_img, (100, 10))
fish_img = pygame.image.load("fish.png")
fish_img = pygame.transform.scale(fish_img, (40, 30))