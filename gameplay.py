import pygame, tiles, time
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
        
        def jump(new_pos):
            # calculate jump

            jump_path.append(new_pos)
            neighs = self.map.neighbours(new_pos)
            pawn_neighs = []
            open_areas = []
            for i in neighs:
                pawn_neighs.append(self.get_unit_at_pos(i))
                offset_x = (i[0] - new_pos[0]) * 2
                offset_y = (i[1] - new_pos[1]) * 2
                open_areas.append((new_pos[0] + offset_x, new_pos[1] + offset_y))               
            if unit.team == 1:
                open_areas.reverse()
                pawn_neighs.reverse()
                               
            if unit.type == "Pawn":
                
                for i in range(len(pawn_neighs)):
                    if not pawn_neighs[i] == None:
                        if not pawn_neighs[i].team == unit.team: 
                            if self.get_unit_at_pos(open_areas[i]) == None:
                                if unit.team == 1:
                                    if open_areas[i][1] < new_pos[1]:
                                        if self.map._tile_exists(open_areas[i]):
                                            jump(open_areas[i])
                                else:
                                    if open_areas[i][1] > new_pos[1]:
                                        if self.map._tile_exists(open_areas[i]):
                                            jump(open_areas[i])
                return jump_path    

            elif unit.type == "King":
                #Same as pawns without the team check since kings can
                #jump both forwards and backwards
                

                for i in range(len(pawn_neighs)):
                    if not pawn_neighs[i] == None:
                        if not pawn_neighs[i].team == unit.team: 
                            if self.get_unit_at_pos(open_areas[i]) == None:
                                # can't travel back to spot already travelled
                                if open_areas[i] not in jump_path:
                                    jump(open_areas[i])
                return jump_path    


        jump_path = []
        path = []
        pawn_neighs = []
        unit = self.get_unit_at_pos(position)
        if not self.can_move(unit):
            return []
        else:

            neighs = self.map.neighbours(position)

            #check to see if there is a jump
            for i in neighs:
                pawn_neighs.append(self.get_unit_at_pos(i))

            if unit.type == "Pawn":

                #Check neighbours to see if there is a possible jump
                for i in pawn_neighs:   
                    if not i == None:
                        if not i.team == unit.team:
                            path = jump(position)
                        
            
                if len(path) >= 1:
                    while not path == [] and path[0] == position:
                        
                            #Dont want starting postion in the path
                        path.remove(path[0])
                        
                if path == []:
                    #No neighbouring enemy pieces check neighbours for 
                    # an empty space
                    for i in neighs:
                        if (self.get_unit_at_pos(i) == None):
                            
                            #Can't go backwards. If moving upwards you 
                            #are actually going in negative direction.
                            if unit.team == 1:
                                if i[1] < position[1]:
                                    path.append(i)
                            else:
                                if i[1] > position[1]:
                                    path.append(i)
                return path
                
            elif unit.type == "King":
            
                #Check neighbours to see if there is a possible jump
                for i in pawn_neighs:   
                    if not i == None:
                        if not i.team == unit.team:
                            path = jump(position)
                            
                if len(path) == 1:
                    if path[0] == position:
                        #If no jumps available check neighbours for an 
                        # empty space
                        for i in neighs:
                            if (self.get_unit_at_pos(i) == None):
                                path.append(i)
                    
                elif path == []:

                    #No neighbouring enemy pieces check neighbours for 
                    # an empty space
                    for i in neighs:
                        if (self.get_unit_at_pos(i) == None):
                            path.append(i)
                return path


    def move(self,position, unit, path):
        neighbourNew, neighbourOld = self.map.neighbours(position), self.map.neighbours(unit.position)
        while unit.position in path:
            path.remove(unit.position)
        for i in neighbourOld:
            if i in neighbourNew:
                Pieces.deactivate(self.get_unit_at_pos(i))

        unit.tile_x = position[0]
        unit.tile_y = position[1]
        unit.position = position
        while unit.position in path:
            path.remove(position)
        for i in neighbourOld:
            if i in path:
                path.remove(i)
        self.kingME(unit)
        self.active_units = Pieces.active_units
        return path

    def kingME (self, unit):
        
        if (unit.team == 0 and unit.position[1] == 7) or (unit.team == 1 and unit.position[1] == 0):
            unit.type = "King"
            unit.piece = unit.type + str(unit.team)
            unit.image = pygame.image.load("assets/"+unit.piece+".png")
            unit.image = pygame.transform.scale(unit.image, (80,80))
        

    def can_move(self, unit):
	"""
	Check to see if there is a jump available to one of the units.
	If so and the incorrect unit is select it returns False. If no 
	jump is available, or a jump exists for the unit, it returns True. 
	"""

        jumpable_units = []
        
	for i in self.active_units:

            #Only check the units on current team
            pawn_neighs = []
            if i.team == unit.team:
                neighs = self.map.neighbours(i.position)
                
                #check to see if there is a jump
                for u in neighs:
                    pawn_neighs.append(self.get_unit_at_pos(u))
                    
                    if unit.type == "Pawn":
                        
                        #Check neighbours to see if there is a possible jump
                        for j in pawn_neighs:
                            if not j == None:
                                if not j.team == unit.team:
                                    if unit.team == 1:
                                        if j.tile_y < unit.tile_y:
                                            moveable_units.append(i)
                                    else:
                                        if j.tile_y > unit.tile_y:
                                            moveable_units.append(i)
                                            
                    elif unit.type == "King":
			#Check neighbours to see if there is a possible jump
                        for j in pawn_neighs:   
                            if not j == None:
                                if not j.team == unit.team:
                                    moveable_units.append(i)
                                    
                                    
        if unit in moveable_units or moveable_units == []:
            return True
	else:
            return False
