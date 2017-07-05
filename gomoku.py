import pygame
from pygame.locals import *

# Define some colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 222, 173)

PLAYER = False

# Define grid globals
HEIGHT = 20
WIDTH = 20
MARGIN = 5
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 380, 380
        self.grid = [[0 for x in range(15)] for y in range(15)]

 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(RED) 
        pygame.display.set_caption('Gomoku')
        

        # Draw the grid
        for row in range(15):
            for column in range(15):
                if column == 7 and row == 7:
                    color = WHITE
                    self.grid[7][7] = 1
                else:
                    color = YELLOW
                pygame.draw.rect(self._display_surf, color,
                                 [(MARGIN + HEIGHT) * column + MARGIN,
                                  (MARGIN + WIDTH) * row + MARGIN,
                                  HEIGHT,
                                  WIDTH])
                pygame.display.update()
        
        self._running = True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            c = pos[0] // (20+5)
            r = pos[1] // (20+5)
            
            global PLAYER
            
            if self.grid[c][r] == 0:
                self.grid[c][r] = 1
                
                if PLAYER:
                    color = WHITE
                    self.grid[c][r] = 1
                else:
                    color = BLACK
                    self.grid[c][r] = 2
                    
                pygame.draw.rect(self._display_surf, color,
                                 [(MARGIN + HEIGHT) * c + MARGIN,
                                  (MARGIN + WIDTH) * r + MARGIN,
                                  HEIGHT,
                                  WIDTH])
                pygame.display.update()
                self.check_win([c, r], PLAYER)

                PLAYER = not PLAYER
            
    def on_loop(self):
        pass

    
    def on_render(self):
        pass

    
    def on_cleanup(self):
        pygame.quit()

 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def check_win(self, currentPosition, player):
        print 'OKIDOKI BOYYYY'
        # checko horizontal
        # check vertical
        # check side /
        # check other side \
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
