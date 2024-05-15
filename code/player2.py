import pygame
from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill((255, 0, 0))

        # rects
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        # Bewegung
        self.gravity = 2900
        self.direction = vector(0, 0)
        self.speed = 200
        self.jump = False
        self.jump_height = -900

        # Kollision
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}

        # Input tracking
        self.space_pressed_last_frame = False

    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector(0, 0)

        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1

        self.direction.x = input_vector.normalize().x if input_vector else 0
        space_pressed = keys[pygame.K_SPACE]

        if space_pressed and not self.space_pressed_last_frame:
            self.jump = True

        self.space_pressed_last_frame = space_pressed

    def move(self, dt):
        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")

        # Vertikal
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collision("vertical")

        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = self.jump_height
                self.jump = False

    def contact_update(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # Kollisionen
        self.on_surface["floor"] = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
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
                        # "Abnullen" der Gravitation nach Kollision
                        self.direction.y = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.contact_update()
