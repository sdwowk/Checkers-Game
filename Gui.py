import sys, pygame
import random
import tiles,checkers

from checkers.pieces import *
from pygame.sprite import LayeredUpdates
from collections import namedtuple

#Code given in class. Math has been refactored to be more general and use less magic numbers

#Game specific constants
MAP_WIDTH = 640
BAR_WIDTH = 160
BUTTON_HEIGHT = 50
CENTER = 80

# Set the fonts
pygame.font.init()
FONT_SIZE = 16
BIG_FONT_SIZE = 42
FONT = pygame.font.SysFont("Arial", FONT_SIZE)
BIG_FONT = pygame.font.SysFont("Arial", BIG_FONT_SIZE)
BIG_FONT.set_bold(True)

# padding for left and top side of the bar
PAD = 6

# RGBA colors for grid stuff
SELECT_COLOR = (255, 255, 0, 255)
UNMOVED_COLOR = (0, 0, 0, 255)
MOVE_COLOR_A = (0, 0, 160, 120)
MOVE_COLOR_B = (105, 155, 255, 160)

# RGB colors for the GUI
FONT_COLOR = (250, 0, 0)
BAR_COLOR = (150, 150, 150)
OUTLINE_COLOR = (50, 50, 50)
BUTTON_HIGHLIGHT_COLOR = (255, 255, 255)
BUTTON_DISABLED_COLOR = (64, 64, 64)


# Names for the different teams
TEAM_NAME = {
    0: "grey",
    1: "red"
}

class Modes:
    Select, ChooseHeads, ChooseTails, GameOver, EndTurn = range(5)
    
Button = namedtuple('Button', ['slot', 'text', 'onClick', 'condition'])

