from settings import *
from sprites import Sprite,AnimatedSprite
from player import Player

class Level:
    def __init__(self,tmx_map,esat_frames):
        self.display_surface = pygame.display.get_surface()

        #Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map,esat_frames)

    def setup(self,tmx_map, esat_frames):
        #fügt Tiles hinzu
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE),surf,(self.all_sprites,self.collision_sprites))
        #fügt objects hinzu
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == "player":
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites,esat_frames)
                frames = esat_frames["player"]

    def run(self,dt):
        self.display_surface.fill('gray')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)