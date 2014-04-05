import pygame, tiles
import sys
import random

from Gui import GUI
from checkers.pieces import *
from pygame.sprite import LayeredUpdates
from collections import namedtuple

class Gameplay(Sprite):

    def __init__(self,TileMap,active_units):
        Sprite.__init__(self)
        self.map = TileMap
        self.active_units = active_units

    def get_unit_at_pos(self, pos):
        """
        Returns the active unit at the given tile position, or None if no unit
        is present.
        """
        #check to have position in tulbe or two seperate variables
        for u in self.active_units:
            if (u.tile_x, u.tile_y) == pos:
                return u
            
        return None

    def move_path(self,tile_x, tile_y):
        
        unit = self.get_unit_at_pos((tile_x,tile_y))

    
