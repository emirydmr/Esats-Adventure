from settings import *
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

class AnimatedSprite(Sprite):
    def __init__(self,pos,frames,groups,z= Z_LAYERS["main"],animation_speed = ANIMATION_SPEED):
        super().__init__(pos,surf,groups,z)
        self.frames,self.frame_index = frames,0
        super().__init__(pos,self.frames[self.frame_index],groups,z)
    def update(self,dt):
        self.animate(dt)