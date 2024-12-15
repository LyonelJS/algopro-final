import pygame
from collision import * # Impoort the collisions to check for collisions

WIDTH, HEIGHT = 1920, 1080 # Set the screen height and width
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")
# Initialize sound mixer
pygame.mixer.init()
character1_attack1_sound = pygame.mixer.Sound("sound/character1_attack1_sound.mp3")  # Adjust the path to your sound file
character1_attack2_sound = pygame.mixer.Sound("sound/character1_attack2_sound.mp3")  # Adjust the path to your sound file
character2_attack1_sound = pygame.mixer.Sound("sound/character2_attack1_sound.mp3")  # Adjust the path to your sound file
character2_attack2_sound = pygame.mixer.Sound("sound/character2_attack2_sound.mp3")  # Adjust the path to your sound file
jump_sound = pygame.mixer.Sound("sound/jump_sound.mp3")  # Adjust the path to your sound file
land_sound = pygame.mixer.Sound("sound/land_sound.mp3")  # Adjust the path to your sound file
jump_sound.set_volume(0.2)
land_sound.set_volume(0.2)

death_sound = pygame.mixer.Sound("sound/death_sound.mp3")  # Adjust the path to your sound file

# Load all the necessary animations for character 1
character1_walk = [pygame.image.load(f"character1/walk/walk_{i}.png").convert_alpha() for i in range(1, 6)]
character1_idle = [pygame.image.load(f"character1/idle/idle_{i}.png").convert_alpha() for i in range(1, 7)]
character1_jump = [pygame.image.load(f"character1/jump/jump_{i}.png").convert_alpha() for i in range(1, 9)]
character1_dead = [pygame.image.load(f"character1/dead/dead_{i}.png").convert_alpha() for i in range(1, 6)]
# Attack1 animation
character1_attack1_side = [pygame.image.load(f"character1/attack_1/side/attack_{i}.png").convert_alpha() for i in range(1, 4)]
character1_attack1_up = [pygame.image.load(f"character1/attack_1/up/attack_{i}.png").convert_alpha() for i in range(1, 4)]
# Attack2 animation
character1_attack2_side = [pygame.image.load(f"character1/attack_2/side/attack_{i}.png").convert_alpha() for i in range(1, 14)]
character1_attack2_up = [pygame.image.load(f"character1/attack_2/up/attack_{i}.png").convert_alpha() for i in range(1, 12)]
# Ult animation
character1_ult_side = [pygame.image.load(f"character1/ult/side/attack_{i}.png").convert_alpha() for i in range(1, 10)]
character1_ult_up = [pygame.image.load(f"character1/ult/up/attack_{i}.png").convert_alpha() for i in range(1, 10)]

character1_hurt = [pygame.image.load(f"character1/hurt/hurt_{i}.png").convert_alpha() for i in range(1, 3)]
character1_run = [pygame.image.load(f"character1/run/run_{i}.png").convert_alpha() for i in range(1, 8)]

# Load all the necessary animations for character 2
character2_walk = [pygame.transform.flip(pygame.image.load(f"character2/walk/walk_{i}.png").convert_alpha(), True, False) for i in range(1, 7)]
character2_idle = [pygame.transform.flip(pygame.image.load(f"character2/idle/idle_{i}.png").convert_alpha(), True, False) for i in range(1, 8)]
character2_jump = [pygame.transform.flip(pygame.image.load(f"character2/jump/jump_{i}.png").convert_alpha(), True, False) for i in range(1, 9)]
character2_dead = [pygame.transform.flip(pygame.image.load(f"character2/dead/dead_{i}.png").convert_alpha(), True, False) for i in range(1, 4)]
# Attack1 animation
character2_attack1_side = [pygame.image.load(f"character2/attack_1/side/attack_{i}.png").convert_alpha() for i in range(1, 7)]
character2_attack1_up = [pygame.image.load(f"character2/attack_1/up/attack_{i}.png").convert_alpha() for i in range(1, 7)]
# Attack2 animation
character2_attack2_side = [pygame.image.load(f"character2/attack_2/side/attack_{i}.png").convert_alpha() for i in range(1, 14)]
character2_attack2_up = [pygame.image.load(f"character2/attack_2/up/attack_{i}.png").convert_alpha() for i in range(1, 14)]
# Ult animation
character2_ult_side = [pygame.image.load(f"character2/ult/side/attack_{i}.png").convert_alpha() for i in range(1, 9)]
character2_ult_up = [pygame.image.load(f"character2/ult/up/attack_{i}.png").convert_alpha() for i in range(1, 8)]

