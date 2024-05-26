import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH,WINDOW_HEIGHT = (1500, 800)
WINDOW = (WINDOW_WIDTH,WINDOW_HEIGHT)
GRAVITY = 2900

ACCELERATION = None
DOUBLE_JUMP_HEIGHT = 1000
JUMP_HEIGHT =1400
WALLJUMP_HEIGHT = 950
DIVE_DISTANCE = 20
SPEED = 200
TILE_SIZE = 64
ANIMATION_SPEED = 50
TICKSPEED = 60
Z_LAYERS = {
    'bg':0,
    'clouds':1,
    'bg tiles': 2,
    'path':3,
    'bg details':4,
    'main':5,
    'water':6,
    'fg':7
}