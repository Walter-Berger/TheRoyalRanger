import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # setup
        self.image = pygame.image.load('graphics/player/down/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        # movement settings
        self.direction = pygame.Vector2()
        self.speed = 500

        # blink settings
        self.blink_distance = 150
        self.blink_cooldown = 1000
        self.blink_cooldown_end = 0

    def input(self):
        keys = pygame.key.get_pressed()      
        # movement input
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
     
        # blink input, only if player is moving
        if self.direction:
            now = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and now >= self.blink_cooldown_end:
                blink_vector = self.direction * self.blink_distance
                self.rect.topleft += blink_vector
                self.blink_cooldown_end = (now + self.blink_cooldown)
            
    def move(self, dt):
        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()
        self.rect.topleft += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)

