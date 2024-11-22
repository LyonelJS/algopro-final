import pygame
from collision import ground, bottom, platform1, platform2, platform3, border_bottom, border_left, border_right, border_top

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

character1_walk = [pygame.image.load(f"character1/walk/walk_{i}.png").convert_alpha() for i in range(1, 6)]
character1_idle = [pygame.image.load(f"character1/idle/idle_{i}.png").convert_alpha() for i in range(1, 7)]
character1_jump = [pygame.image.load(f"character1/jump/jump_{i}.png").convert_alpha() for i in range(1, 9)]
character1_dead = [pygame.image.load(f"character1/dead/dead_{i}.png").convert_alpha() for i in range(1, 6)]
character1_attack1 = [pygame.image.load(f"character1/attack_1/attack_{i}.png").convert_alpha() for i in range(1, 4)]
character1_hurt = [pygame.image.load(f"character1/hurt/hurt_{i}.png").convert_alpha() for i in range(1, 3)]


character2_walk = [pygame.transform.flip(pygame.image.load(f"character2/walk/walk_{i}.png").convert_alpha(), True, False) for i in range(1, 7)]
character2_idle = [pygame.transform.flip(pygame.image.load(f"character2/idle/idle_{i}.png").convert_alpha(), True, False) for i in range(1, 8)]
character2_jump = [pygame.transform.flip(pygame.image.load(f"character2/jump/jump_{i}.png").convert_alpha(), True, False) for i in range(1, 9)]
character2_dead = [pygame.transform.flip(pygame.image.load(f"character2/dead/dead_{i}.png").convert_alpha(), True, False) for i in range(1, 4)]
character2_attack1 = [pygame.image.load(f"character2/attack_1/attack_{i}.png").convert_alpha() for i in range(1, 7)]
character2_hurt = [pygame.image.load(f"character2/hurt/hurt_{i}.png").convert_alpha() for i in range(1, 4)]