class GUI(LayeredUpdates):
    """
    A large portion of code from the GUI was taken from assignment 4. The 
    biggest modification from assignment 4 however is the introduction of
    a model view controller design to the GUI.
    """
    num_instances = 0

    def Simulation_pressed(self):
        """
        A future milestone to have two AI's play against each other.
        Used to ask user to select Heads or Tails at this point in time.
        """
        pass

    def HeadsPressed(self):
        #Button can only be pressed once
        if not self.can_choose():
            return
        else:
            heads = random.randint(0,1)
            x = random.randint(0,1)
            if x == heads:
            #player1 goes first
                self.select_state = True
                return
            else:
            #Computer goes first
                self.select_state = True
                self.end_turn_processed()
        
    def TailsPressed(self):
        #Button can only be pressed once
        if not self.can_choose():
            return
        else:
            tails = random.randint(0,1)
            x = random.randint(0,1)
            if x == tails:
                #Player goes first
                self.select_state = True
                return

            else:
                #Computer goes first
                self.select_state = True
                self.end_turn_processed()

    def __init__(self, screen_rect, bg_color):
        """
        Initialize the display.
        screen_rect: the bounds of the screen
        bg_color: the background color
        """
        LayeredUpdates.__init__(self)
        
        if GUI.num_instances != 0:
            raise Exception("GUI: can only have one instance of a simulation")
        GUI.num_instances = 1
        
        # Set up the screen
        self.screen = pygame.display.set_mode((screen_rect.w, screen_rect.h))
        self.screen_rect = screen_rect
        
        # The rect containing the info bar
        self.bar_rect = pygame.Rect(screen_rect.w - BAR_WIDTH,
                                     0,
                                     BAR_WIDTH,
                                     screen_rect.h)
        
        # The rect containing the map view
        self.view_rect = pygame.Rect(0,
                                      0,
                                      MAP_WIDTH,
                                      screen_rect.h)
        self.bg_color = bg_color
        self.map = None

        # Set up team information
        self.num_teams = None
        self.current_team = 0
        self.win_team = None 

        # The currently selected unit
        self.sel_unit = None
        self.moveable_tiles = []
       
        # Haven't determined who goes first yet.
        self.select_state = False
 
        # Set up GUI
        self.buttons = [
            Button(0, "Heads", self.HeadsPressed, self.can_choose),
            Button(1, "Tails", self.TailsPressed, self.can_choose),
            Button(2, "Choose Below", self.Simulation_pressed, None),
            Button(3, "EndTurn", self.end_turn_processed, None)]
        
        # We start in select mode
        self.mode = Modes.Select

    def load_level(self, filename):
        """
        Loads a map from the given filename. Modified from assignment four to
        work properly with MVC design
        """
        self.remove(self.map)
        
        map_file = open(filename, 'r')
        
        # Move up to the line with the team count
        line = map_file.readline()
        while line.find("Teams: ") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected team count")
        
        # Get the number of teams
        line = line.lstrip("Teams: ")
        self.num_teams = int(line)
        
        # Move up to the line with the tile sprites
        line = map_file.readline()
        while line.find("Tiles: ") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected tile file")
        
        # Get the number of teams
        line = line.lstrip("Tiles: ")
        line = line.strip()
        tile_filename = line
        
        # Move up to the line with the tile size
        line = map_file.readline()
        while line.find("Tile size: ") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected tile size")
        
        # Get the number of teams
        line = line.lstrip("Tile size: ")
        line = line.strip()
        size = line.split('x')
        tile_w, tile_h = size
        
        # Convert to ints
        tile_w = int(tile_w)
        tile_h = int(tile_h)
        
        # Move up to the line with the map file
        line = map_file.readline()
        while line.find("Map: ") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected map filename")
        
        # Get the map filename
        line = line.lstrip("Map: ")
        line = line.strip()
        map_filename = line
        
        # Create the tile map
        self.map = tiles.TileMap(tile_filename, tile_w, tile_h)
        
        self.map.load_from_file(map_filename)
        self.add(self.map)
        
        # Center the map on-screen
        self.map.rect.center = self.view_rect.center
        
        # Move up to the unit definitions
        while line.find("UNITS START") < 0:
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected unit definitions")
        line = map_file.readline()
        #Creating a list for the new units
        new_unit = []
        
        # Create the units
        while line.find("UNITS END") < 0:
            line = line.rstrip()
            line = line.split(' ')
            unit_name = line[0]
            unit_team = int(line[1])
            unit_x, unit_y = int(line[2]), int(line[3])
            unit_id = int(line[4])
            
            new_unit.append((unit_team,unit_x, unit_y, True, unit_id))
                        
            line = map_file.readline()
            if line == "":
                raise Exception ("Expected end of unit definitions")
        return new_unit

    def on_click(self, e):
        """
        This is called when a click event occurs.
        e is the click event. Modified from assignment four.
        """
        # Don't react when in move, attack or game over mode.
        if (self.mode == Modes.GameOver):
            return
        
        # make sure we have focus and that it was the left mouse button
        if (e.type == pygame.MOUSEBUTTONUP
            and e.button == 1
            and pygame.mouse.get_focused()):
            
            # If this is in the map, we're dealing with units or tiles
            if self.map.rect.collidepoint(e.pos):
                # Get the tile's position
                tile_x, tile_y = self.map.tile_coords(e.pos)

                return tile_x, tile_y
                
            else:
                # Check which button was pressed
                for button in self.buttons:
                    # If the button is enabled and has a click function, call
                    # the function
                    if ((not button.condition or button.condition()) and self.get_button_rect(button).collidepoint(e.pos)):
                        
                        button.onClick()
                #Click was off of the tile grid return a values that won't
                #effect the game
                return 9, 9
        else:
            return 9, 9
                        

    def draw(self, active_units):
        """
        Render the display. Modified code from assignment four to be more
        applicable to checkers.
        """
        # Fill in the background
        self.screen.fill(self.bg_color)
        
        # Update and draw the group contents
        LayeredUpdates.draw(self, self.screen)
        
        # draw units
        for u in active_units:
            u.rect.x,u.rect.y = self.update_unit_rect(u)
        active_units.draw(self.screen)
        
        for i in self.buttons:
            self.draw_bar_button(i)

        # Draw the win message
        if self.mode == Modes.GameOver:
            # Determine the message
            win_text = "TEAM {} WINS!".format(
                TEAM_NAME[self.win_team].upper())
            
            #Clear Highlights
            self.map.clear_highlights()

            # Render the text
            win_msg = BIG_FONT.render(
                win_text,
                True,
                FONT_COLOR)
                
            # Move it into position
            msg_rect = pygame.Rect((0, 0), win_msg.get_size())
            msg_rect.center = (MAP_WIDTH / 2, self.screen.get_height() / 2)
            
            # Draw it
            self.screen.blit(win_msg, msg_rect)

        # Update the screen
        pygame.display.flip()

    def draw_bar_title(self, text, line_num):
        """
        Draws a title at a specified line number with the specified text.
        Same as in assignment four.
        """
        title_text = FONT.render(text, True, FONT_COLOR)
        self.screen.blit(
            title_text,
            (self.bar_rect.centerx - (title_text.get_width()/2),
            FONT_SIZE * line_num + PAD))

    def draw_bar_div_line(self, line_num):
        """
        Draws a dividing line at a specified line number. Same as in assignment
        four.
        """
        y = FONT_SIZE * line_num + FONT_SIZE//2 + PAD
        pygame.draw.line(
            self.screen,
            (50, 50, 50),
            (self.bar_rect.x, y),
            (self.bar_rect.right, y))
            
    def get_button_rect(self, button):
        """
        Gets the rectangle bounding a button in screen cordinates.
        Same as in assignment four.
        """
        # The y-coordinate is based on its slot number
        y = self.screen.get_height() - BUTTON_HEIGHT * (button.slot + 1)
        return pygame.Rect(self.bar_rect.x,
                            y,
                            self.bar_rect.width,
                            BUTTON_HEIGHT)

    def draw_bar_button(self, button):
        """
        Renders a button to the bar.
        If the mouse is hovering over the button it is rendered in white,
        else rgb(50, 50, 50). Modified from assignment four for our purposes
        """

        but_rect = self.get_button_rect(button)
        
        # The outline needs a slightly smaller rectangle
        but_out_rect = but_rect
        but_out_rect.width -= 1

        # Determine the button color
        but_color = BAR_COLOR
        
        # The button can't be used
        if not self.can_choose():
            but_color = BUTTON_DISABLED_COLOR
        else:
            # The button can be used
            mouse_pos = pygame.mouse.get_pos()
            if but_rect.collidepoint(mouse_pos):
                # Highlight on mouse over
                but_color = BUTTON_HIGHLIGHT_COLOR
        
        # Draw the button
        pygame.draw.rect(self.screen, but_color, but_rect)
            
        # Draw the outline
        pygame.draw.rect(self.screen, OUTLINE_COLOR, but_out_rect, 2)

        # Draw the text
        but_text = FONT.render(button.text, True, FONT_COLOR)
        self.screen.blit(
            but_text,
            (self.bar_rect.centerx - (but_text.get_width()/2),
            but_rect.y + (BUTTON_HEIGHT//2) - but_text.get_height()//2))

    def cur_team(self):
        """
        Gets the current team based on the turn.
        """
        return (self.current_turn) % self.num_teams

    def can_choose(self):
        
        return not self.select_state

        
    def end_turn_processed(self):
        """
        This is called when the end turn button is pressed.
        Advances to the next turn.
        """
     
        # advance turn
        self.current_team += 1 
        self.current_team = self.current_team % 2
        return None

    def update_unit_rect(self, unit):
        """
        Scales a unit's display rectangle to screen coordiantes.
        Same as in assignment four
        """
        rect = []
        x, y = unit.tile_x, unit.tile_y
        screen_x, screen_y = self.map.screen_coords((x, y))
        return screen_x, screen_y

    def draw_path(self):
        # Highlight squares of a path
        self.map.set_highlight(
            "move", MOVE_COLOR_A, MOVE_COLOR_B, self.moveable_tiles)
