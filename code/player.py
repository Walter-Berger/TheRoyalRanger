import pygame
from settings import *
from debug import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # setup
        self.sprite_sheet = pygame.image.load("graphics/player/green.png").convert_alpha()
        self.animations = self.load_animations()  
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 10
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.direction = pygame.Vector2()
        self.speed_walking = 300
        self.speed_running = 500
        self.speed = self.speed_walking
        self.running = False

        # dash 
        self.dash_cooldown = 4000
        self.dash_time = 0
        self.dashing = False

    def load_animations(self):
        COLS, ROWS = 12, 8
        DOWN_ROW, LEFT_ROW, RIGHT_ROW, UP_ROW = 0, 1, 2, 3
        DOWN_LEFT_ROW, DOWN_RIGHT_ROW, UP_LEFT_ROW, UP_RIGHT_ROW = 0, 1, 2, 3
        

        sw, sh = self.sprite_sheet.get_size()
        fw, fh = sw // COLS, sh // ROWS

        def frames_from_row(row, start, end):
            return [
                self.sprite_sheet.subsurface(pygame.Rect(c * fw, row * fh, fw, fh))
                for c in range(start, end)
            ]

        return {
            'up': frames_from_row(UP_ROW, 0, 3),
            'up-run': frames_from_row(UP_ROW, 6, 9),
            'down': frames_from_row(DOWN_ROW, 0, 3),
            'down-run': frames_from_row(DOWN_ROW, 6, 9),
            'left': frames_from_row(LEFT_ROW, 0, 3),
            'left-run': frames_from_row(LEFT_ROW, 6, 9),
            'right': frames_from_row(RIGHT_ROW, 0, 3),
            'right-run': frames_from_row(RIGHT_ROW, 6, 9),

            'up-right': frames_from_row(UP_RIGHT_ROW, 3, 6),
            'up-left': frames_from_row(UP_LEFT_ROW, 3, 6),
            'down-right': frames_from_row(DOWN_RIGHT_ROW, 3, 6),
            'down-left': frames_from_row(DOWN_LEFT_ROW, 3, 6),
            'up-right-run': frames_from_row(UP_RIGHT_ROW, 9, 12),
            'up-left-run': frames_from_row(UP_LEFT_ROW, 9, 12),
            'down-right-run': frames_from_row(DOWN_RIGHT_ROW, 9, 12),
            'down-left-run': frames_from_row(DOWN_LEFT_ROW, 9, 12),
        }

    def get_status(self):
        # determine facing direction based on movement
        if self.direction.y < 0 and self.direction.x == 0:    
            self.status = 'up-run' if self.running else 'up'
        elif self.direction.y > 0 and self.direction.x == 0:  
            self.status = 'down-run' if self.running else 'down'
        elif self.direction.x < 0 and self.direction.y == 0:  
            self.status = 'left-run' if self.running else 'left'
        elif self.direction.x > 0 and self.direction.y == 0:  
            self.status = 'right-run' if self.running else 'right'

        # diagonal
        elif self.direction.y < 0 and self.direction.x < 0:  
            self.status = 'up-left-run' if self.running else 'up-left'
        elif self.direction.y < 0 and self.direction.x > 0:  
            self.status = 'up-right-run' if self.running else 'up-right'
        elif self.direction.y > 0 and self.direction.x < 0:  
            self.status = 'down-left-run' if self.running else 'down-left'
        elif self.direction.y > 0 and self.direction.x > 0:  
            self.status = 'down-right-run' if self.running else 'down-right'

    def animate(self, dt):
        if self.direction:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()      
        # movement input
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        self.direction = self.direction.normalize() if self.direction else self.direction

        # running check
        self.running = keys[pygame.K_LSHIFT]
        self.speed = self.speed_running if self.running else self.speed_walking

        # blink input, only if player is moving
        if self.direction:
            if keys[pygame.K_SPACE] and not self.dashing:
                self.dash_time = pygame.time.get_ticks()
                self.dashing = True
                blink_vector = self.direction * 150
                self.rect.topleft += blink_vector
       
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.dash_time >= self.dash_cooldown:
            self.dashing = False

    def update(self, dt):
        self.input()
        self.cooldown()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        

