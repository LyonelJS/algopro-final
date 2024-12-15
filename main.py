import pygame
import sys
from character import *
from hud import *
from background import *
from collision import *
from menu import show_menu, pause_menu

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

# Frame rate
FPS = 120
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("map.webp").convert_alpha()

# Main game loop
if __name__ == '__main__':
    running = True
    while running:
        # Reset game
        character1.reset()
        character2.reset()

        while True:  # Inner game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Show pause menu when escape is clicked
                        pygame.mouse.set_visible(True)
                        menu_result = pause_menu(screen, background_image, WIDTH, HEIGHT)
                        if menu_result == "resume":
                            continue  # Resume the game
                        else:
                            running = False  # Exit the game loop
                            break

            # Check win conditions
            if character1.win:
                pygame.mouse.set_visible(True)
                if character2.reset_character_pos == False:
                    menu_result = show_menu(
                        screen, background_image, character1.point, character2.point, 1, WIDTH, HEIGHT
                    )
                    if menu_result == "play_again":
                        break  # Restart the game loop
                    else:
                        running = False
                        break
            elif character2.win:
                pygame.mouse.set_visible(True)
                if character1.reset_character_pos == False:
                    menu_result = show_menu(
                        screen, background_image, character1.point, character2.point, 2, WIDTH, HEIGHT
                    )
                    if menu_result == "play_again":
                        break  # Restart the game loop
                    else:
                        running = False
                        break

            # Update and draw the game
            pygame.mouse.set_visible(False)
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
