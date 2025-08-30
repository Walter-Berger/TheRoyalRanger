import pygame
from settings import *
from support import *
from debug import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # setup
        self.image = pygame.image.load("graphics/player/down_idle/0.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
        self.collision_sprites = collision_sprites

        # graphics setup
        self.import_player_assets()
        self.state = 'down'
        self.frame_index = 0
        self.animation_speed = 6

        # movement
        self.direction = pygame.Vector2()
        self.walking_speed = 300
        self.running_speed = 500
        self.speed = self.walking_speed
        self.running = False

        # dash 
        self.dash_cooldown = 4000
        self.dash_time = 0
        self.dashing = False

    def import_player_assets(self):
        player_path = "graphics/player/"

        variants = ["", "_idle", "_sprint"]
        base_directions = [
            "up", "down", "left", "right",
            "up_left", "up_right", "down_left", "down_right"
        ]     

        # build full animation dictionary dynamically
        self.animations = {
            f"{direction}{variant}": []
            for direction in base_directions
            for variant in variants
        }

        # import animations from folders
        for animation in self.animations.keys():
            full_path = f"{player_path}{animation}"
            self.animations[animation] = import_folder(full_path) 

    def get_state(self):
        # idle case
        if self.direction.length_squared() == 0:
            base = self.state.split('_')[0]
            parts = self.state.split('_')
            if len(parts) >= 2 and parts[1] in ("left", "right"):  
                base = "_".join(parts[:2]) 
            
            self.state = f"{base}_idle"
            return

        vertical = ""
        horizontal = ""
        if self.direction.y < 0:    vertical = "up"
        elif self.direction.y > 0:  vertical = "down"
        if self.direction.x < 0:    horizontal = "left"
        elif self.direction.x > 0:  horizontal = "right"

        # combine into base direction (e.g. "up_left", "down", "right")
        base = "_".join([dir for dir in (vertical, horizontal) if dir]) or "down"

        # apply sprint if running
        self.state = f"{base}_sprint" if self.running else base

    def animate(self, dt):
        animation_speed = self.animation_speed * 1.5 if self.running else self.animation_speed
        self.frame_index = self.frame_index + animation_speed * dt if self.direction else 0
        self.image = self.animations[self.state][int(self.frame_index) % len(self.animations[self.state])]

    def input(self):
        keys = pygame.key.get_pressed()      
        # movement input
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.direction = self.direction.normalize() if self.direction else self.direction

        # running check
        self.running = keys[pygame.K_LSHIFT] and self.direction
        self.speed = self.running_speed if self.running else self.walking_speed

        # blink input, only if player is moving
        if self.direction:
            if keys[pygame.K_SPACE] and not self.dashing:
                self.dash_time = pygame.time.get_ticks()
                self.dashing = True
                blink_vector = self.direction * 150
                self.rect.topleft += blink_vector

    def collisions(self, axis):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collisions('horizontal')

        self.rect.y += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collisions('vertical')

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.dash_time >= self.dash_cooldown:
            self.dashing = False

    def update(self, dt):
        self.input()
        self.cooldown()
        self.get_state()
        self.move(dt)
        self.animate(dt)


        

