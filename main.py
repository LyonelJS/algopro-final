import pygame
import sys
from character import *
from hud import *
from background import *
from collision import *

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

# Frame rate
FPS = 120
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load("map.webp").convert_alpha()

# Main game loop
if __name__ == '__main__':
    running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    character1.update(character2)
    character2.update(character1)


    zoomed_background = zoom(background_image, zoom_factor)
    x_offset, y_offset = center_background(zoomed_background)
    offset_x, offset_y = camera()

    screen.blit(zoomed_background, (x_offset - offset_x, y_offset - offset_y))

    draw_hud(offset_x, offset_y)
    character1.draw(offset_x, offset_y)
    character2.draw(offset_x, offset_y)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
