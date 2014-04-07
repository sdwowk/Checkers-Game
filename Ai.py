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

    def __init__(self, Gameplay):
        self.active_units = Gameplay.active_units
        self.team = 1
        self.game = Gameplay

    def move(self):
        team_units = []
        for i in self.active_units:
            if i.team == self.team:
                team_units.append(i)
        
        return team_units

    def vulnerable(self, unit):
        neighbours = self.game.map.neighbours(unit.position)
        pawn_neighs = []
        for i in neighbours:
            pawn_neighs.append(self.game.get_unit_at_pos(i))
        
        for i in pawn_neighs:
            if not i == None:
                if i.position[1] < unit.position[1]:
                    if i.position[0] > unit.position[0]:
                        tile = (unit.position[0]-1, unit.position[1]+1)
                    else:
                        tile = (unit.position[0]+1, unit.position[1]+1)
                    if not i.team == self.team:
                        if self.game.get_unit_at_pos(tile) == None:
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
            if self.vulnerable(k):
                bad_moves[k] = v
            else:
                good_moves[k] = v

        if good_moves == {}:
            maxpath = []
            unit = 0
            for k,v in bad_moves.items():
                if v > maxpath:
                    maxpath = v
                    unit = k
            return  unit, maxpath
        else:
            maxpath = []
            unit = 0
            for k,v in good_moves.items():
                if v > maxpath:
                    maxpath = v
                    unit = k
            return unit, maxpath