character2_hurt = [pygame.image.load(f"character2/hurt/hurt_{i}.png").convert_alpha() for i in range(1, 4)]
character2_run = [pygame.image.load(f"character2/run/run_{i}.png").convert_alpha() for i in range(1, 8)]

# Define the Character class
class Character:
    def __init__(self, name, xpos, ypos, controls, animations): # Init variables
        self.name = name # Name of the character
        self.xpos = xpos # Position of the character
        self.ypos = ypos 
        self.controls = controls # Controls of the character (left or right)
        self.xmovement = True # Allow movement or not
        self.ymovement = True
        self.velocity_y = 0  # Vertical velocity (for jump and gravity)
        self.jump_count = 0  # Jump counter (double jump logic)
        self.width, self.height = 80, 80 # Size of the character
        self.range_width, self.range_height = 80, 80 # Range of the character
        self.collide_ground = True # Collision check
        self.collide_platform = False
        self.collide_bottom = False
        self.platform_collidable = True # Allow the collision with platform
        self.range_width_adjustment, self.range_height_adjustment = 0, 0  # Initial height adjustment for the range for attack 2
        self.range_x_adjustment, self.range_y_adjustment = 0, 0 # Initial position for the range for attack 2
        self.health = 1000 # Character health
        self.inrange = False # Range check
        self.direction = None # Direction check
        self.is_knocked_back = False # Knockback check
        self.knockback_direction = None # Initial knockback direction (none)
        self.knockback_speed = 10 # Initial knockback speed
        self.skill_counter = 0 # Skill counter
        self.ulti_counter = 0 # Ult counter
        self.point = 0 # Character score
        self.gravity = True # Activate gravity initially
        self.reset_character_pos = False # Reset the character's position
        self.collide_cooldown = False # Make sure to only collide with the border rect only once
        self.attack_available = True # Attack availability check
        self.attack_cooldown = False # Attack cooldown for attack 1
        self.attack2_cooldown = False # Attack cooldown for attack 2
        self.range = 'melee' # Initial range is melee
        self.win = False # Checks if the character wins
        self.score_added = False # Make sure to only add 1 point per death
        self.prev_key = None # previous direction of the player
        self.in_the_air = False # Checks if the player is in the air (not colliding with anything)
        self.run = False # Checks movement for animation logic
        self.alive = True
        self.is_attacking = False
        self.is_attacking2 = False
        self.attacking_range = False
        self.is_ult = False
        self.walking = False
        self.hurt = False 

        self.x_offset = 0 # Initial x offset
        self.sprint_time = 1000 # Dash time
        self.sprint_reset_cooldown = False # Sets a cooldown for the dash if the dash time reaches 0
        self.timer = 1000 # Sets the cooldown timer

        self.animations = animations # Changes the animation according to the character current animation
        self.current_action = 'idle' # Default animation to idle
        self.frame_index = 0 # animation frame index
        self.image = self.animations[self.current_action] # Current image in the animation
        self.beam_height = HEIGHT # For respawn 
        self.beam_width = 120
        self.transparency = 50
        self.animation_speed = 0.1
        self.sound_played = False

