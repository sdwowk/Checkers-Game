import tiles, pygame, sys, random
from Gui import GUI
from checkers.pieces import *
from gameplay import *


class AI:

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
            
            
        
