import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # setup
        self.animations = self.load_animations()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 10
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movement settings
        self.direction = pygame.Vector2()
        self.speed = 500

        # blink settings
        self.blink_distance = 150
        self.blink_cooldown = 1000
        self.blink_cooldown_end = 0

    def load_animations(self):
        directions = ['up', 'down', 'left', 'right']
        animations = {}

        for direction in directions:
            animations[direction] = []
            # we need to make sure that images are in the right order
            # this is achieved by naming them 0.png, 1.png, ...
            for i in range(4):
                path = f'graphics/player/{direction}/{i}.png'
                image = pygame.image.load(path).convert_alpha()
                animations[direction].append(image)

        return animations

    def get_status(self):
        # determine facing direction based on movement
        if self.direction.y < 0 and self.direction.x == 0:    self.status = 'up'
        elif self.direction.y > 0 and self.direction.x == 0:  self.status = 'down'
        elif self.direction.x < 0 and self.direction.y == 0:  self.status = 'left'
        elif self.direction.x > 0 and self.direction.y == 0:  self.status = 'right'
        # diagonal status
        #elif self.direction.y < 0 and self.direction.x < 0:    self.status = 'up-left'
        #elif self.direction.y < 0 and self.direction.x > 0:  self.status = 'up-right'
        #elif self.direction.y > 0 and self.direction.x < 0:  self.status = 'down-left'
        #elif self.direction.y > 0 and self.direction.x > 0:  self.status = 'down-right'

    def animate(self, dt):
        if self.direction:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

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
        self.get_status()
        self.move(dt)
        self.animate(dt)

