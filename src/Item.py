from sys import implementation

import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
