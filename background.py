import pygame
from character import character1, character2

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
zoom_factor = 1.2

def zoom(image, zoom_factor):
    zoomed_image = pygame.transform.scale(image, (int(WIDTH * zoom_factor), int(HEIGHT * zoom_factor)))
    return zoomed_image

def camera():
    init_mid_x = 1.425 * WIDTH // 3
    init_mid_y = 0.99 * HEIGHT // 2

    mid_x = (character1.xpos + character2.xpos) / 2
    mid_y = (character1.ypos + character2.ypos) / 2

    offset_x = mid_x - init_mid_x
    offset_y = mid_y - init_mid_y
    offset_x = max(-200, min(200, offset_x))
    offset_y = max(-200, min(200, offset_y))
   
    return offset_x, offset_y

def center_background(zoomed_image):
    bg_width, bg_height = zoomed_image.get_size()
    x_offset = (WIDTH - bg_width) // 2 
    y_offset = (HEIGHT - bg_height) // 2 

    # Return the live offset values along with the offsets
    return x_offset, y_offset
