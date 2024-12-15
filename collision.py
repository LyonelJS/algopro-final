import pygame

WIDTH, HEIGHT = 1920, 1080

# Collision class to produce the collisions for every rect and return the value
class Collision:
    def __init__(self, name): # Sets the name of each rect initially
        self.name = name
    
    def rect(self, x, y, w, h): # Creates the rect based on the values given and returning the value
        rect = pygame.Rect(x, y, w, h)
        return rect

# All the rects with the names and values so that it can be used to check for collision
ground = Collision('ground').rect((WIDTH // 3), (1.14 * HEIGHT // 2), (WIDTH // 3), 1)
bottom = Collision('bottom').rect((WIDTH // 3), (1.14 * HEIGHT // 2) + 1, (WIDTH // 3), (HEIGHT // 2))
platform1 = Collision('platform1').rect(460, 470, 275, 1)
platform2 = Collision('platform2').rect(715, 370, 485, 1)
platform3 = Collision('platform3').rect(1190, 470, 275, 1)
border_bottom = Collision('border_bottom').rect(-1000, HEIGHT + 1000, WIDTH + 2000, 1000)
border_top = Collision('border_top').rect(-1000, HEIGHT - 4000, WIDTH + 2000, 1000)
border_left = Collision('border_left').rect(-3000, HEIGHT - 1000, 2000, HEIGHT + 2000)
border_right = Collision('border_right').rect(WIDTH + 1000, -1000, 2000, HEIGHT + 2000)

        
