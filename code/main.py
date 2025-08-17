import pygame, sys
from settings import *
from player import *
from debug import *

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The Royal Ranger')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player((100,100), self.all_sprites)
    
    def run(self):
        while True:  
            # get delta time in ms
            dt = self.clock.tick(FPS) / 1000 

            # event loop
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    pygame.quit()
                    sys.exit()

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            self.player.draw_blink_cooldown()
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
