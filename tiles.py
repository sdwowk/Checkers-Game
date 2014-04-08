import pygame, sys, math
import pygame.gfxdraw
from pygame.sprite import Sprite
from collections import namedtuple

# A container class which stores information about a tile.
Tile = namedtuple('Tile', ['type',
                           'sprite_id',
                           'passable'])

# a dictionary of tile IDs associated with their type data
tile_types = {
    0:  Tile('Black', 0, True),
    1:  Tile('White', 1, False),
}

HIGHLIGHT_RATE = 0.0025
GRID_COLOR = (0, 0, 0, 80)

class TileMap(Sprite):
    """
    A class which renders a grid of tiles from a spritesheet.
    """
    
    def __init__(self, sheet_name, tile_width, tile_height):
        """
        sheet_name: the filename of the sprite sheet to use
        tile_width: the width of each tile, in pixels
        tile_height: the height of each tile, in pixels
        """
        
        # Set up map info
        self._sprite_sheet = pygame.image.load(sheet_name)

        self._tile_width = tile_width
        self._tile_height = tile_height
        self._map_width = None
        self._map_height = None
        self._tiles = []
        self._highlights = {}
        
        Sprite.__init__(self)
        
        # These are required for a pygame Sprite
        self.image = None
        self._base_image = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        
    def _tile_count(self):
        """
        Returns the number of tiles on the map.
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t._tile_count()
        64
        """
        return int(self._map_width/self._tile_width) * int(self._map_height/self._tile_height)
        
    def _tile_position(self, index):
        """
        Returns a tile's coordinates in tile units within the map given its
        index in the list.
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t._tile_position(2)
        (2, 0)
        >>> t._tile_position(18)
        (2, 2)
        >>> t._tile_position(20)
        (4, 2)
        """
        return (index % int(self._map_width/self._tile_width), index // int(self._map_width/self._tile_width))
                
    def _tile_exists(self, coords):
        """
        Returns true if a tile exists, or false if it doesn't
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t._tile_exists((2, 2))
        True
        >>> t._tile_exists((-2, -1))
        False
        >>> t._tile_exists((9, 7))
        False
        """
        return not (
            coords[0] < 0 or
            coords[0] >= (self._map_width/self._tile_width) or
            coords[1] < 0 or
            coords[1] >= self._map_height/self._tile_width)
        
    def _tile_index(self, coords):
        """
        Returns a tile's index in the list given its tile coordinates in tile
        units. Returns -1 if the provided coordinates are invalid.
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t._tile_index((2, 2))
        18
        >>> t._tile_index((7, 7))
        63
        """
        if not self._tile_exists(coords): return -1

        #make sure to cast to int because input is sometimes floats
        #There won't be rounding errors though because the numbers
        #are just integers with .0 after
        return int(coords[1] * (self._map_width/self._tile_width) + int(coords[0]))
        
    def _get_highlight_color(self, colorA, colorB):
        """
        Returns the movement color, which changes based on time.
        """
        # This produces a sine wave effect between a and b.
        sin = (math.sin(pygame.time.get_ticks() * HIGHLIGHT_RATE) + 1) * 0.5
        effect = lambda a, b: a + sin * (b - a)
        
        r = effect(colorA[0], colorB[0])
        g = effect(colorA[1], colorB[1])
        b = effect(colorA[2], colorB[2])
        a = effect(colorA[3], colorB[3])
        
        return (r, g, b, a)
        
    def _render_base_image(self, redraw = []):
        """
        Redraws all the tiles onto the base image.
        """
        # Create the empty surface
        self._base_image = pygame.Surface(
            (self._map_width,
            self._map_height)
        )
        
        # draw in each tile
        for i in range(self._tile_count()):
            tile_id = tile_types[self._tiles[i]].sprite_id
            
            # get its position from its index in the list
            x, y = self._tile_position(i)
            x *= self._tile_width
            y *= self._tile_height
            
            # determine which subsection to draw based on the sprite id
            area = pygame.Rect(
                tile_id * self._tile_width,
                0,
                self._tile_width,
                self._tile_height
            )
            
            # draw the tile
            self._base_image.blit(self._sprite_sheet, (x, y), area)
            
    def _set_tiles(self, tiles):
        """
        Sets the list of tiles.
        """
        self._tiles = tiles[:]
        
        # The image now needs to be redrawn
        self._render_base_image()
            
    def get_tiles(self):
        """
        Returns a copy of the list of tiles.
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> len(t.get_tiles())
        64
        """
        return self._tiles[:]
            
    def load_from_file(self, filename):
        """
        Loads tile data from the given image file.
        The image file should be have an 8-bit indexed palette. Each colour
        index corresponds to the tile (e.g. colour index 2 = tile type 2)
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t.rect
        <rect(0, 0, 640, 640)>
        """
        tiles = []
        
        # Load in the map image.
        map_image = pygame.image.load(filename)
        self._map_width, self._map_height = map_image.get_size()
        self._map_width = self._map_width * 20
        self._map_height = self._map_height * 20

        self.rect.w = self._map_width
        self.rect.h = self._map_height
        
        # Go through the image adding tiles
        map_tiles = []
        for y in range(int(self.rect.w/self._tile_height)):
            for x in range(int(self.rect.h/self._tile_width)):
                # The tile number corresponds to the pixel colour index
                tiles.append(map_image.get_at_mapped((int(x*4), int(y*4))))
        
        # Set the tiles
        self._set_tiles(tiles)
        
    def get_tile_size(self):
        """
        Returns a tuple containing a tile's width and height within this map.
        
        >>> t = TileMap("assets/tiles.png", 80, 80)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t.get_tile_size()
        (80, 80)
        """
        return (self._tile_width, self._tile_height)
        
    def tile_coords(self, screen_coords):
        """
        Returns the tile coordinates within this TileMap that the given screen
        coordinates fall into.
        
        >>> t = TileMap("assets/tiles.png", 20, 20)
        >>> t.load_from_file("maps/test-1.gif")
        >>> t.tile_coords((45, 22))
        (2, 1)
        """
        x, y = screen_coords
        return math.floor((x - self.rect.left) / self._tile_width), math.floor((y - self.rect.top) / self._tile_height)
        
        
    def screen_coords(self, tile_coords):
        """
        Returns the screen coordinates of a given tile.
        
        >>> t = TileMap("assets/tiles.png", 20, 20)
        >>> t.load_from_file("maps/test-1.gif")
        >>> t.screen_coords((3, 4))
        (60, 80)
        """
        x, y = tile_coords
        return (
            x * self._tile_width + self.rect.x,
            y * self._tile_height + self.rect.y
        )
        
    def tile_data(self, coords):
        """
        Returns the tile data for a given tile.
        
        >>> t = TileMap("assets/tiles.png", 20, 20)
        >>> t.load_from_file("maps/test-1.gif")
        >>> t.tile_data((0, 0)) == tile_types[0]
        True
        >>> t.tile_data((1, 1)) == tile_types[6]
        True
        
        """
        if not self._tile_exists(coords): return False
        
        index = self._tile_index(coords)
        
        return tile_types[self._tiles[index]]
        
    def neighbours(self, coords):
        """
        Returns all neighbour coordinates to a given tile. Does not return
        coordinates which do not exist.
        
        >>> t = TileMap("assets/tiles.png", 20, 20)
        >>> t.load_from_file("GameBoard/CheckersBoard.gif")
        >>> t.neighbours((0, 0))
        [(1, 1)]
        >>> t.neighbours((4, 4)) == [(5, 5), (3, 5), (5, 3), (3, 3)]
        True
        >>> t.neighbours((1, 1)) == [(2, 2), (0, 2), (2, 0), (0, 0)]
        True
        """
        x, y = coords
        
        # The possible neighbouring tiles.
        neighbours = [
            (x + 1, y + 1),
            (x - 1, y+1),
            (x + 1, y-1),
            (x - 1, y - 1)
        ]
        
        # Return only those which exist.
        return [n for n in neighbours if self._tile_exists(n)]
        
    def set_highlight(self, name, colorA, colorB, tiles):
        """
        Sets the given list of tile coordinates to be highlighted in the given
        color and wave between the first and second colors.
        It will be stored under the given name.
        """
        self._highlights[name] = (tiles, colorA, colorB)

        
    def remove_highlight(self, name):
        """
        Removes highlights of the given colour. If the highlights do not
        exist, does nothing.
        """
        if name in self._highlights:
            del self._highlights[name]
            
    def clear_highlights(self):
        """
        Removes all highlights.
        """
        self._highlights.clear()
        
    def update(self):
        """
        Overrides the default update function for sprites. This updates
        the image.
        """
        # copy over the base image
        self.image = self._base_image.copy()

            
                
        # draw the highlights
        for name, (tiles, colorA, colorB) in self._highlights.items():
            for coord in tiles:
                tile_rect = pygame.Rect(
                    coord[0] * self._tile_width,
                    coord[1] * self._tile_height,
                    self._tile_width,
                    self._tile_height
                )
                pygame.gfxdraw.box(self.image,
                                   tile_rect,
                                   self._get_highlight_color(colorA, colorB))

        # draw the grid
        for x in range(0,
                        self._map_width,
                        self._tile_width):
            pygame.gfxdraw.vline(
                self.image,
                x,
                0,
                self._map_height,
                GRID_COLOR
            )
        for y in range(0,
                        self._map_height,
                        self._tile_height):
            pygame.gfxdraw.hline(
                self.image,
                0,
                self._map_width,
                y,
                GRID_COLOR
            )
    

