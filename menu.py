import pygame
import sys

# Function to blur the background
def blur_surface(surface, amount):
    blur = pygame.transform.smoothscale(surface, (surface.get_width() // amount, surface.get_height() // amount))
    return pygame.transform.smoothscale(blur, surface.get_size())

# Menu function to the winner and points
def show_menu(screen, background_image, player1_points, player2_points, winner, WIDTH, HEIGHT):
    blurred_background = blur_surface(background_image, 10)
    winner_font = pygame.font.Font(None, 130)  
    points_font = pygame.font.Font(None, 120)  

    # Determine winner text color
    if winner == 1:
        winner_text = winner_font.render("Player 1 Wins!", True, (255, 0, 0))  # Red
    else:
        winner_text = winner_font.render("Player 2 Wins!", True, (0, 0, 255))  # Blue

    # Points text
    player1_points_text = points_font.render(f"{player1_points}", True, (255, 0, 0))  # Red
    player2_points_text = points_font.render(f"{player2_points}", True, (0, 0, 255))  # Blue

    # Button size
    button_width, button_height = 300, 80
    play_again_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2), (button_width, button_height))
    exit_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 + 120), (button_width, button_height))

    while True:
        screen.blit(blurred_background, (0, 0)) # Draw the blurred background

        # Draw the winning texts
        screen.blit(player1_points_text, (WIDTH // 2 - winner_text.get_width() - player1_points_text.get_width() + 50, HEIGHT // 2 - 200))  # Player 1 score
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 200))  # winner text
        screen.blit(player2_points_text, (WIDTH // 2 + winner_text.get_width() - 50, HEIGHT // 2 - 200))  # Player 2 score

        # Draw buttons
        pygame.draw.rect(screen, (0, 128, 0), play_again_rect)  # Green play again button
        pygame.draw.rect(screen, (128, 0, 0), exit_rect)  # Red exit button
        screen.blit(pygame.font.Font(None, 50).render("Play Again", True, (255, 255, 255)),
                    (WIDTH // 2 - 75, HEIGHT // 2 + 20)) # Write the text
        screen.blit(pygame.font.Font(None, 50).render("Exit", True, (255, 255, 255)),
                    (WIDTH // 2 - 35, HEIGHT // 2 + 140))

        # Change the cursor to a hand when hovering over buttons
        if play_again_rect.collidepoint(pygame.mouse.get_pos()) or exit_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Set cursor to pointer
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set cursor back to default

        pygame.display.flip()

        # Exit or play again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    return "play_again"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Pause menu function
def pause_menu(screen, background_image, WIDTH, HEIGHT):
    blurred_background = blur_surface(background_image, 10)
    button_font = pygame.font.Font(None, 80)

    # Button sizes
    button_width, button_height = 300, 80
    resume_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 - 60), (button_width, button_height))
    exit_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 + 60), (button_width, button_height))

    while True:
        screen.blit(blurred_background, (0, 0))

        # Draw the buttons
        pygame.draw.rect(screen, (0, 128, 0), resume_rect)  # Green resume button
        pygame.draw.rect(screen, (128, 0, 0), exit_rect)  # Red exit button
        resume_text = button_font.render("Resume", True, (255, 255, 255)) # The button texts
        exit_text = button_font.render("Exit", True, (255, 255, 255))

        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 70))

        # Change the cursor to a hand when hovering over buttons
        if resume_rect.collidepoint(pygame.mouse.get_pos()) or exit_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Set cursor to pointer
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Set cursor back to default

        pygame.display.flip()
        # Continue or exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    return "resume"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
