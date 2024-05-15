import pygame

from settings import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill((255,0,0))

        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        #Kontaktindikatoren
        self.floor = False
        self.wall = False

        #Movement
        self.gravity = GRAVITY
        self.direction = vector(0,0)
        self.speed = SPEED
        self.jump = False
        self.jump_height = JUMP_HEIGHT
        self.walljump_height = WALLJUMP_HEIGHT


        # Kollision
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor":False,"left":False,"right":False}

        #Timer
        self.timers = {"wall jump":Timer(200)}
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_LEFT]:
            input_vector.x-=1
        if keys[pygame.K_RIGHT]:
            input_vector.x+=1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump = True
            self.timers["wall jump"].activate()

    def move(self,dt):
        #Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        #Wallslide
        if self.floor == False and self.wall == True:
            self.direction.y = 0
            self.rect.y += self.gravity/10 * dt
        else:
        #Normale Gravitation
            self.direction.y += self.gravity /2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity /2 * dt
            self.collision("vertical")


        if self.jump:
            #EinfacherSprung
            if self.floor:
                self.direction.y = -self.jump_height
            self.jump = False
            if self.wall:
                self.direction.y = -self.walljump_height
            self.jump = False



    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        right_rect = pygame.Rect(self.rect.topright+ vector(0,self.rect.height/4),(2,self.rect.height/2))
        left_rect = pygame.Rect(self.rect.topleft+ vector(-2,self.rect.height/4),(2,self.rect.height/2))
        # surfaces = [floor_rect,right_rect,left_rect]
        # for surface in surfaces:
        #     pygame.draw.rect(self.display_surface,"yellow",surface)
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        #Kollisionen

        self.on_surface["floor"]= True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface["left"] = True if left_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface["right"] = True if right_rect.collidelist(collide_rects) >= 0 else False
        if self.on_surface["left"] or self.on_surface["right"]:
            self.wall =True
        else:
            self.wall = False
        if self.on_surface["floor"]:
            self.floor = True
        else:
            self.floor = False
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
                        #"Abnullen" der Gravitation nach Kollision
                        self.direction.y = 0
                    # Bottom Kollision
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        #"Abnullen" der Gravitation nach Kollision
                        self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()
        print(self.on_surface)
        print(f"floor {self.floor}")
        print(f"wall {self.wall}")
        print(self.timers["wall jump"].active)