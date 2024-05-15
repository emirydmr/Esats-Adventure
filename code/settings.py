import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH,WINDOW_HEIGHT = 1000, 600
WINDOW = (WINDOW_WIDTH,WINDOW_HEIGHT)
GRAVITY = 2900

DOUBLE_JUMP_HEIGHT = 100
JUMP_HEIGHT = 900
DIVE_DISTANCE = 20
SPEED = 200
TILE_SIZE = 64
ANIMATION_SPEED = 6
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