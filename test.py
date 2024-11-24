import pygame
import sys
import math

class Character:
    def __init__(self, name, xpos, ypos, controls, image, offset_x, offset_y):
        self.name = name
        self.xpos = xpos - offset_x
        self.ypos = ypos - offset_y
        self.controls = controls
        self.xmovement = True
        self.ymovement = True
        self.image = image  # Store current image
        self.original_image = image  # Store original image
        self.velocity_y = 0  # Vertical velocity (for jump and gravity)
        self.jump_count = 0  # To count jumps (double jump logic)
        self.width, self.height = 80, 80
        self.range_width, self.range_height = 80, 80
        self.collide_ground = True
        self.collide_platform = False
        self.collide_bottom = False
        self.platform_collidable = True
        self.range_width_adjustment, self.range_height_adjustment = 0, 0  # Initial height adjustment for the blue box
        self.range_x_adjustment, self.range_y_adjustment = 0, 0
        self.health = 1000
        self.inrange = False
        self.direction = None
        self.is_knocked_back = False
        self.knockback_speed = 10
        self.skill_counter = 0
        self.ulti_counter = 0
        self.point = 0
        self.gravity = True
        self.reset_character_pos = False
        self.collide_cooldown = False
        self.attack_available = True
        self.range = 'melee'
        self.win = False
        self.dash_cooldown = False


    def get_rect_hitbox(self):
        return pygame.Rect(self.xpos, self.ypos, self.width, self.height)
    
    def get_rect_range(self):
        return pygame.Rect(self.xpos + self.range_x_adjustment, self.ypos - self.range_y_adjustment, self.range_width - self.range_width_adjustment, self.range_height - self.range_height_adjustment)
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)  # Health can't go below 0

    

    def check_collision(self, ground, platforms, borders):
        for border in borders:
            if self.get_rect_hitbox().colliderect(border) and self.collide_cooldown == False:
                self.reset_character_pos = True
                self.collide_cooldown = True
                self.health = 0
                self.ulti_counter = 0
                self.xmovement = False
                self.ymovement = False
                character1.attack_available, character2.attack_available = False, False

            if self.get_rect_hitbox().colliderect(border_top):
                print('top')
            elif self.get_rect_hitbox().colliderect(border_bottom):
                print('bottom')
            elif self.get_rect_hitbox().colliderect(border_left):
                print('left')
            elif self.get_rect_hitbox().colliderect(border_right):
                print('right')



        if self.get_rect_hitbox().colliderect(ground):
            self.ypos = ground.top - self.height
            self.velocity_y = 0
            self.jump_count = 0
            self.collide_ground = True
            self.collide_platform = False
            self.collide_bottom = False
            self.platform_collidable = True
        elif self.get_rect_hitbox().colliderect(bottom):
            self.collide_bottom = True
            self.collide_ground = False
            self.collide_platform = False
        else:
            for platform in platforms:
                print(self.get_rect_hitbox().colliderect(platform))
                if self.get_rect_hitbox().colliderect(platform) and self.velocity_y > 0 and self.platform_collidable:
                    self.ypos = platform.top - self.height
                    self.velocity_y = 0
                    self.jump_count = 0
                    self.collide_ground = False
                    self.collide_platform = True
                    self.collide_bottom = False
                    self.platform_collidable = True
                    break

    def movement(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        keys = pygame.key.get_pressed()
        if self.controls == 'left':
            if keys[pygame.K_w] and self.velocity_y >= 0 and self.ymovement:
                
                self.direction = 'up'
                if self.jump_count < 2:
                    self.velocity_y = -20
                    self.jump_count += 1
                if keys[pygame.K_v] and self.velocity_y >= 25:
                    self.velocity_y = -25

            if keys[pygame.K_s] and self.ymovement:
                self.direction = 'down'

                if self.collide_platform:
                    self.velocity_y += 0.78
                    self.ypos += self.velocity_y
                    self.platform_collidable = False
                if keys[pygame.K_v]:
                    self.velocity_y = 25

            if keys[pygame.K_a] and not self.collide_bottom and self.xmovement:
                self.xpos -= 5
                self.direction = 'left'

                if keys[pygame.K_v]:
                    self.xpos -= 10

            if keys[pygame.K_d] and not self.collide_bottom and self.xmovement:
                self.xpos += 5
                self.direction = 'right'
                if keys[pygame.K_v]:
                    self.xpos += 10

        if self.controls == 'right':
            if keys[pygame.K_UP] and self.velocity_y >= 0 and self.ymovement:
                
                self.direction = 'up'
                if self.jump_count < 2:
                    self.velocity_y = -20
                    self.jump_count += 1
                if keys[pygame.K_m] and self.velocity_y >= 25:
                    self.velocity_y = -25

            if keys[pygame.K_DOWN] and self.ymovement:
    
                self.direction = 'down'
                if self.collide_platform:
                    self.velocity_y += 0.78
                    self.ypos += self.velocity_y
                    self.platform_collidable = False
                if keys[pygame.K_m]:
                    self.velocity_y = 25

            if keys[pygame.K_LEFT] and not self.collide_bottom and self.xmovement:
                self.xpos -= 5
                self.direction = 'left'
                if keys[pygame.K_m]:
                    self.xpos -= 10

            if keys[pygame.K_RIGHT] and not self.collide_bottom and self.xmovement:
                self.xpos += 5
                self.direction = 'right'
                if keys[pygame.K_m]:
                    self.xpos += 10
                

        self.player_direction()
        
        if self.gravity:
            self.velocity_y += 0.78
            self.ypos += self.velocity_y
            
        self.check_collision(ground, [platform1, platform2, platform3], [border_bottom, border_top, border_right, border_left])

    def reset_position(self, target_x, target_y):
        self.gravity = False  # Stop gravity for smooth movement
        self.velocity_y = 0  # Reset vertical velocity
            
            # Calculate the step distance
        x_step = abs(self.xpos - target_x) / 30
        y_step = abs(self.ypos - target_y) / 30
            
            # Move horizontally towards target_x
        if self.xpos < target_x:
            self.xpos += x_step
        elif self.xpos > target_x:
            self.xpos -= x_step

            # Move vertically towards target_y
        if self.ypos < target_y:
                self.ypos += y_step
        elif self.ypos > target_y:
            self.ypos -= y_step

            # When reaching the target, restore normal behavior
        if abs(self.xpos - target_x) < 5 and abs(self.ypos - target_y) < 5:
            self.xpos, self.ypos = target_x, target_y
            self.gravity = True  # Reactivate gravity
            self.reset_character_pos = False
            self.collide_cooldown = False
            self.ymovement = True
            self.xmovement = True
            self.attack_available = True
            character1.attack_available, character2.attack_available = True, True
    # Stop moving once the character is close enough to the target

    
    def check_hits(self, other):
        other.inrange = False
        if self.get_rect_range().colliderect(other.get_rect_hitbox()):
            other.inrange = True

    def player_direction(self):
        if self.range == 'melee':
            if self.direction == 'up':
                self.range_y_adjustment = self.range_height - 30
                self.range_height_adjustment = 30
                self.range_x_adjustment, self.range_width_adjustment = 0, 0
            if self.direction == 'down':
                self.range_y_adjustment = -self.range_height
                self.range_x_adjustment, self.range_width_adjustment = 0, 0
                self.range_height_adjustment = 30
            if self.direction == 'left':
                self.range_x_adjustment = 30 - self.range_width
                self.range_width_adjustment = 30
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.image = pygame.transform.flip(self.original_image, True, False)
            if self.direction == 'right':
                self.range_x_adjustment = self.range_width
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.range_width_adjustment = 30
                self.image = self.original_image
        if self.range == 'range':
            if self.direction == 'up':
                self.range_y_adjustment = self.range_height + 90
                self.range_height_adjustment = -90
                self.range_x_adjustment, self.range_width_adjustment = 0, 0
            if self.direction == 'down':
                self.range_y_adjustment = -self.range_height
                self.range_x_adjustment, self.range_width_adjustment = 0, 0
                self.range_height_adjustment = -90
            if self.direction == 'left':
                self.range_x_adjustment = -90 - self.range_width
                self.range_width_adjustment = -90
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.image = pygame.transform.flip(self.original_image, True, False)
            if self.direction == 'right':
                self.range_x_adjustment = self.range_width
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.range_width_adjustment = -90
                self.image = self.original_image

    def knockback(self, direction, multiplier):
    # Deceleration via division: gradually reduce knockback speed until it becomes very small
        health_lost = 1000 - self.health
        self.knockback_speed *= multiplier

        add_knockback = (health_lost/100) * multiplier**3

        decelerator = 1.1
        if self.knockback_speed > 0.1:  # Set a small threshold to stop knockback once it's nearly zero
            self.knockback_speed /= decelerator  # Divide the speed by 1.1 each time (you can adjust this divisor)

        knockback_amount = self.knockback_speed + add_knockback
    
        if direction == 'up':
            self.velocity_y = 0
            self.ypos -= knockback_amount * 2 
            self.ymovement = False

        if direction == 'down':
            self.velocity_y = 0
            self.ypos += knockback_amount * 2 
            self.ymovement = False

        if direction == 'right':
            self.xpos += knockback_amount 
            self.xmovement = False
        if direction == 'left':
            self.xpos -= knockback_amount 
            self.xmovement = False


    # Stop knockback when the speed is small enough
        if self.knockback_speed < 0.1:
            self.xmovement = True
            self.ymovement = True
            self.is_knocked_back = False  # End knockback when speed is low enough
            self.knockback_speed = 10

    def attack(self, other):
        self.check_hits(other)

        keys = pygame.key.get_pressed()
        multiplier = 1

        if self.controls == 'left':
            if keys[pygame.K_t] and self.attack_available:  # Check if the attack key is pressed and cooldown is not active
                if other.inrange:  # If the other character is within range
                    other.take_damage(50)
                    other.inrange = False
                    other.is_knocked_back = True
                    self.skill_counter += 1
                    self.ulti_counter += 1
                    self.skill_counter = min(3, self.skill_counter)
                    self.ulti_counter = min(8, self.ulti_counter)
                    self.attack_available = False

            if keys[pygame.K_g] and self.attack_available:
                self.range = 'range'
                if self.skill_counter == 3:
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 5
                        other.is_knocked_back = True
                        self.skill_counter = 0
                        self.attack_available = False
            if not keys[pygame.K_g]:
                multiplier = 1
                self.range = 'melee'

            if keys[pygame.K_f] and self.attack_available:
                if self.ulti_counter == 8:
                    self.ulti_counter = 0
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 6
                        other.is_knocked_back = True
                        self.attack_available = False
            

        if self.controls == 'right':
            if keys[pygame.K_i] and self.attack_available:  # Check if the attack key is pressed and cooldown is not active
                if other.inrange:  # If the other character is within range
                    other.take_damage(50)
                    other.inrange = False
                    other.is_knocked_back = True
                    self.skill_counter += 1
                    self.ulti_counter += 1
                    self.skill_counter = min(3, self.skill_counter)
                    self.ulti_counter = min(8, self.ulti_counter)
                    self.attack_available = False
            
            if keys[pygame.K_k] and self.attack_available:
                self.range = 'range'
                if self.skill_counter == 3:
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 5
                        other.is_knocked_back = True
                        self.attack_cooldown = True
                        self.skill_counter = 0
                        self.attack_available = False
            if not keys[pygame.K_k]:
                multiplier = 1
                self.range = 'melee'

            if keys[pygame.K_l] and self.attack_available:
                if self.ulti_counter == 8:
                    self.ulti_counter = 0
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 6
                        other.is_knocked_back = True
                        self.attack_available = False


        if other.is_knocked_back:
            other.knockback(self.direction, multiplier)
        elif not other.is_knocked_back and not other.reset_character_pos:
            self.attack_available = True
        
    def score(self, other):
        if self.health == 0:
            other.point += 1
            self.health = 1000
        if (self.point - other.point == 2 and self.point > other.point) or self.point == 3:
            self.win = True
        
    def draw(self):
        screen.blit(pygame.transform.scale(self.image, (self.width, self.height)), (int(self.xpos), int(self.ypos)))
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect_hitbox(), 2)
        pygame.draw.rect(screen, (0, 0, 255), self.get_rect_range(), 2)



