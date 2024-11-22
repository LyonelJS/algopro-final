import pygame
import math
from character import *

def draw_hud(offset_x, offset_y):
    # Update font sizes for better readability
    score_font = pygame.font.Font(None, 48)  # Larger font for score
    hud_font = pygame.font.Font(None, 36)  # Regular font for other HUD elements

    # Define colors for HUD
    health_bar_color = (255, 0, 0)  # Red for health
    skill_bar_color = (0, 255, 0)  # Green for skill
    background_bar_color = (50, 50, 50)  # Gray for background bar
    # Common properties
    health_bar_width = 300
    bar_height = 40
    max_skill_arc = 360  # Each skill step covers 120 degrees

    # Character 1's unique skill circle properties
    skill_circle_radius_1 = 30  # Radius for Character 1's skill counter
    skill_circle_thickness_1 = 10  # Thickness for Character 1's skill circle
    skill_circle_color_1 = (211, 211, 211)  # Red color for Character 2's skill circle


    ulti_circle_radius_1 = 50  # Radius for Character 1's skill counter
    ulti_circle_thickness_1 = 20  # Thickness for Character 1's skill circle

    # Character 2's unique skill circle properties
    skill_circle_radius_2 = 30  # Radius for Character 2's skill counter
    skill_circle_thickness_2 = 10  # Thickness for Character 2's skill circle
    skill_circle_color_2 = (211, 211, 211)  # Green color for Character 1's skill circle


    ulti_circle_radius_2 = 50  # Radius for Character 1's skill counter
    ulti_circle_thickness_2 = 20  # Thickness for Character 1's skill circle

    # Draw Character 1's HUD
    # Score and health bar for character 1
    
    if character1.win:
        screen.blit(score_font.render(f"YOU WIN", True, (0, 0, 255)), (WIDTH // 3 - 100, 120))
    else:
        screen.blit(score_font.render(f"Score: {character1.point}", True, (0, 0, 255)), (WIDTH // 3 - 100, 120))


    # Health bar for character 1
    pygame.draw.rect(screen, background_bar_color, (297, 177, health_bar_width + 6, bar_height + 6))
    pygame.draw.rect(screen, health_bar_color, (300, 180, character1.health / (10/3), bar_height))
    health_text1 = hud_font.render(f"{character1.health}", True, (255, 255, 255))
    screen.blit(health_text1, (310, 185))

    pos_text1 = hud_font.render(f"Health: {character1.xpos}{character1.ypos}", True, (255, 255, 255))
    screen.blit(pos_text1, (WIDTH//2, HEIGHT//2))
    
    # Skill counter circle and arc for character 1
    skill_pos1 = (350, 300)  # Position for Character 1's skill counter circle
    pygame.draw.circle(screen, background_bar_color, skill_pos1, skill_circle_radius_1 + 6, skill_circle_thickness_1 + 6)
    skill_progress1 = (character1.skill_counter / 3) * max_skill_arc  # Scale skill progress for 3 parts
    if skill_progress1 == 360:
        skill_bar_color = (255, 165, 0) # orange color when full
        skill_circle_thickness_1 = 25  # Thicker circle when full
        skill_circle_radius_1 = 45  # Larger radius when full
    else:
        skill_bar_color = skill_circle_color_1  # Use green color for Character 1
    pygame.draw.arc(screen, skill_bar_color, 
                    (skill_pos1[0] - skill_circle_radius_1, skill_pos1[1] - skill_circle_radius_1, 
                     skill_circle_radius_1 * 2, skill_circle_radius_1 * 2), 
                    -0.5 * math.pi, (-0.5 * math.pi + math.radians(skill_progress1)), skill_circle_thickness_1)
    
    #ult bar for char1
    ulti_pos1 = (500, 300)  # Position for Character 1's skill counter circle
    pygame.draw.circle(screen, background_bar_color, ulti_pos1, ulti_circle_radius_1 + 6, ulti_circle_thickness_1 + 6)
    ulti_progress1 = (character1.ulti_counter / 8) * max_skill_arc  # Scale skill progress for 3 parts
    if ulti_progress1 == 360:
        skill_bar_color = (255, 165, 0)  # orange color when full
        ulti_circle_thickness_1 = 35  # Thicker circle when full
        ulti_circle_radius_1 = 65  # Larger radius when full
    else:
        skill_bar_color = skill_circle_color_1  # Use green color for Character 1
    pygame.draw.arc(screen, skill_bar_color, 
                    (ulti_pos1[0] - ulti_circle_radius_1, ulti_pos1[1] - ulti_circle_radius_1, 
                     ulti_circle_radius_1 * 2, ulti_circle_radius_1 * 2), 
                    -0.5 * math.pi, (-0.5 * math.pi + math.radians(ulti_progress1)), ulti_circle_thickness_1)


    # Draw Character 2's HUD
    # Score and health bar for character 2
    if character2.win:
        screen.blit(score_font.render(f"YOU WIN", True, (255, 0, 0)), (2 * WIDTH // 3 - 100, 120))
    else:
        screen.blit(score_font.render(f"Score: {character2.point}", True, (255, 0, 0)), (2 * WIDTH // 3 - 100, 120))

    health_lost = 1000 - character2.health
    # Health bar for character 2
    pygame.draw.rect(screen, background_bar_color, (WIDTH - 297 - health_bar_width - 6, 177, health_bar_width + 6, bar_height + 6))
    pygame.draw.rect(screen, health_bar_color, (WIDTH - 600 + health_lost / (10/3), 180, character2.health / (10/3), bar_height))
    health_text2 = hud_font.render(f"{character2.health}", True, (255, 255, 255))
    screen.blit(health_text2, (WIDTH - 370, 185))

    # Skill counter circle and arc for character 2
    skill_pos2 = (WIDTH - 350, 300)  # Position for Character 2's skill counter circle
    pygame.draw.circle(screen, background_bar_color, skill_pos2, skill_circle_radius_2 + 6, skill_circle_thickness_2 + 6)
    skill_progress2 = (character2.skill_counter / 3) * max_skill_arc  # Scale skill progress for 3 parts
    if skill_progress2 == 360:
        skill_bar_color = (0, 0, 255)  # blue color when full
        skill_circle_thickness_2 = 25  # Thicker circle when full
        skill_circle_radius_2 = 45  # Larger radius when full
    else:
        skill_bar_color = skill_circle_color_2  # Use red color for Character 2
    pygame.draw.arc(screen, skill_bar_color, 
                    (skill_pos2[0] - skill_circle_radius_2, skill_pos2[1] - skill_circle_radius_2, 
                     skill_circle_radius_2 * 2, skill_circle_radius_2 * 2), 
                    -0.5 * math.pi, (-0.5 * math.pi + math.radians(skill_progress2)), skill_circle_thickness_2)
    
    #ult bar for char2
    ulti_pos2 = (WIDTH - 500, 300)  # Position for Character 1's skill counter circle
    pygame.draw.circle(screen, background_bar_color, ulti_pos2, ulti_circle_radius_2 + 6, ulti_circle_thickness_2 + 6)
    ulti_progress2 = (character2.ulti_counter / 8) * max_skill_arc  # Scale skill progress for 3 parts
    if ulti_progress2 == 360:
        skill_bar_color = (0, 0, 255) # Blue color when full
        ulti_circle_thickness_2 = 35  # Thicker circle when full
        ulti_circle_radius_2 = 65  # Larger radius when full
    else:
        skill_bar_color = skill_circle_color_2  # Use green color for Character 1
    pygame.draw.arc(screen, skill_bar_color, 
                    (ulti_pos2[0] - ulti_circle_radius_2, ulti_pos2[1] - ulti_circle_radius_2, 
                     ulti_circle_radius_2 * 2, ulti_circle_radius_2 * 2), 
                    -0.5 * math.pi, (-0.5 * math.pi + math.radians(ulti_progress2)), ulti_circle_thickness_2)
    
    if character1.xpos > WIDTH or character1.xpos + 70 < 0 or character1.ypos > HEIGHT or character1.ypos + 170 < 0:
        pygame.draw.circle(screen, (0, 0, 255), (max(250, min(WIDTH - 250, character1.xpos - offset_x + 50)), max(150, min(character1.ypos - offset_y, HEIGHT - 150))), 30, 30)
    
    if character2.xpos > WIDTH or character2.xpos < 0 or character2.ypos > HEIGHT or character2.ypos + 170 < 0:
        pygame.draw.circle(screen, (255, 165, 0), (max(250, min(WIDTH - 250, character2.xpos - offset_x + 50)), max(150, min(character2.ypos - offset_y, HEIGHT - 150))), 30, 30)
    