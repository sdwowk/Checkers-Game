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

    def set_path(self, position):
        """
        Tells the unit that it should be moving, where, and how.
        """
        
        def jump(new_pos, path):
            # calculate jump
            path.append(new_pos)
            neighs = self.map.neighbours(position)
            for i in neighs:
                pawn_neighs.append(self.get_unit_at_pos(i))

            open_areas = [(new_pos[0] + 2, new_pos[1] - 2),
                          (new_pos[0] + 2, new_pos[1] + 2), 
                          (new_pos[0] - 2, new_pos[1] + 2),
                          (new_pos[0] - 2, new_pos[1] - 2)]

            if unit.type == "Pawn":

                if not pawn_neighs[0] == None:
                    if not pawn_neighs[0].team == unit.team: 
                        if self.get_unit_at_pos(open_areas[1]) == None:
                            path.append(jump(open_areas[1], path))
                            
                if not pawn_neighs[1] == None:
                    if not pawn_neighs[1].team == unit.team:
                        if self.get_unit_at_pos(open_areas[2]) == None:
                            path.append(jump(open_areas[2], path))

                return path
                    
            if unit.type == "King":
                king_neighs = [self.get_unit_at_pos(neighs[0]), self.get_unit_at_pos(neighs[1]), self.get_unit_at_pos(neighs[2]), self.get_unit_at_pos(neighs[3])]
                if not king_neighs[0].team == unit.team:
                    if self.get_unit_at_pos(open_areas[0]) == None:
                        path.append(jump(open_areas[0], path))
                        
                if not king_neighs[1].team == unit.team:
                    if self.get_unit_at_pos(open_areas[1]) == None:
                        path.append(jump(open_areas[1], path))
                        
                if not king_neighs[2].team == unit.team:
                    if self.get_unit_at_pos(open_areas[2]) == None:
                        path.append(jump(open_areas[2], path))
                        
                if not king_neighs[3].team == unit.team:
                    if self.get_unit_at_pos(open_areas[3]) == None:
                        path.append(jump(open_areas[3], path))
                        
                return path



        path = []
        pawn_neighs = []
        unit = self.get_unit_at_pos(position)
        neighs = self.map.neighbours(position)
        for i in neighs:
            pawn_neighs.append(self.get_unit_at_pos(i))

        if unit.type == "Pawn":
            """
            if unit.team == 0:

            else:
                pawn_neighs = [self.get_unit_at_pos(neighs[0]),self.get_unit_at_pos(neighs[3])]
            """
            for i in pawn_neighs:   
                if not i == None:
                    if not i.team == unit.team:
                        return jump(position, path)

            if path == []:
                for i in neighs:
                    if (self.get_unit_at_pos(i) == None):
                        path.append(i)
                    
            return path

        elif unit.type == "King":
            king_neighs = [get_unit_at_pos(neighs[0]), get_unit_at_pos(neighs[1]), get_unit_at_pos(neighs[2]), get_unit_at_pos(neighs[3])]
            
            if (king_neighs[0].team == unit.team)                                           or (king_neighs[1].team == unit.team)                                           or (king_neighs[2].team == unit.team)                                           or (king_neighs[3].team == unit.team):

                return jump(postion, path)
                
            else:
                if (king_neighs[0] == None):
                    path.append(pawn_neighs[0])
                if (king_neighs[1] == None):
                    path.append(pawn_neighs[1])
                if (king_neighs[2] == None):
                    path.append(pawn_neighs[2])
                if (king_neighs[3] == None):
                    path.append(pawn_neighs[3])
                
        return path

    def move(self,position, unit, path):
        neighbourNew, neighbourOld = self.map.neighbours(position), self.map.neighbours(unit.position)
        for i in neighbourOld:
            if i in neighbourNew:
                Pieces.deactivate(i)
                self.active_units = Pieces.active_units

        if unit.position in path:
            path.remove(unit.position)
        unit.tile_x = position[0]
        unit.tile_y = position[1]
        unit.position = position
        for i in neighbourOld:
            if i in path:
                path.remove(i)
            
        return path
