import pygame
from pygame.locals import *

# Define some colors
BLACK  = (0, 0, 0)
WHITE  = (245, 245, 245)
RED    = (255, 0, 0)
YELLOW = (205, 164, 131)
GREEN  = (0, 255, 0)
BACKGROUND = (64,41,22)

PLAYER = False

# Define grid globals
WIDTH = 20
MARGIN = 1
PADDING = 20
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = (WIDTH + MARGIN) * 15 + MARGIN + PADDING * 2, (WIDTH + MARGIN) * 15 + MARGIN + PADDING * 2
        self.grid = [[0 for x in range(15)] for y in range(15)]

 
    def on_init(self):
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(YELLOW) 
        pygame.display.set_caption('Gomoku')
        
        # Draw background rect for game area

        pygame.draw.rect(self._display_surf, BACKGROUND,
                         [PADDING,
                          PADDING,
                          (WIDTH + MARGIN) * 15 + MARGIN,
                          (WIDTH + MARGIN) * 15 + MARGIN]) 

        # Draw the grid
        for row in range(15):
            for column in range(15):
                color = YELLOW
                pygame.draw.rect(self._display_surf, color,
                                 [(MARGIN + WIDTH) * column + MARGIN + PADDING,
                                  (MARGIN + WIDTH) * row + MARGIN + PADDING,
                                  WIDTH,
                                  WIDTH])
                pygame.display.update()
        
        self._running = True

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            c = (pos[0] - PADDING) // (WIDTH+MARGIN)
            r = (pos[1] - PADDING) // (WIDTH+MARGIN)
            
            if 0 <= c < 15 and 0 <= r < 15:
                global PLAYER
                
                if self.grid[c][r] == 0:
                    self.grid[c][r] = 1
                    
                    if PLAYER:
                        color = WHITE
                        self.grid[c][r] = 1
                    else:
                        color = BLACK
                        self.grid[c][r] = 2
                        
                    pygame.draw.circle(self._display_surf, color,
                                     ((MARGIN + WIDTH) * c + MARGIN + WIDTH / 2 + PADDING,
                                      (MARGIN + WIDTH) * r + MARGIN + WIDTH / 2 + PADDING),
                                      WIDTH / 2 - MARGIN,0)
                    
                    
                    # check win
                    if self.check_win([c,r],PLAYER):
                        win = "Player 1 win" if PLAYER else "Player 2 win"
                        myfont = pygame.font.SysFont('Comic Sans MS', 30)
                        text_surface = myfont.render(win, False, (0, 0, 0))
                        self._display_surf.blit(text_surface, (0,0))

                        # Incomplete button functionalit for new_game
                        pygame.draw.rect(self._display_surf, GREEN,(50,150,100,50))
                        pygame.draw.rect(self._display_surf, RED,(250,150,100,50))
                        

                    PLAYER = not PLAYER
            
    def on_loop(self):
        pass

    
    def on_render(self):
        pygame.display.update()
        

    
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
    
    def check_win(self,position,player):
        target = 1 if player else 2
        if self.grid[position[0]][position[1]] != target:
            return False
        directions = [([0,1] , [0,-1]) , ([1,0] , [-1,0]) , ([-1,1] , [1,-1]) , ([1,1] , [-1,-1])]
        for direction in directions:
            continue_chess = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < 15 and 0 <= p[1] < 15:
                    if self.grid[p[0]][p[1]] == target:
                        continue_chess += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if continue_chess >= 6:
                return True
        return False

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