class Character:
    def __init__(self, name, xpos, ypos, controls, animations):
        self.name = name
        self.xpos = xpos 
        self.ypos = ypos 
        self.controls = controls
        self.xmovement = True
        self.ymovement = True
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
        self.knockback_direction = None
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
        self.offset_x = 0
        self.offset_y = 0
        self.prev_key = None
        self.in_the_air = False
        self.alive = True
        self.is_attacking = False
        self.walking = False
        self.x_offset = 0
        self.hurt = False

        self.animations = animations
        self.current_action = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.current_action]
        



    def get_rect_hitbox(self, offset_x, offset_y):
        return pygame.Rect(self.xpos + offset_x + 30, self.ypos + offset_y, self.width - 40, self.height)
    
    def get_rect_range(self, offset_x, offset_y):
        return pygame.Rect(self.xpos + self.range_x_adjustment + offset_x + 30, self.ypos - self.range_y_adjustment + offset_y, self.range_width - self.range_width_adjustment - 40, self.range_height - self.range_height_adjustment)
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)  # Health can't go below 0
        self.check_health()

    def check_health(self):
        if self.health == 0:
            self.alive = False
            self.set_action('dead')   
            self.reset_character_pos = True
            self.ulti_counter = 0
            self.xmovement = False
            self.ymovement = False
            character1.attack_available, character2.attack_available = False, False
            self.in_the_air = False
        
        elif self.health > 0:
            self.alive = True
            self.set_action('idle')   
            self.reset_character_pos = False
            self.xmovement = True
            self.ymovement = True
            character1.attack_available, character2.attack_available = True, True

    def check_collision(self, ground, platforms, borders):
        for border in borders:
            if self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(border) and self.collide_cooldown == False:
                self.reset_character_pos = True
                self.collide_cooldown = True
                self.health = 0                
                self.check_health()
                

            if self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(border_top):
                print('top')
            elif self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(border_bottom):
                print('bottom')
            elif self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(border_left):
                print('left')
            elif self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(border_right):
                print('right')



        if self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(ground):
            self.ypos = ground.top - self.height
            self.velocity_y = 0
            self.jump_count = 0
            self.collide_ground = True
            self.collide_platform = False
            self.collide_bottom = False
            self.platform_collidable = True
            self.in_the_air = False

        elif self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(bottom):
            self.collide_bottom = True
            self.collide_ground = False
            self.collide_platform = False
            self.in_the_air = False

        else:
            for platform in platforms:
                if self.get_rect_hitbox(self.offset_x, self.offset_y).colliderect(platform) and self.velocity_y > 0 and self.platform_collidable:
                    self.ypos = platform.top - self.height
                    self.velocity_y = 0
                    self.jump_count = 0
                    self.collide_ground = False
                    self.collide_platform = True
                    self.collide_bottom = False
                    self.platform_collidable = True
                    self.in_the_air = False
    
                    break
    def check_movement(self):
        if self.alive:
            if self.is_attacking:
                self.set_action('attack1')
            if self.hurt:
                self.set_action('hurt')
            if self.in_the_air and not self.is_attacking:
                self.set_action('jump')
            if self.walking and not self.in_the_air and not self.is_attacking:
                self.set_action('walk')

            if not self.walking and not self.in_the_air and not self.is_attacking and not self.hurt:
                self.set_action('idle')

    def movement(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        keys = pygame.key.get_pressed()

        # Left character controls
        if self.controls == 'left':
            if keys[pygame.K_w] and self.velocity_y >= 0 and self.ymovement:
                character1.direction = 'up'
                if self.jump_count < 2:
                    self.velocity_y = -20
                    self.jump_count += 1
                    self.in_the_air = True
                    self.frame_index = 0
                    self.platform_collidable = True
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
                self.walking = True
                if keys[pygame.K_v]:
                    self.xpos -= 10

            if keys[pygame.K_d] and not self.collide_bottom and self.xmovement:
                self.xpos += 5
                self.direction = 'right'
                self.walking = True
                if keys[pygame.K_v]:
                    self.xpos += 10
            
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.walking = False
            # Idle action when no movement keys are pressed
           
        # Right character controls
        if self.controls == 'right':
            if keys[pygame.K_UP] and self.velocity_y >= 0 and self.ymovement:
                self.direction = 'up'
                if self.jump_count < 2:
                    self.velocity_y = -20
                    self.jump_count += 1
                    self.in_the_air = True
                    self.frame_index = 0
                    self.platform_collidable = True

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
                self.walking = True
                if keys[pygame.K_m]:
                    self.xpos -= 10

            if keys[pygame.K_RIGHT] and not self.collide_bottom and self.xmovement:
                self.xpos += 5
                self.direction = 'right'
                self.walking = True
                if keys[pygame.K_m]:
                    self.xpos += 10

            # Idle action when no movement keys are pressed
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.walking = False

        self.player_direction()
        self.check_movement()
        self.update_animation(self.name)

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
            self.health = 1000
            self.check_health()

            

    # Stop moving once the character is close enough to the target

    
    def check_hits(self, other):
        other.inrange = False
        if self.get_rect_range(self.offset_x, self.offset_y).colliderect(other.get_rect_hitbox(self.offset_x, self.offset_y)):
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
                self.prev_key = 'left'
                self.range_x_adjustment = 40 - self.range_width 
                self.range_width_adjustment = -10
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
            if self.direction == 'right':
                self.prev_key = 'right'
                self.range_x_adjustment = self.range_width - 50
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.range_width_adjustment = -10
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
                self.range_x_adjustment = -80 - self.range_width
                self.range_width_adjustment = -120
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
            if self.direction == 'right':
                self.range_x_adjustment = self.range_width - 40
                self.range_y_adjustment, self.range_height_adjustment = 0, 0
                self.range_width_adjustment = -120

    def knockback(self, direction, multiplier):
    # Deceleration via division: gradually reduce knockback speed until it becomes very small
        if self.knockback_direction is None:
            self.knockback_direction = direction
        health_lost = 1000 - self.health
        self.knockback_speed *= multiplier
        self.walking = False
        self.hurt = True

        add_knockback = (health_lost/100) * multiplier**3

        decelerator = 1.1
        if self.knockback_speed > 0.1:  # Set a small threshold to stop knockback once it's nearly zero
            self.knockback_speed /= decelerator  # Divide the speed by 1.1 each time (you can adjust this divisor)

        knockback_amount = self.knockback_speed + add_knockback
    
        if self.knockback_direction == 'up':
            self.velocity_y = 0
            self.ypos -= knockback_amount * 2 
            self.ymovement = False

        elif self.knockback_direction == 'down':
            self.velocity_y = 0
            self.ypos += knockback_amount * 2 
            self.ymovement = False

        elif self.knockback_direction == 'right':
            self.xpos += knockback_amount 
            self.xmovement = False

        elif self.knockback_direction == 'left':
            self.xpos -= knockback_amount 
            self.xmovement = False

    # Stop knockback when the speed is small enough
        if self.knockback_speed < 0.1:
            self.xmovement = True
            self.ymovement = True
            self.is_knocked_back = False  # End knockback when speed is low enough
            self.knockback_speed = 10
            self.hurt = False
            self.knockback_direction = None

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
                    self.is_attacking = True
            if self.attack_available:
                if self.frame_index >= 2:
                    self.is_attacking = False

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
                    self.is_attacking = True

            if self.attack_available:
                if self.frame_index >=2:
                    self.is_attacking = False
            
            if keys[pygame.K_k] and self.attack_available:
                self.range = 'range'
                if self.skill_counter == 3:
                    if other.inrange:
                        other.take_damage(70)
                        other.inrange = False
                        multiplier = 5
                        other.is_knocked_back = True
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
        self.check_movement()

        if other.is_knocked_back:
            other.knockback(self.direction, multiplier)
            if self.xpos > other.xpos:
                other.direction = 'right'
            else: 
                other.direction = 'left'
        elif not other.is_knocked_back and not other.reset_character_pos:
            self.attack_available = True
        
    def score(self, other):
        if self.health == 0:
            other.point += 1
        if (self.point - other.point == 2 and self.point > other.point) or self.point == 3:
            self.win = True

    def set_action(self, action):
        if self.current_action != action:
            self.frame_index = 0  # Reset to the first frame of the new action
        self.current_action = action

        self.update_time = pygame.time.get_ticks()  # Track when the action started

    def update_animation(self, character):
        if self.current_action == 'idle' or 'walk' or 'dead' or 'hurt':
            speed = 0.1
        if self.current_action == 'jump':
            if self.frame_index < 4:
                speed = 0.7
            else:
                speed = 0.05     
        if self.current_action == 'attack1':
            if self.frame_index < 2:
                speed = 0.8   
            elif self.frame_index >= 2:
                speed = 0.01        

        self.frame_index += speed
            # Loop animation if it exceeds frame count
        if self.frame_index >= len(self.animations[self.current_action]):
            if self.current_action == 'walk' or self.current_action == 'idle':
                self.frame_index = 0  # Loop walk/idle
            else:
                self.frame_index = len(self.animations[self.current_action]) - 1  # Hold attack animation on the last frame

        # Set the current image based on the updated frame
        self.image = self.animations[self.current_action][int(self.frame_index)]

        if character == 'character1':
            if self.direction == 'left' or self.prev_key == 'left':
                self.image = pygame.transform.flip(self.image, True, False)

        if character == 'character2':
            if self.is_attacking or self.hurt:
                if self.direction == 'left' or self.prev_key == 'left':
                    self.image = pygame.transform.flip(self.image, True, False)
            else:
                if self.direction == 'right' or self.prev_key == 'right':
                    self.image = pygame.transform.flip(self.image, True, False)


        # Update the current image

        
    def draw(self, offset_x, offset_y):
        if character1:
            character1.x_offset = 10
            if self.direction == 'left' or self.prev_key == 'left':
                character1.x_offset += 40
                if self.walking:
                    character1.x_offset -= 20
            if self.direction == 'right':
                if self.walking:
                    character1.x_offset += 20
        if character2:
            character2.x_offset = 35
            if self.direction == 'right':
                character2.x_offset -= 10
        screen.blit(pygame.transform.scale(self.image, (self.width + 80, self.height + 80)), (int(self.xpos - offset_x - self.x_offset), int(self.ypos - offset_y - 80)))

# Initialize character objects
character1 = Character('character1', 1.2 * WIDTH // 3, HEIGHT // 2, 'left', animations={
        'walk': character1_walk, # List of frames for walking
        'idle': character1_idle,  # List of frames for idle
        'jump': character1_jump,  # List of frames for jumping
        'dead': character1_dead,  # List of frames for dead
        'attack1': character1_attack1,  # List of frames for dead
        'hurt': character1_hurt


    })
character2 = Character('character2', 1.65 * WIDTH // 3, HEIGHT // 2, 'right', animations={
        'walk': character2_walk, # List of framse for wallking
        'idle': character2_idle,  # List of frames for idle
        'jump': character2_jump,  # List of frames for jumping
        'dead': character2_dead,  # List of frames for dead
        'attack1': character2_attack1,  # List of frames for dead
        'hurt': character2_hurt

    })