# Create the character's hitbox rect
    def get_rect_hitbox(self):
        return pygame.Rect(self.xpos + 30, self.ypos , self.width - 40, self.height)
    
    # Create the character's range rect
    def get_rect_range(self):
        return pygame.Rect(self.xpos + self.range_x_adjustment + 30, self.ypos - self.range_y_adjustment, self.range_width - self.range_width_adjustment - 40, self.range_height - self.range_height_adjustment)
    # Sets the health of the character based on the damage taken
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)  # Health can't go below 0
        self.check_health()
    # Checks the health of the character
    def check_health(self):
        if self.health == 0: # Checks if the health is 0
            self.alive = False # Adjusts the character attributes when losing a round
            self.set_action('dead')   
            self.reset_character_pos = True
            self.ulti_counter = 0
            self.xmovement = False
            self.ymovement = False
            character1.attack_available, character2.attack_available = False, False
            self.in_the_air = False
            death_sound.play()
        
        elif self.health > 0: # Restore the character attributes when the health is more than 0
            self.alive = True
            self.set_action('idle')   
            self.reset_character_pos = False
            self.xmovement = True
            self.ymovement = True
            character1.attack_available, character2.attack_available = True, True
    # Checks the character hitbox rect collision with the map
    def check_collision(self, ground, platforms, borders):
        for border in borders:
            if self.get_rect_hitbox().colliderect(border) and self.collide_cooldown == False:
                self.reset_character_pos = True
                self.collide_cooldown = True
                self.health = 0                
                self.check_health()
        
        if self.get_rect_hitbox().colliderect(ground):
            self.ypos = ground.top - self.height
            self.velocity_y = 0
            self.jump_count = 0
            self.collide_ground = True
            self.collide_platform = False
            self.collide_bottom = False
            self.platform_collidable = True
            self.in_the_air = False
            if self.sound_played == False:
                land_sound.play()
                self.sound_played = True
        elif self.get_rect_hitbox().colliderect(bottom):
            self.collide_bottom = True
            self.collide_ground = False
            self.collide_platform = False
            self.in_the_air = False
            if self.sound_played == False:
                land_sound.play()
                self.sound_played = True
        else:
            for platform in platforms:                
                if self.get_rect_hitbox().colliderect(platform):
                    self.collide_platform = True
                    self.collide_ground = False
                    self.collide_bottom = False
                    if self.velocity_y > 0 and self.platform_collidable:
                        self.ypos = platform.top - self.height
                        self.velocity_y = 0
                        self.jump_count = 0 
                        self.platform_collidable = True
                        self.in_the_air = False
                        if self.sound_played == False:
                            land_sound.play()
                            self.sound_played = True
                        break
    # For animation logic, checks which animation is prioritized
    def check_movement(self):
        if self.alive:
            if self.is_attacking:
                if self.direction == 'up':
                    self.set_action('attack1_up')
                elif self.direction == 'left' or 'right':
                    self.set_action('attack1_side')
            if self.is_attacking2:
                if self.direction == 'up':
                    self.set_action('attack2_up')
                elif self.direction == 'left' or 'right':
                    self.set_action('attack2_side')
            if self.is_ult:
                if self.direction == 'up':
                    self.set_action('ult_up')
                elif self.direction == 'left' or 'right':
                    self.set_action('ult_side')
            if self.hurt:
                self.set_action('hurt')
            if self.in_the_air and not self.is_attacking and not self.is_attacking2 and not self.is_ult and not self.hurt:
                self.set_action('jump')
            if self.run and not self.in_the_air and not self.is_attacking and not self.is_attacking2 and not self.is_ult and not self.hurt:
                self.set_action('run')
            if self.walking and not self.in_the_air and not self.is_attacking and not self.is_attacking2 and not self.is_ult and not self.hurt and not self.run:
                self.set_action('walk')
            if not self.walking and not self.in_the_air and not self.is_attacking and not self.is_attacking2 and not self.is_ult and not self.hurt and not self.run:
                self.set_action('idle')
    # Handles character movement
    def movement(self):
        keys = pygame.key.get_pressed() # Get inputs from the player

        # Left character controls
        if self.controls == 'left':
            if keys[pygame.K_w] and self.velocity_y >= 0 and self.ymovement: # Character 1 jump
                self.direction = 'up'
                if self.jump_count < 2:
                    if not self.hurt:
                        self.velocity_y = -16
                    if self.hurt:
                        self.velocity_y = -10
                    self.jump_count += 1
                    self.in_the_air = True
                    self.frame_index = 0
                    self.platform_collidable = True
                    jump_sound.play()
                    self.sound_played = False
                if keys[pygame.K_v] and self.velocity_y >= 18 and self.sprint_time > 0: # Dash
                    self.velocity_y = -20
                    self.sprint_time -= 200
                    self.run = True
                    jump_sound.play()


            if keys[pygame.K_s] and self.ymovement: # Character 1 move down
                self.direction = 'down'
                if self.collide_platform:
                    self.in_the_air = True
                    self.frame_index = 5
                    self.velocity_y += 0.78
                    self.ypos += self.velocity_y
                    self.platform_collidable = False
                    self.sound_played = False

                if keys[pygame.K_v] and self.sprint_time > 0: # Dash
                    self.velocity_y = 25
                    self.sprint_time -= 200
                    self.run = True
                    jump_sound.play()

            if keys[pygame.K_a] and not self.collide_bottom and self.xmovement: # Character 1 move left
                self.xpos -= 5
                self.direction = 'left'
                self.walking = True
                if keys[pygame.K_v] and self.sprint_time > 0: # Dash
                    self.xpos -= 10
                    self.sprint_time -= 20
                    self.run = True
                    jump_sound.play()

            if keys[pygame.K_d] and not self.collide_bottom and self.xmovement: # Character 1 move right
                self.xpos += 5
                self.direction = 'right'
                self.walking = True
                if keys[pygame.K_v] and self.sprint_time > 0: # Dash
                    self.xpos += 10
                    self.sprint_time -= 20
                    self.run = True
                    jump_sound.play()

            if not keys[pygame.K_a] and not keys[pygame.K_d]: # For animation
                self.walking = False
            # If not sprinting, reset the sprint time
            if (not keys[pygame.K_v] or (not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s])) and not self.sprint_reset_cooldown :
                self.sprint_time += 200
                self.run = False
            if self.sprint_time <= 0: # Set a cooldown if sprint time reaches 0
                self.sprint_reset_cooldown = True
                self.timer -= 10
                self.run = False

            if self.timer <= 0: # Reset the timer and remove the cooldown if the timer is done
                self.timer = 1000
                self.sprint_reset_cooldown = False
                self.sprint_time += 200
            elif self.sprint_time > 1000: # Makes sure the sprint time does not go beyond limit
                self.sprint_time = 1000
           
        # Right character controls
        if self.controls == 'right':
            if keys[pygame.K_UP] and self.velocity_y >= 0 and self.ymovement:
                self.direction = 'up'
                if self.jump_count < 2:
                    if not self.hurt:
                        self.velocity_y = -16
                    if self.hurt:
                        self.velocity_y = -10
                    self.jump_count += 1
                    self.in_the_air = True
                    self.frame_index = 0
                    self.platform_collidable = True
                    jump_sound.play()
                    self.sound_played = False

                if keys[pygame.K_m] and self.velocity_y >= 18 and self.sprint_time > 0:
                    self.velocity_y = -20
                    self.sprint_time -= 200
                    self.run = True
                    jump_sound.play()

            if keys[pygame.K_DOWN] and self.ymovement:
                self.direction = 'down'
                if self.collide_platform:
                    self.in_the_air = True
                    self.frame_index = 5
                    self.velocity_y += 0.78
                    self.ypos += self.velocity_y
                    self.platform_collidable = False
                    self.sound_played = False

                if keys[pygame.K_m] and self.sprint_time > 0:
                    self.velocity_y = 25
                    self.sprint_time -= 200
                    self.run = True
                    jump_sound.play()

            if keys[pygame.K_LEFT] and not self.collide_bottom and self.xmovement :
                self.xpos -= 5
                self.direction = 'left'
                self.walking = True
                if keys[pygame.K_m] and self.sprint_time > 0:
                    self.xpos -= 10
                    self.sprint_time -= 20
                    self.run = True
                    jump_sound.play()

            if keys[pygame.K_RIGHT] and not self.collide_bottom and self.xmovement:
                self.xpos += 5
                self.direction = 'right'
                self.walking = True
                if keys[pygame.K_m] and self.sprint_time > 0:
                    self.xpos += 10
                    self.sprint_time -= 20
                    self.run = True
                    jump_sound.play()

            # For animation
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.walking = False
            # Sprinting logic, same as character 1
            if (not keys[pygame.K_m] or (not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT])) and not self.sprint_reset_cooldown :
                self.sprint_time += 200
                self.run = False
            if self.sprint_time <= 0:
                self.sprint_reset_cooldown = True
                self.timer -= 10
                self.run = False
            if self.timer <= 0:
                self.timer = 1000
                self.sprint_reset_cooldown = False
                self.sprint_time += 200
            elif self.sprint_time > 1000:
                self.sprint_time = 1000
        # Gravity
        if self.gravity:
            self.velocity_y += 0.78
            self.ypos += self.velocity_y
        # Checks whether the character collides with the map, either ground or platforms
        self.check_collision(ground, [platform1, platform2, platform3], [border_bottom, border_top, border_right, border_left])
    # Reset the character's position if their health is 0 or fall of the map
    def reset_position(self, target_x, target_y):
        self.gravity = False  # Stop gravity to reset the character's position
        self.velocity_y = 0  # Reset vertical velocity
        self.beam_height = HEIGHT
        self.beam_width = 120
        self.transparency = 50
            # Calculate the distance to the target
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

            # When reaching the target, restore initial character attributes
        if abs(self.xpos - target_x) < 5 and abs(self.ypos - target_y) < 5:
            self.xpos, self.ypos = target_x, target_y
            self.gravity = True  # Reactivate gravity
            self.reset_character_pos = False
            self.collide_cooldown = False
            self.health = 1000
            self.check_health()
            self.score_added = False
    # check whether the character's range rect collides with the enemy's hitbox rect
    def check_hits(self, other):
        other.inrange = False
        if self.get_rect_range().colliderect(other.get_rect_hitbox()):
            other.inrange = True
    # Checks the player direction
    def player_direction(self):
        if self.range == 'melee': # Adjusts the range rect for melee attacks according to the direction of the character
            if self.direction == 'up':
                self.range_y_adjustment = self.range_height - 30
                self.range_height_adjustment = 30
                self.range_x_adjustment, self.range_width_adjustment = 0, 0
            if self.direction == 'down':
                self.direction = self.prev_key

            if self.direction == 'left':
                self.prev_key = 'left'
                self.range_x_adjustment = 40 - self.range_width 
                self.range_width_adjustment = -10
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
            if self.direction == 'right':
                self.prev_key = 'right'
                self.range_x_adjustment = self.range_width - 50
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.range_width_adjustment = -10
        if self.range == 'range': # Adjusts the range rect for range attacks according to the direction of the character
            if self.direction == 'up':
                self.range_y_adjustment = self.range_height + 90
                self.range_height_adjustment = -90
                self.range_x_adjustment, self.range_width_adjustment = 0, 0
            if self.direction == 'down':
                self.direction = self.prev_key
            if self.direction == 'left':
                self.range_x_adjustment = -80 - self.range_width
                self.range_width_adjustment = -120
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
            if self.direction == 'right':
                self.range_x_adjustment = self.range_width - 40
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.range_width_adjustment = -120
    # Sets the knockback if the character gets hit
    def knockback(self, direction, multiplier):
        if self.knockback_direction is None: # Set the knockback direction only if it does not have a knockback direction yet
            self.knockback_direction = direction
        health_lost = 1000 - self.health # Calculate the health lost
        self.knockback_speed *= multiplier # Multipy the knockback speed by the multiplier that is passed from the attack that is used
        self.hurt = True # Sets the animation

        add_knockback = (health_lost/100) * multiplier**3 # Adds more knockback the more health is lost. 

        decelerator = 1.1
        if self.knockback_speed > 0.1:  # Checks whether there is knockback
            self.knockback_speed /= decelerator  # If there is knockback, divide it by decelerator to make the character stop eventually

        knockback_amount = self.knockback_speed + add_knockback # Calculate the knockback amount based on the multipliers and the health lost

        # Sets the logic of the knockback based on the direction
        if self.knockback_direction == 'up': 
            self.velocity_y = 0
            self.ypos -= knockback_amount * 2 
            self.ymovement = False

        elif self.knockback_direction == 'right':
            self.xpos += knockback_amount 
            self.xmovement = False

        elif self.knockback_direction == 'left':
            self.xpos -= knockback_amount 
            self.xmovement = False

    # Stop knockback when the speed is small enough and returns the normal character attributes
        if self.knockback_speed < 0.1:
            self.xmovement = True
            self.ymovement = True
            self.is_knocked_back = False  # End knockback when speed is low enough
            self.knockback_speed = 10 # Reset the knockback speed
            self.hurt = False # Update the animation
            self.knockback_direction = None # Reset the knockback direction
    # Handles the character's attack
    def attack(self, other):

        keys = pygame.key.get_pressed() # Get the user input
        multiplier = 1 # multiplier of knockback
        # Left character attack controls
        if self.controls == 'left':
            if keys[pygame.K_t] and self.attack_available and not self.attack_cooldown and not self.attack2_cooldown:  
                self.attack_cooldown = True
                if other.inrange:  # If the other character is within range
                    other.take_damage(50)
                    other.inrange = False
                    other.is_knocked_back = True
                    self.skill_counter += 1
                    self.ulti_counter += 1
                    self.skill_counter = min(3, self.skill_counter)
                    self.ulti_counter = min(8, self.ulti_counter)
                    self.attack_available = False
                    self.attack_cooldown = True
                    self.is_attacking = True
                    character1_attack1_sound.play()
            if self.attack_available:
                if self.frame_index > 2:
                    self.is_attacking = False
            if not keys[pygame.K_t]:
                self.attack_cooldown = False

            if keys[pygame.K_g] and self.attack_available and not self.attack2_cooldown:
                if self.skill_counter == 3:
                    self.attacking_range = True
                    self.skill_counter = 0
                    self.xmovement = False
                    self.ymovement = False
                    character1_attack2_sound.play()

            if self.attacking_range == True:
                self.range = 'range'
                self.is_attacking2 = True
                self.attack2_cooldown = True
                if self.frame_index > 6:
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 5
                        other.is_knocked_back = True
                        self.attack_available = False
            
            if self.current_action == 'attack2_up':
                if self.frame_index > 10:
                    multiplier = 1
                    self.range = 'melee'
                    self.attacking_range = False
                    self.attack2_cooldown = False
                    self.is_attacking2 = False
            if self.current_action == 'attack2_side':
                if self.frame_index > 12:
                    multiplier = 1
                    self.range = 'melee'
                    self.attacking_range = False
                    self.attack2_cooldown = False
                    self.is_attacking2 = False

            if keys[pygame.K_f] and self.attack_available:
                if self.ulti_counter == 8:
                    self.ulti_counter = 0
                    self.is_ult = True
                    self.xmovement = False
                    self.ymovement = False
                    character1_attack2_sound.play()
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 7
                        other.is_knocked_back = True
                        self.attack_available = False
            if self.current_action == 'ult_side' or 'ult_up':
                if self.frame_index > 8:
                    self.is_ult = False
            
            if not self.is_attacking2 and not self.is_ult:
                self.xmovement = True
                self.ymovement = True
                
        # Right character attack controls
        if self.controls == 'right':
            if keys[pygame.K_i] and self.attack_available and not self.attack_cooldown and not self.attack2_cooldown:  # Check if the attack key is pressed and cooldown is not active
                self.attack_cooldown = True
                if other.inrange:  # If the other character is within range
                    other.take_damage(50)
                    other.inrange = False
                    other.is_knocked_back = True
                    self.skill_counter += 1
                    self.ulti_counter += 1
                    self.skill_counter = min(3, self.skill_counter)
                    self.ulti_counter = min(8, self.ulti_counter)
                    self.attack_available = False
                    self.is_attacking = True
                    character2_attack1_sound.play()
            if self.attack_available:
                if self.frame_index > 5:
                    self.is_attacking = False
            if not keys[pygame.K_i]:
                self.attack_cooldown = False

            
            if keys[pygame.K_k] and self.attack_available and not self.attack2_cooldown:
                if self.skill_counter == 3:
                    self.attacking_range = True
                    self.skill_counter = 0
                    self.xmovement = False
                    self.ymovement = False
                    character2_attack2_sound.play()

            if self.attacking_range == True:
                self.range = 'range'
                self.is_attacking2 = True
                self.attack2_cooldown = True
                if self.frame_index > 6:
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 5
                        other.is_knocked_back = True
                        self.attack_available = False
            if self.current_action == 'attack2_side' or 'attack2_up':
                if self.frame_index > 12:
                    multiplier = 1
                    self.range = 'melee'
                    self.attacking_range = False
                    self.attack2_cooldown = False
                    self.is_attacking2 = False
            

            if keys[pygame.K_l] and self.attack_available:
                if self.ulti_counter == 8:
                    self.ulti_counter = 0
                    self.is_ult = True
                    self.xmovement = False
                    self.ymovement = False
                    character2_attack2_sound.play()
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 7
                        other.is_knocked_back = True
                        self.attack_available = False
            if self.current_action == 'ult_side':
                if self.frame_index > 7:
                    self.is_ult = False
            if self.current_action == 'ult_up':
                if self.frame_index > 6:
                    self.is_ult = False
            
            if not self.is_ult and not self.is_attacking2:
                self.xmovement = True
                self.ymovement = True
                
        # Sets the animation for character falling down
        if self.gravity:
            if self.velocity_y > 1:
                self.in_the_air = True
                self.frame_index = 5
                self.sound_played = False

        # Sets the direction of the knocked back animation
        if other.is_knocked_back:
            other.knockback(self.direction, multiplier)
            if self.xpos > other.xpos:
                other.direction = 'right'
            else: 
                other.direction = 'left'
        elif not other.is_knocked_back and not other.reset_character_pos: # Allow attack when the enemy is no longer knocked back
            self.attack_available = True
        
    def score(self, other): # Sets the winning condition
        if self.alive == False and not self.score_added: # Adds the score to the other character if not alive
            other.point += 1
            self.score_added = True
        if (self.point - other.point == 2 and self.point > other.point) or (self.point >= 3 and other.point != self.point): # sets who wins the game, either 2 point difference or reaches 3 points and not a tie
            self.win = True
    # Sets the action for the animation
    def set_action(self, action):
        if self.current_action != action:
            self.frame_index = 0  # Reset to the first frame of the new action
        self.current_action = action
    # Update the animation of the character 
    def update_animation(self, character):
        # Speed of the frames logic for each action
        if self.current_action == 'idle' or 'walk' or 'dead' or 'hurt': 
            self.animation_speed = 0.01
        if self.current_action == 'run':
            self.animation_speed = 0.2
        if self.current_action == 'jump':
            if self.frame_index < 4:
                self.animation_speed = 0.7
            else:
                self.animation_speed = 0.05     
        if character1.current_action == 'attack1_side' or 'attack1_up':
            self.animation_speed = 0.6         
        if character1.current_action == 'attack2_side' or 'attack2_up':
            if character1.frame_index < 7:
                self.animation_speed = 0.6
            elif character1.frame_index >= 7:
                self.animation_speed = 0.1
        
        if character1.current_action == 'ult_side':
            if self.frame_index < 6:
                self.animation_speed = 0.6
            elif self.frame_index >= 6:
                self.animation_speed = 0.02
        if character1.current_action == 'ult_up':
            if self.frame_index < 7:
                self.animation_speed = 0.6
            elif self.frame_index >= 7:
                self.animation_speed = 0.05
        if character2.current_action == 'attack1_side' or 'attack1_up':
            if character2.frame_index < 4:
                self.animation_speed = 0.6   
            elif character2.frame_index >= 4:
                self.animation_speed = 0.1        
        if character2.current_action == 'attack2_side' or 'attack2_up':
            if character2.frame_index > 11:
                character2.animation_speed = 0.6
            elif character2.frame_index >= 11:
                character2.animation_speed = 0.3
        if character2.current_action == 'ult_side':
            if character2.frame_index < 5:
                self.animation_speed = 0.6   
            elif character2.frame_index >= 5:
                self.animation_speed = 0.1  
        if character2.current_action == 'ult_up':
            if character2.frame_index < 3:
                self.animation_speed = 0.6   
            elif character2.frame_index >= 3:
                self.animation_speed = 0.1  

        # Increments the frame_index by the animation speed
        self.frame_index += self.animation_speed
            # Loop animation if it exceeds frame count for actions like walk, idle, and run
        if self.frame_index >= len(self.animations[self.current_action]):
            if self.current_action == 'walk' or self.current_action == 'idle' or self.current_action == 'run':
                self.frame_index = 0  # Loop walk/idle
            else:
                self.frame_index = len(self.animations[self.current_action]) - 1  # Hold attack animation on the last frame

        # Set the current image based on the current action and updated frame index
        self.image = self.animations[self.current_action][int(self.frame_index)]
        # Handles the flipping logic between left and right direction
        if character == 'character1':
            if self.direction == 'left' or self.prev_key == 'left':
                self.image = pygame.transform.flip(self.image, True, False)

        if character == 'character2':
            if self.is_attacking or self.is_attacking2 or self.is_ult or self.hurt or self.run:
                if self.direction == 'left' or self.prev_key == 'left':
                    self.image = pygame.transform.flip(self.image, True, False)
            else:
                if self.direction == 'right' or self.prev_key == 'right':
                    self.image = pygame.transform.flip(self.image, True, False)

    # Draws the characters with the offset of the camera        
    def draw(self, offset_x, offset_y):
        if character1: # Sets the offset so that the animation fits the range and hitbox rect of the character
            character1.x_offset = 10
            if self.direction == 'left' or self.prev_key == 'left':
                character1.x_offset += 40
                if self.walking:
                    character1.x_offset -= 20
                if self.is_attacking2: 
                    if self.current_action == 'attack2_side':
                        character1.x_offset += self.width + 100
            if self.direction == 'right':
                if self.walking:
                    character1.x_offset += 20
                if self.is_attacking2: 
                    if self.current_action == 'attack2_side':
                        character1.x_offset -= self.width - 100
        if character2:
            character2.x_offset = 35
            if self.direction == 'right':
                character2.x_offset -= 10
                if self.current_action == 'attack2_side':
                        character2.x_offset -= self.width - 100
            if self.direction == 'left' or self.prev_key == 'left':
                if self.is_attacking2: 
                    if self.current_action == 'attack2_side':
                        character2.x_offset += self.width + 100
        # Sets the position of where to draw the animation and the size of it when range attack so that it fits the range and hitbox rect of the character
        if self.is_attacking2:
            if self.current_action == 'attack2_side':
                screen.blit(pygame.transform.scale(self.image, (2*self.width + 180, self.height + 80)), (int(self.xpos - offset_x - self.x_offset), int(self.ypos - offset_y - 80)))
            elif self.current_action == 'attack2_up' :
                screen.blit(pygame.transform.scale(self.image, (self.width + 80, 2*self.height + 180)), (int(self.xpos - offset_x - self.x_offset), int(self.ypos - offset_y - 250)))
    
        else: # Draw it normally for other actions
            screen.blit(pygame.transform.scale(self.image, (self.width + 80, self.height + 80)), (int(self.xpos - offset_x - self.x_offset), int(self.ypos - offset_y - 80)))
        # Draws the respawn beam for each character
        if self.reset_character_pos:
            surface = pygame.Surface((self.beam_width, self.beam_height), pygame.SRCALPHA)
            surface.fill((255, 255, 100, self.transparency))
            screen.blit(surface, (self.xpos - offset_x, 0))
        else:
            beam_offset = 0
            beam_offset = (120 - self.beam_width)/2
            surface = pygame.Surface((self.beam_width, self.beam_height), pygame.SRCALPHA)
            surface.fill((255, 255, 100, self.transparency))
            screen.blit(surface, (self.xpos - offset_x + beam_offset, 0))
            self.transparency = max(0, self.transparency - 0.7)  # Decrease alpha gradually, with a minimum of 0
            self.beam_width = max(0, self.beam_width - 0.7)  # Decrease height
            self.beam_height = max(0, self.beam_height - 20)  # Decrease height
    def reset(self): # Reset all player attribute to initial
        self.win = False
        self.reset_character_pos = True
        character1.xpos, character1.ypos = 1.2 * WIDTH // 3, 0.96 * HEIGHT // 2
        character2.xpos, character2.ypos = 1.65 * WIDTH // 3, 0.96 * HEIGHT // 2
        self.point = 0
        self.ulti_counter = 0
        self.skill_counter = 0
        self.is_ult = False
        self.is_attacking = False
        self.is_attacking2 = False
        self.is_knocked_back = False
        self.knockback_speed = 10 # Reset the knockback speed
        self.hurt = False # Update the animation
        self.knockback_direction = None # Reset the knockback direction
    # Calls all the function that must be called from the Character class
    def update(self, other):
        self.movement()
        self.player_direction()
        self.attack(other)
        self.check_hits(other)
        if self.xpos < WIDTH//2:
            if self.reset_character_pos:
                self.reset_position(1.2 * WIDTH//3, 0.96 * HEIGHT//2)
                self.direction = 'right'
        else:
            if self.reset_character_pos:
                self.reset_position(1.65 *WIDTH//3, 0.96 * HEIGHT//2)
                self.direction = 'left'
        self.update_animation(self.name)
        self.check_movement()
        self.score(other)



# Initialize character 1
character1 = Character('character1', 1.2 * WIDTH // 3, HEIGHT // 2, 'left', animations={
        'walk': character1_walk, # List of frames for walking
        'idle': character1_idle,  # List of frames for idle
        'jump': character1_jump,  # List of frames for jumping
        'dead': character1_dead,  # List of frames for dead
        'attack1_side': character1_attack1_side,  # List of frames for attack1 
        'attack1_up': character1_attack1_up,  

        'attack2_side': character1_attack2_side,  # List of frames for attack2
        'attack2_up': character1_attack2_up, 
    
        'ult_side': character1_ult_side,  # List of frames for ult
        'ult_up': character1_ult_up, 

        'hurt': character1_hurt, # List of frames for hurt
        'run': character1_run # List of frames for run


    })
# Initialize character 2
character2 = Character('character2', 1.65 * WIDTH // 3, HEIGHT // 2, 'right', animations={
        'walk': character2_walk, # List of framse for wallking
        'idle': character2_idle,  # List of frames for idle
        'jump': character2_jump,  # List of frames for jumping
        'dead': character2_dead,  # List of frames for dead
        'attack1_side': character2_attack1_side,  # List of frames for attack1
        'attack1_up': character2_attack1_up, 

        'attack2_side': character2_attack2_side,  # List of frames for attack2
        'attack2_up': character2_attack2_up,  

        'ult_side': character2_ult_side,  # List of frames for ult
        'ult_up': character2_ult_up, 

        'hurt': character2_hurt, # List of frames for hurt
        'run': character2_run # List of frames for run

    })


