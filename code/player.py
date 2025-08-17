import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(PLAYER_IMAGE_IDLE_DOWN).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.Vector2()
        self.speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        # walking up and down
        if keys[pygame.K_w]:    self.direction.y = -1
        elif keys[pygame.K_s]:  self.direction.y = 1
        else:                   self.direction.y = 0
        # walking left and right
        if keys[pygame.K_a]:    self.direction.x = -1
        elif keys[pygame.K_d]:  self.direction.x = 1
        else:                   self.direction.x = 0
            
    def move(self, dt):
        # if walking diagonal vector need to be normalized, otherwise player would move faster
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.topleft += self.direction * self.speed * dt 

    def update(self, dt):
        self.input()
        self.move(dt)

