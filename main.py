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

    character1.movement()
    character2.movement()

    character1.attack(character2)
    character2.attack(character1)

    character1.score(character2)
    character2.score(character1)
    
    if character1.xpos < WIDTH//2:
        if character1.reset_character_pos:
            character1.reset_position(1.2 * WIDTH//3, 0.96 * HEIGHT//2)
            character1.direction = 'right'
    else:
        if character1.reset_character_pos:
            character1.reset_position(1.65 *WIDTH//3, 0.96 * HEIGHT//2)
            character1.direction = 'left'

    if character2.xpos < WIDTH//2:
        if character2.reset_character_pos:
            character2.reset_position(1.2 * WIDTH//3, 0.96 * HEIGHT//2)
            character2.direction = 'right'
    else:
        if character2.reset_character_pos:
            character2.reset_position(1.65 *WIDTH//3, 0.96 * HEIGHT//2)
            character2.direction = 'left'

    zoomed_background = zoom(background_image, zoom_factor)
    x_offset, y_offset = center_background(zoomed_background)
    offset_x, offset_y = camera()
    Character.offset_x, Character.offset_y = offset_x, offset_y

    screen.blit(zoomed_background, (x_offset - offset_x, y_offset - offset_y))

    draw_hud(offset_x, offset_y)
    character1.draw(offset_x, offset_y)
    character2.draw(offset_x, offset_y)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
