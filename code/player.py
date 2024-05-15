import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill((255,0,0))

        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        #Movement
        self.gravity = GRAVITY
        self.direction = vector(0,0)
        self.speed = SPEED
        self.jump = False
        self.double_jump = False
        self.dive = False

        self.dive_distance = DIVE_DISTANCE
        self.jump_height = JUMP_HEIGHT
        self.double_jump_height = DOUBLE_JUMP_HEIGHT

        # Kollision
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor":False,"left":False,"right":False}

        self.display_surface = pygame.display.get_surface()
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_LEFT]:
            input_vector.x-=1
        if keys[pygame.K_RIGHT]:
            input_vector.x+=1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE]:
            self.jump = True
        if keys[pygame.K_SPACE] and self.jump:
            self.double_jump = True
        if keys[pygame.K_SPACE] and self.double_jump:
            self.dive = True

    def move(self,dt):
        #Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        #Vertikal
        self.direction.y += self.gravity /2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity /2 * dt
        self.collision("vertical")

        #EinfacherSprung
        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height
            self.jump = False
        if self.double_jump == True:
            self.direction.y = -self.jump_height
            self.double_jump = False
        if self.dive:
            self.direction.x = +self.dive_distance
            self.dive = False


    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        right_rect = pygame.Rect(self.rect.topright+ vector(0,self.rect.height/4),(2,self.rect.height/2))
        left_rect = pygame.Rect(self.rect.topright+ vector(0,self.rect.height/4),(-2,self.rect.height/2))

        pygame.draw.rect(self.display_surface,"yellow",floor_rect)

        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        #Kollisionen
        self.on_surface["floor"] = True if floor_rect.collidelist(collide_rects) >= 0 else False
    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "horizontal":
                    # Linksseitige Kollision
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # Rechtsseitige Kollision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left


                else:
                    # Top Kollision
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # Bottom Kollision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        #"Abnullen" der Gravitation nach Kollision
                        self.direction.y = 0
    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_contact()
