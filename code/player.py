import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        # setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player/down/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.dash_speed = self.speed * 3
        self.dash_cooldown = -1.0
        self.dash_duration = 0.2
        self.dash_timer = 0

    def input(self):
        keys = pygame.key.get_pressed()      
        # movement input
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        # dash input
        if keys[pygame.K_SPACE] and self.dash_timer <= self.dash_cooldown:
            self.dash_timer = self.dash_duration
            
    def move(self, dt):
        # diagonal vector need to be normalized, otherwise player would move faster
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # determine current speed
        current_speed = self.dash_speed if self.dash_timer > 0 else self.speed
        self.rect.topleft += self.direction * current_speed * dt
        self.dash_timer -= dt

    def update(self, dt):
        self.input()
        self.move(dt)

