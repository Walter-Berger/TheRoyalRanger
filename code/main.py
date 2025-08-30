import pygame, sys
from settings import *
from player import *
from debug import *
from pytmx.util_pygame import load_pygame
from sprites import *

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The Royal Ranger')
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
                
        # map setup
        self.setup_map()     
    
    def setup_map(self):
        map_data = load_pygame('data/maps/world_map.tmx')
        for x,y, image in map_data.get_layer_by_name('Ground').tiles():
            Sprites((x*TILESIZE, y*TILESIZE), image, self.all_sprites)

        for obj in map_data.get_layer_by_name('Objects'):
            if obj.name == 'Grass':
                Sprites((obj.x,obj.y), obj.image, self.all_sprites)
            else:
                self.objects = CollidableSprites((obj.x,obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map_data.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)

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
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
