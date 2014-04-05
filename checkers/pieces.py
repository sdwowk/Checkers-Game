import pygame, tiles, checkers
from pygame.sprite import Sprite

FRAME_MOVE_SPEED = 3/20
SIZE = 20

class Pieces(Sprite):
    """
    Representation of checker units that contain all the rules for movement.
    This just handles rules of movement, jumping and position on the map. 
    """
    active_units = pygame.sprite.LayeredUpdates()

    #check if we need angle
    def __init__(self, team = -1, tile_x = None, tile_y = None, activate = False):
        Sprite.__init__(self)
        #Default values to assign to later
        self.team = team
        self.tile_x  = tile_x
        self.tile_y = tile_y
        self.position = (tile_x,tile_y)
        self.type = "Pawn" 
        self.piece = self.type + str(self.team)
        self._moving = False
        self._active = False
        self._path = []
        #changed, check if allowed
        self.turn_state = [False]

        #set required pygame things.
        self.image = pygame.image.load("assets/"+self.piece+".png")
        self.rect = pygame.Rect(0, 0, SIZE, SIZE)
        self._update_image()
        
        if activate:
            self.activate()

    @staticmethod
    def get_unit_at_pos(pos):
        """
        Returns the active unit at the given tile position, or None if no unit
        is present.
        """
        #check to have position in tulbe or two seperate variables
        for u in Pieces.active_units:
            if (u.tile_x, u.tile_y) == pos:
                return u
            
        return None
    
    @property
    def active(self):
        """
        Returns whether this is active.
        """
        return self._active
    
    @property
    def is_moving(self):
        """
        Returns whether or not a unit is currently in transit.
        """
        return self._moving
    
    @property
    def tile_pos(self):
        """
        Returns the unit's tile position.
        """
        return (self.tile_x, self.tile_y)

    #might get rid of if we don't need to draw
    def _update_image(self):
        """
        Re-renders the unit's image.
        """
        # Pick out the right sprite depending on the team
        subrect = pygame.Rect(self.team * SIZE,
                              0,
                              self.rect.w,
                              self.rect.h)
        try:
            subsurf = self._base_image.subsurface(subrect)
        except ValueError:
            # No sprite for this team
            raise ValueError(
                "Class {} does not have a sprite for team {}!".format(
                    self.__class__.__name__, self.team))
        except AttributeError:
            # No image is loaded
            return


    def activate(self):
        """
        Adds this unit to the active roster.
        """
        if not self._active:
            self._active = True
            Pieces.active_units.add(self)
    
    def deactivate(self):
        """
        Removes this unit from the active roster.
        """
        if self._active:
            self._active = False
            Pieces.active_units.remove(self)

    

    #changed to get rid of damage
    def is_attackable(self, from_tile, from_pos, to_tile, to_pos):
        """
        Returns whether the given tile is attackable.
        
        Override this for subclasses, perhaps using this as a default value.
        """
        # We can only attack within the unit's range.
        if not self.is_tile_in_range(from_tile, from_pos, to_pos):
            return False
        
        # Get the unit we're going to attack.
        u = Pieces.get_unit_at_pos(to_pos)
        
        # We can't attack if there's no unit there, if it's on our team,
        # if we can't hit this particular unit, or if the damage is 0
        if (not u
            or u.team == self.team
            or not self.can_hit(u)):
            return False
            
        return True

    def can_hit(self, target_unit):
        """
        Determines whether a unit can hit another unit.
        
        Really only used to be overridden in subclasses for special
        effects.
        """
        return True

 
    def turn_ended(self, tile):
        """
        Called when the turn for this unit's team has ended.
        Returns True if the unit is still alive, and False otherwise.
        """
        self.turn_state = [False]
        return True

    def is_tile_in_range(self, from_tile, from_pos, to_pos):
        """
        Checks to see if a tile is in attackable range from its current
        position. Takes tile range bonus into account.
        """
        # Get range
        r = self.max_atk_range
        # Add (or subtract) bonus range from occupied tile
        r += from_tile.range_bonus
        
        dist = helper.manhattan_dist(from_pos, to_pos)
        if dist <= r:
            return True
        return False

    def set_path(self, tile_x, tile_y):
        """
        Tells the unit that it should be moving, where, and how.
        """
        position = tile_pos()
        if self.type == "Pawn":
            if                                                                           ((get_unit_at_pos((position[0]-1),(position[1]+1))).team == self.team)       or ((get_unit_at_pos((position[0]+1),(position[1]+1))).team == self.team):
                #jump function
                pass   


        elif self.type == "King":
            if                                                                           ((get_unit_at_pos((position[0]-1),(position[1]+1))).team == self.team)       or ((get_unit_at_pos((position[0]+1),(position[1]+1))).team == self.team)       or ((get_unit_at_pos((position[0]-1),(position[1]-1))).team == self.team)       or ((get_unit_at_pos((position[0]+1),(position[1]-1))).team == self.team):
                #jump function
                pass

checkers.unit_types["Pawns"] = Pieces
