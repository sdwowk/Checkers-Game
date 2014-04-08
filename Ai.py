import tiles, pygame, sys, random
from Gui import GUI
from checkers.pieces import *
from gameplay import *


class AI:
    """
    A very dumb AI. The main program that runs the game (main.py) must hold a
    while loop until the AI randomly selects a unit that can move. Once a 
    moveable unit has been select, that move is executed.
    
    """

    def __init__(self, active_units):
        self.active_units = active_units
        self.team = 1

    def move(self):
        path = []
        team_units = []
        for i in self.active_units:
            if i.team == self.team:
                team_units.append(i)
        rand_index = random.randint(0,len(team_units)-1)
        move_unit = team_units[rand_index]
        return move_unit
            
            
class SmartAI:
    """
    Looks at all of its potential moves and tries to pick one where it does
    not make itself vulnerable to attack.
    """

    def __init__(self, Game):
        self.active_units = Game.active_units
        self.team = 1
        self.game = Game

    def move(self):
        team_units = []
        for i in self.active_units:
            if i.team == self.team:
                team_units.append(i)
        
        return team_units

    def vulnerable(self, choices, unit):
        #Checks vulnerability within path
        for position in choices:
            neighbours = self.game.map.neighbours(position)
            pawn_neighs = []
            for i in neighbours:
                pawn_neighs.append(self.game.get_unit_at_pos(i))
                
            for i in pawn_neighs:
                if not i == None:
                        if self.can_jump(i, position, unit):
                            return True
        return False
                        
    def can_jump(self, unit, dest, dest_unit):
        """
        Calculates whether or not a unit can jump.
        """

        i = dest

        if self.game.can_move(unit):
            #Kings are not dependant on team
            if unit.type == "King":
                if unit.tile_x > i[0]:
                    if unit.tile_y > i[1]:
                        pos_move = self.game.get_unit_at_pos(((i[0]-1), (i[1]-1)))
                        if pos_move == None or pos_move == dest_unit:
                            return True
                    else:
                        pos_move = self.game.get_unit_at_pos(((i[0]-1), (i[1]+1)))
                        if pos_move == None or pos_move == dest_unit:
                            return True
                else:
                    if unit.tile_y > i[1]:
                        pos_move = self.game.get_unit_at_pos(((i[0]+1), (i[1]-1)))
                        if pos_move == None or pos_move == dest_unit:
                            return True
                    else:
                        pos_move = self.game.get_unit_at_pos(((i[0]+1), (i[1]+1)))
                        if pos_move == None or pos_move == dest_unit:
                            return True

            #Team 0 pawn
            elif unit.team == 0:
                if dest_unit.team == 1:
                    if unit.tile_y < i[1]:
                        if i[0] > unit.tile_x:
                            pos_move = self.game.get_unit_at_pos(((i[0]+1), (i[1]+1)))
                            if pos_move == None or pos_move == dest_unit:
                                return True
                        else:
                            pos_move = self.game.get_unit_at_pos(((i[0]-1), (i[1]+1)))
                            if pos_move == None or pos_move == dest_unit:
                                return True
            #Team 1 pawn
            else:
                if unit.tile_y > i[1]:
                    if dest_unit.team == 0:
                        if i[0] > unit.tile_x:
                            pos_move = self.game.get_unit_at_pos(((i[0]-1), (i[1] -1)))
                            if pos_move == None or pos_move == dest_unit:
                                return True
                        else:
                            pos_move = self.game.get_unit_at_pos(((i[0]+1), (i[1]-1)))
                            if pos_move == None or pos_move == dest_unit:
                                return True

        return False

    def find_path(self):
        memo = {}
        team_units = self.move()
        for i in team_units:
            memo[i] = self.game.set_path(i.position)
        
        bad_moves = {}
        good_moves = {}

        for (k,v) in memo.items():
            if v == [] or self.vulnerable(v, k) == True:
                bad_moves[k] = v
            else:
                good_moves[k] = v

        if good_moves:
            maxpath = []
            unit = 0
            for k,v in good_moves.items():
                if len(v) >= len(maxpath):
                    maxpath = v
                    unit = k
            return  unit, maxpath
        else:
            maxpath = []
            unit = 0
            for k,v in bad_moves.items():
                if len(v) >= len(maxpath):
                    maxpath = v
                    unit = k
                    
            if maxpath == []:
                path = ["Over"]
                unit = None
                return unit, path
            return unit, maxpath
