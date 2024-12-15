import pygame
from character import character1, character2 # Import the characters

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
zoom_factor = 1.2

def zoom(image, zoom_factor): # Zooms the background image
    zoomed_image = pygame.transform.scale(image, (int(WIDTH * zoom_factor), int(HEIGHT * zoom_factor)))
    return zoomed_image

def camera(): # Sets the offset for the camera
    init_mid_x = 1.425 * WIDTH // 3 # The initial average or midpoint of the two characters
    init_mid_y = 0.99 * HEIGHT // 2

    mid_x = (character1.xpos + character2.xpos) / 2 # Calculates the change of the average of the two characters in real time
    mid_y = (character1.ypos + character2.ypos) / 2

    offset_x = mid_x - init_mid_x # Calculates the coordinates of the midpoint where the camera should be
    offset_y = mid_y - init_mid_y
    offset_x = max(-200, min(200, offset_x)) # Sets the max and the min of the camera so that it doesnt exceed the background image
    offset_y = max(-200, min(200, offset_y))
   
    return offset_x, offset_y # Return the offsets

def center_background(zoomed_image): # Center the background initially
    bg_width, bg_height = zoomed_image.get_size()
    x_offset = (WIDTH - bg_width) // 2 
    y_offset = (HEIGHT - bg_height) // 2 

    # Return the live offset values along with the offsets
    return x_offset, y_offset
