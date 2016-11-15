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

    def get_state(self):
        state = ""
  	    # Want to sort the list based on unit id
        tempList = sorted(self.active_units, key=lambda x: x.id, reverse=False)
        for i in tempList:
            state += str(i.team) + " " + i.type + " " + str(i.tile_x) + " " + str(i.tile_y) + " "
        return state    

    def get_unit_at_pos(self, pos):
        """
        Returns the active unit at the given tile position, or None if no 
        unit is present.
        """

        #Check to have position in tuple or two seperate variables
        for u in self.active_units:
            if (u.position) == pos:
                return u
            
        return None

    def set_path(self, position):
        """
        Finds the path for a unit. Calls the jump method which uses recursion
        to compute the path if a jump is available. Returns an empty path
        if there is no move for the unit or if another unit has a jump.
        """
       
        path = []
        pawn_neighs = []
        unit = self.get_unit_at_pos(position)
        # Checks to see if there is a jump for another unit or if your unit
        # has a jump if not returns None.
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
                            path += self.jump(position, unit, path)
                        
            
                if len(path) >= 1:
                    while not path == [] and path[0] == position:
                        
                        #Dont want starting postion in the path
                        path.remove(path[0])
                        
                if path == []:
                    #No neighbouring enemy pieces, check neighbours for 
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
                    while position in path:
                        path.remove(position)

                return path
                
            elif unit.type == "King":
            
                #Check neighbours to see if there is a possible jump
                for i in pawn_neighs:   
                    if not i == None:
                        if not i.team == unit.team:
                            path += self.jump(position, unit, path)
                            
                while position in path:
                    path.remove(position)
                    
                if path == []:

                    #No neighbouring enemy pieces check neighbours for 
                    # an empty space
                    for i in neighs:
                        if (self.get_unit_at_pos(i) == None):
                            if self.map._tile_exists(i):
                                path.append(i)
                    while position in path:
                        path.remove(position)

                return path


    def move(self,position, unit, path):
        """
        Updates the units position and the path by removing unreachable
        positions in the original path. Also handles deleting pieces an 
        whether the game is over.
        """

        tempunit = unit
        if not self.is_reachable(unit,position):
            return path
        else:
            neighbourNew, neighbourOld = self.map.neighbours(position), self.map.neighbours(unit.position)

            #Delete any occurence of the units old position
            while unit.position in path:
                path.remove(unit.position)

            #If there is the same neighbour in both the new and old positions
            # a jump has ocurred and the jumped unit must be removed.
            for i in neighbourOld:
                if i in neighbourNew:
                    Pieces.deactivate(self.get_unit_at_pos(i))
                if i in path:
                    path.remove(i)
            list0 = []
            list1 = []
            for i in Pieces.active_units:
                if i.team == 0:
                    list0.append(i)
                else:
                    list1.append(i)
            if list0 == [] or list1 == []:
                return ["Over"]
 
        #updating the unit's positions
        unit.tile_x = position[0]
        unit.tile_y = position[1]
        unit.position = position

       #Get rid of old sections of the path
        for i in path:
            #If a position was reachable but now is not remove it from path
            if (self.is_reachable(tempunit, i) and not 
                self.is_reachable(unit, i)):
                path.remove(i)



        #Delete the new position from path, to make sure the piece can't 
        #travel back over the same position in a single turn
        while unit.position in path:
            path.remove(position)

        #Update units
        self.active_units = Pieces.active_units

        if path == []:
            path = ["Done"]
            
            #Check to see if the piece is a king
            self.kingME(unit)
            self.active_units = Pieces.active_units
            return path
        else:
            self.kingME(unit)

            if not self.can_move(unit):
                path = ["Done"]
            self.active_units = Pieces.active_units
            return path

    def kingME (self, unit):
        """
        Updates the unit type and image if he is a king
        """
        if ((unit.team == 0 and unit.tile_y == 7) or 
            (unit.team == 1 and unit.tile_y == 0)):
            unit.type = "King"
            unit.piece = unit.type + str(unit.team)
            unit.image = pygame.image.load("assets/"+unit.piece+".png")
            unit.image = pygame.transform.scale(unit.image, (80,80))
        
 
    def jump(self, new_pos, unit, jump_path):
        """
        Calculates the path of a piece that can jump using recursion. This
        function does use specific indexing according to the neighbours
        method in tiles.py. For pawns there is a need to check whether a
        piece has a piece in front of it, if that piece is from the other 
        team, if the space behind the jump piece is free and does a team 
        check to make sure pawns can't move in the wrong direction.
        """
        
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
                                    if open_areas[i] not in jump_path:
                                        if self.map._tile_exists(open_areas[i]):
                                            self.jump(open_areas[i], unit, jump_path)
                            else:
                                if open_areas[i][1] > new_pos[1]:
                                    if open_areas[i] not in jump_path:
                                        if self.map._tile_exists(open_areas[i]):
                                            self.jump(open_areas[i], unit, jump_path)
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
                                if self.map._tile_exists(open_areas[i]):
                                    self.jump(open_areas[i], unit, jump_path)
            return jump_path    



    def can_move(self, unit):
        """
        Check to see if there is a jump available to one of the units.
        If so and the incorrect unit is select it returns False. If no 
        jump is available, or a jump exists for the unit, it returns True. 
        """
        
        jumpable_units = []
        
        for i in self.active_units:
            path = []
            #Only check the units on current team
            if i.team == unit.team:
                path += self.jump(i.position, i, path)

                #Position of the current piece should not be in the path
                while i.position in path:
                    path.remove(i.position)

                #If the path is not empty it has a jump available
                if not path == []:
                    jumpable_units.append(i)

                                    
        if (unit in jumpable_units) or (jumpable_units == []):
            return True
        else:
            return False


    def is_reachable(self,unit,position):
        """
        Used to check if a click on the board is reachable by the current
        unit. Also used in path clearing since a unit can move at most 2
        tiles in the x and y direction at one time.
        """

        dxy = 2
        if (position[0] <= (unit.tile_x + dxy) and 
            position[0] >= (unit.tile_x - dxy)):

            if unit.team == 0:
                if unit.type == "Pawn":
                    if (position[1] <= unit.tile_y + dxy and 
                        not unit.tile_y - position[1] == 0):
                        
                        return True
                else:
                    if (position[1] <= unit.tile_y + dxy and 
                        position[1] >= unit.tile_y-dxy):
                        return True
            else:
                if unit.type == "Pawn":
                    if (position[1] >= unit.tile_y - dxy and 
                        not unit.tile_y - position[1] == 0):
                        
                        return True
                else:
                    if (position[1] <= unit.tile_y + dxy and
                        position[1] >= unit.tile_y-dxy):
                        return True
        return False
