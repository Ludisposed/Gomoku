import pygame
from pygame.locals import *

# Define some colors
BLACK  = (0, 0, 0)
WHITE  = (245, 245, 245)
RED    = (133, 42, 44)
YELLOW = (205, 164, 131)
GREEN  = (26, 81, 79)
BACKGROUND = (64,41,22)

PLAYER = False

# Define grid globals
WIDTH = 20
MARGIN = 1
PADDING = 20
DOT = 4

BOARD = (WIDTH + MARGIN) * 14 + MARGIN

GAME_WIDTH = BOARD + PADDING * 2
GAME_HIGHT = GAME_WIDTH + 100

 
class Gomoku:
    def __init__(self):
        self.grid = [[0 for x in range(15)] for y in range(15)]
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode((GAME_WIDTH,GAME_HIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.fill(YELLOW) 
        pygame.display.set_caption('Gomoku')
        
        self.gomoku_board_init()
        pygame.display.update()

        self._running = True
        self._playing = False
        self.pieces = []
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        
        
        if event.type == pygame.MOUSEBUTTONUP:
            #does not update postion in python3.6, and I don't know why
            pos = pygame.mouse.get_pos()
            #print(pos)
            c = (pos[0] - PADDING + WIDTH // 2) // (WIDTH+MARGIN)
            r = (pos[1] - PADDING + WIDTH // 2) // (WIDTH+MARGIN)
            
            if 0 <= c < 15 and 0 <= r < 15:
                global PLAYER
                
                if self.grid[c][r] == 0:

                    color = self.record_in_grid(c,r)
                    
                    center = ((MARGIN + WIDTH) * c + MARGIN + PADDING,
                                (MARGIN + WIDTH) * r + MARGIN + PADDING)
                    self.add_gomoku_piece(center,color)
                    
                    # check win
                    if self.check_win([c,r],PLAYER):
                        self.show_winner()
                        self._playing = False
                        self.pieces = []

                        # Incomplete button functionalit for new_game
                        #pygame.draw.rect(self._display_surf, GREEN,(PADDING,GAME_WIDTH + 50,BOARD // 2 - PADDING,30))
                        #pygame.draw.rect(self._display_surf, RED,(PADDING + BOARD // 2 + PADDING,GAME_WIDTH + 50,BOARD//2 - PADDING,30))
                        

                    PLAYER = not PLAYER

    
    def on_loop(self):
        pass

    
    def on_render(self):

        #self.pieces = [] can't remove circles, I need work on it tomorrow
        for piece in self.pieces:
            pygame.draw.circle(self._display_surf, piece['color'],
                               piece['center'],
                               WIDTH // 2 - MARGIN,0)
        pygame.display.update()
        

    
    def on_cleanup(self):

        pygame.quit()

 
    def on_execute(self):
    	
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    def start(self):
        self.piece = []
        self._playing = True
        
    def give_up(self):
        pass
        
    def regret(self):
        pass
    def show_winner(self):
    	win = "Player 1 win" if PLAYER else "Player 2 win"
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        text = myfont.render(win, False, BLACK)
        textRect = text.get_rect()
        textRect.centerx = self._display_surf.get_rect().centerx
        textRect.centery = GAME_WIDTH 
        self._display_surf.blit(text, textRect)

    def gomoku_board_init(self):
    	# Draw background rect for game area
        pygame.draw.rect(self._display_surf, BACKGROUND,
                         [PADDING,
                          PADDING,
                          BOARD,
                          BOARD]) 

        # Draw the grid
        for row in range(14):
            for column in range(14):
                pygame.draw.rect(self._display_surf, YELLOW,
                                 [(MARGIN + WIDTH) * column + MARGIN + PADDING,
                                  (MARGIN + WIDTH) * row + MARGIN + PADDING,
                                  WIDTH,
                                  WIDTH])

        # Five mark points
        points = [(3,3),(11,3),(3,11),(11,11),(7,7)]
        for point in points:
            pygame.draw.rect(self._display_surf, BACKGROUND,
                            (PADDING + point[0] * (MARGIN + WIDTH) - DOT // 2,
                             PADDING + point[1] * (MARGIN + WIDTH) - DOT // 2,
                             DOT,
                             DOT),0)
        
    def record_in_grid(self,c,r):
    	if PLAYER:
            color = WHITE
            self.grid[c][r] = 1
        else:
            color = BLACK
            self.grid[c][r] = 2
        return color

    def add_gomoku_piece(self,center,color):
        p = {'center':center,'color':color}
        if p not in self.pieces:
            self.pieces.append(p)
    	

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
    theApp = Gomoku()
    theApp.on_execute()