# Check and handle hits between characters


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
character1_image = pygame.image.load("character1.png").convert_alpha()
character2_image = pygame.image.load("character2.jpg").convert_alpha()

# Initialize character objects
character1 = Character('character1', 1.2 * WIDTH // 3, HEIGHT // 2, 'left', character1_image, 0, 0)
character2 = Character('character2', 1.65 * WIDTH // 3, HEIGHT // 2, 'right', character2_image, 0, 0)

class Collision:
    def __init__(self, name):
        self.name = name
    
    def rect(self, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        return rect

zoom_factor = 1.2

# Update font sizes for better readability
score_font = pygame.font.Font(None, 48)  # Larger font for score
hud_font = pygame.font.Font(None, 36)  # Regular font for other HUD elements

# Define colors for HUD
health_bar_color = (255, 0, 0)  # Red for health
skill_bar_color = (0, 255, 0)  # Green for skill
background_bar_color = (50, 50, 50)  # Gray for background bar

def draw_hud():
    # Common properties
    health_bar_width = 300
    bar_height = 40
    max_skill_arc = 360  # Each skill step covers 120 degrees

    # Character 1's unique skill circle properties
    skill_circle_radius_1 = 30  # Radius for Character 1's skill counter
    skill_circle_thickness_1 = 10  # Thickness for Character 1's skill circle
    skill_circle_color_1 = (211, 211, 211)  # Green color for Character 1's skill circle

    ulti_circle_radius_1 = 50  # Radius for Character 1's skill counter
    ulti_circle_thickness_1 = 20  # Thickness for Character 1's skill circle

    # Character 2's unique skill circle properties
    skill_circle_radius_2 = 30  # Radius for Character 2's skill counter
    skill_circle_thickness_2 = 10  # Thickness for Character 2's skill circle
    skill_circle_color_2 = (211, 211, 211)  # Red color for Character 2's skill circle

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
        skill_bar_color = (0, 0, 255)  # Blue color when full
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
        skill_bar_color = (0, 0, 255)  # Blue color when full
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


    # Health bar for character 2
    pygame.draw.rect(screen, background_bar_color, (WIDTH - 297 - health_bar_width - 6, 177, health_bar_width + 6, bar_height + 6))
    pygame.draw.rect(screen, health_bar_color, (WIDTH - 600, 180, character2.health / (10/3), bar_height))
    health_text2 = hud_font.render(f"{character2.health}", True, (255, 255, 255))
    screen.blit(health_text2, (WIDTH - 370, 185))

    # Skill counter circle and arc for character 2
    skill_pos2 = (WIDTH - 350, 300)  # Position for Character 2's skill counter circle
    pygame.draw.circle(screen, background_bar_color, skill_pos2, skill_circle_radius_2 + 6, skill_circle_thickness_2 + 6)
    skill_progress2 = (character2.skill_counter / 3) * max_skill_arc  # Scale skill progress for 3 parts
    if skill_progress2 == 360:
        skill_bar_color = (255, 165, 0)  # Orange color when full
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
        skill_bar_color = (255, 165, 0)  # Blue color when full
        ulti_circle_thickness_2 = 35  # Thicker circle when full
        ulti_circle_radius_2 = 65  # Larger radius when full
    else:
        skill_bar_color = skill_circle_color_2  # Use green color for Character 1
    pygame.draw.arc(screen, skill_bar_color, 
                    (ulti_pos2[0] - ulti_circle_radius_2, ulti_pos2[1] - ulti_circle_radius_2, 
                     ulti_circle_radius_2 * 2, ulti_circle_radius_2 * 2), 
                    -0.5 * math.pi, (-0.5 * math.pi + math.radians(ulti_progress2)), ulti_circle_thickness_2)


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
    if offset_x > 0:
        offset_x = min(200, offset_x)
    elif offset_x < 0:
        offset_x = max(-200, offset_x)

    if offset_y > 0:
        offset_y = min(200, offset_y)
    elif offset_y < 0:
        offset_y = max(-200, offset_y)
    return offset_x, offset_y

def center_background(zoomed_image):
    bg_width, bg_height = zoomed_image.get_size()
    x_offset = (WIDTH - bg_width) // 2 
    y_offset = (HEIGHT - bg_height) // 2 
    return x_offset, y_offset


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    zoomed_background = zoom(background_image, zoom_factor)
    x_offset, y_offset = center_background(zoomed_background)
    offset_x, offset_y = camera()

    screen.blit(zoomed_background, (x_offset - offset_x, y_offset - offset_y))
    ground = Collision('ground').rect((WIDTH // 3) - offset_x, (1.14 * HEIGHT // 2) - offset_y, (WIDTH // 3), 1)
    bottom = Collision('bottom').rect((WIDTH // 3) - offset_x, (1.14 * HEIGHT // 2) + 1 - offset_y, (WIDTH // 3), (HEIGHT // 2))
    platform1 = Collision('platform1').rect(460, 470, 275, 1)
    platform2 = Collision('platform2').rect(715, 370, 485, 1)
    platform3 = Collision('platform3').rect(1190, 470, 275, 1)
    border_bottom = Collision('border_bottom').rect(-1000, HEIGHT + 1000, WIDTH + 2000, 1000)
    border_top = Collision('border_top').rect(-1000, HEIGHT - 4000, WIDTH + 2000, 1000)
    border_left = Collision('border_left').rect(-3000, HEIGHT - 1000, 2000, HEIGHT + 2000)
    border_right = Collision('border_right').rect(WIDTH + 1000, -1000, 2000, HEIGHT + 2000)

    character1 = Character('character1', 1.2 * WIDTH // 3, HEIGHT // 2, 'left', character1_image, offset_x, offset_y)
    character2 = Character('character2', 1.65 * WIDTH // 3, HEIGHT // 2, 'right', character2_image, offset_x, offset_y)

    character1.movement()
    character2.movement()

    character1.attack(character2)
    character2.attack(character1)

    character1.score(character2)
    character2.score(character1)

    if character1.reset_character_pos:
        character1.reset_position(1.2 * WIDTH//3, 0.96 * HEIGHT//2)
    if character2.reset_character_pos:
        character2.reset_position(1.65 *WIDTH//3, 0.96 * HEIGHT//2)

    draw_hud()
    character1.draw()
    character2.draw()
    pygame.draw.rect(screen, (255, 0, 0), bottom, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
