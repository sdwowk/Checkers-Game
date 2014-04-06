import sys, pygame, tiles, checkers
from Gui import GUI
from checkers.pieces import *
from gameplay import *
from Ai import AI

RESOLUTION = pygame.Rect(0, 0, 800, 600)
BG_COLOR = (32, 32, 32)

# Initialize everything
pygame.mixer.pre_init(22050, -16, 2, 512) # Small buffer for less sound lag
pygame.init()
pygame.display.set_caption("Checkers")
main_gui = GUI(RESOLUTION, BG_COLOR)
clock = pygame.time.Clock()
argv = sys.argv[1:]

# If a filename was given, load that level. Otherwise, load a default.
level = "CheckersBoard"
if len(argv) > 0:
    level = argv[0]
new_units = main_gui.load_level("GameBoard/" + level + ".lvl")
for i in new_units:

    Checkers = Pieces(i[0],i[1],i[2],i[3])

gameplay = Gameplay(main_gui.map, Checkers.active_units)
ai = AI(Checkers.active_units)

path = None

# The main game loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        # End if q is pressed
        elif (event.type == pygame.KEYDOWN and
        (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            pygame.display.quit()
            sys.exit()
        # Respond to clicks
        elif event.type == pygame.MOUSEBUTTONUP:
            tile_x,tile_y = main_gui.on_click(event)
            
            if main_gui.select_state == True:
                
                unitnew = gameplay.get_unit_at_pos((tile_x, tile_y))
                
                if not unitnew == None:
                    if unitnew.team == main_gui.current_team:
                        print(main_gui.current_team)
                        path = gameplay.set_path((tile_x, tile_y))
                        main_gui.moveable_tiles = path
                        print(path)
                        main_gui.draw_path()
                        unitold = unitnew
       
                elif not path == None:
                    if (tile_x, tile_y) in path:
                        path = gameplay.move((tile_x, tile_y), unitold, path)
                    if path == []:
                        #Returns None so that there is no path
                        path = main_gui.end_turn_processed()  
                if main_gui.current_team == 1:
                    while path == None or len(path) < 1:
                        unit = ai.move()
                        path = gameplay.set_path(unit.position)
                    path = gameplay.move(path[0], unit, path)
                    if path == []:
                        path = main_gui.end_turn_processed()
                        
    main_gui.update()
    main_gui.draw(gameplay.active_units)
    clock.tick(60)
 
