import os

import pygame
from os.path import join
from settings import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites,frames):
        super().__init__(groups)
        self.frames, self.frame_number= frames,0
        self.state,self.right_faced = "idle",True
        self.image = self.frames["player"][self.state][self.frame_number]

        #animation
        self.possible_states = os.listdir(join("..","assets","Esat","sprites"))

        print(self.possible_states)
        #rects
        self.rect = self.image.get_frect(topleft = pos)
        self.hitbox_rect = self.rect.inflate(-78,-26)
        self.old_rect = self.rect.copy()

        #Kontaktindikatoren
        self.floor = False
        self.wall = False

        #Movement
        self.state = "idle"
        self.acceleration = ACCELERATION
        self.gravity = GRAVITY
        self.direction = vector(0,0)
        self.speed = SPEED
        self.jump = False
        self.jump_height = JUMP_HEIGHT
        self.walljump_height = WALLJUMP_HEIGHT
        #self.idle = True if


        # Kollision
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor":False,"left":False,"right":False}

        #Timers
        self.timers = {
            "wall slide block": Timer(200), #Wallslides sollen erst nach einer gewissen Zeit möglich sein
            "pre wall jump block": Timer(300),  # Bewirkt, dass Walljumps erst gemacht werden dürfen, wenn der Spieler eine gewisse Dauer bereits geslidet ist
            "post wall jump input block":Timer(300),#Blockiert L/R Input wenn Player einen Walljump gemacht hat

        }
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)

        if self.timers["post wall jump input block"].active == False:
            #Blockiert linksseitigen Input wenn der Walljump-Timer aktiv ist, und der Player linksseitigen Kontakt hat
            if keys[pygame.K_LEFT] and not self.on_surface["left"]:
                input_vector.x-=1
                self.right_faced = False
            #Blockiert linksseitigen Input wenn der Walljump-Timer aktiv ist, und der Player rechtssseitigen Kontakt hat
            if keys[pygame.K_RIGHT] and not self.on_surface["right"]:
                input_vector.x+=1
                self.right_faced = True
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump = True
    def update_state(self):
        if self.on_surface["floor"]:
            self.state = "idle" if self.direction.x == 0 else "walk"
    def move(self,dt):
        #Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        #self.direction.x += self.acceleration * dt
        #self.rect.x = self.direction.x * self.speed * dt * self.acceleration
        self.collision("horizontal")

        #Wallslide
        if ((self.floor == False) and (self.wall == True)) and self.timers["wall slide block"].active == False:
            self.direction.y = 0
            self.rect.y += self.gravity/10 * dt
        else:
        #Normale Gravitation
            self.direction.y += self.gravity /2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity /2 * dt
            self.collision("vertical")

        if self.floor:
            self.timers["pre wall jump block"].activate()


        if self.jump:
            #EinfacherSprung
            if self.floor:
                self.direction.y = -self.jump_height
                self.timers["wall slide block"].activate()
            elif self.wall and self.timers["pre wall jump block"].active == False:
                #Blockiert Input wenn Walljump aktiv, siehe input()
                self.timers["post wall jump input block"].activate()
                self.direction.x = 1 if self.on_surface["left"] else -1
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

    def animate(self,dt):
        self.frame_number += ANIMATION_SPEED *dt
        self.image = self.frames["player"][self.state][int(self.frame_number % len(self.frames["player"][self.state]))]
        self.image = self.image if self.right_faced else pygame.transform.flip(self.image,True,False)
    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.update_state()
        self.animate(dt)
        self.update_timers()
        self.check_contact()

