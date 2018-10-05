# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import argparse
import re
from random import choice
import time
from simpleclient import GomokuClientThread, ClientCommand

# STILL BLOCKING

# Define some colors
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
RED = (133, 42, 44)
YELLOW = (208, 176, 144)
GREEN = (26, 81, 79)

# Define grid globals
WIDTH = 20
MARGIN = 1
PADDING = 20
DOT = 4
BOARD = (WIDTH + MARGIN) * 14 + MARGIN
GAME_WIDTH = BOARD + PADDING * 2
GAME_HIGHT = GAME_WIDTH + 100

# when to update
class Gomoku(object):
    def __init__(self, player, server_addr, board_row=15, board_column=15):
        pygame.init()
        pygame.font.init()
        pygame.time.set_timer(USEREVENT+1, 10000)# every 10 seconds
        
        self._display_surf = pygame.display.set_mode(
            (GAME_WIDTH, GAME_HIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption('Gomoku')

        self.grid = None
        self.client_thread = None

        self.server_addr = server_addr
        self.last_player = -1
        self.player = player
        self._running = True
        self.winner = -1
        self.board_row = board_row
        self.board_column = board_column
        self.lastPosition = [-1, -1]

    def on_execute(self):
        self.client_thread = GomokuClientThread()
        self.client_thread.start()
        self.client_thread.cmd_q.put(ClientCommand(ClientCommand.CONNECT, self.server_addr))
        
        while self._running:
            data = self.client_thread.reply_q.get(True)
            print(data)
            if data:
                self.last_player = data["player"]
                self.grid = self.grid_str_2_matrix(data["grid"])
                self.lastPosition = [data["x"], data["y"]]
                self.gomoku_board_init()
                
                if data["gameover"] == -1:
                    if data["next_player"] != self.player:
                        self.client_thread.cmd_q.put(ClientCommand(ClientCommand.SEND, {"wait": True}))
                        print("waiting")
                    else:
                        for event in pygame.event.get():
                            self.on_event(event)
                        x, y = self.random_position()
                        self.grid[x][y] = self.player
                        data = {"grid":self.grid, "x":x, "y":y, "player":self.player}
                        self.client_thread.cmd_q.put(ClientCommand(ClientCommand.SEND, data))
                        print("new move")
                else:
                    print("game over")
                    self._running = False
                    if data["gameover"] == 0:
                        self.winner = 0
                    else:
                        self.winner = data["player"]
                    self.client_thread.cmd_q.put(ClientCommand(ClientCommand.CLOSE))
                    break
            self.on_render()
            time.sleep(5)
            
              
        self.on_cleanup()

    def random_position(self):
        print(self.grid)
        n = len(self.grid)
        m = len(self.grid[0])
        return choice([[i, j] for i in range(n) for j in range(m) if self.grid[i][j] == 0])


    def update(self, message):
        self._playing = True
        self.grid = message["grid"]
        self.lastPosition = [message["x"], message["y"]]
        self.last_player = message["player"]
        if self.last_player == self.player or (self.last_player == -1 and self.player == 2):
            self._playing = False
        self.winner = message["winner"]
        if self.winner >= 0:
            self._playing = False
    

    def on_event(self, event):
        print(event.type == pygame.MOUSEBUTTONUP)
        if event.type == pygame.QUIT:
            self.close_connection()
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            r = (pos[0] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)
            c = (pos[1] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)
            print(r, c)
            if 0 <= r < self.board_row and 0 <= c < self.board_column and self.grid[r][c] == 0:
                self.grid[r][c] = self.player
                data = {"grid":self.grid, "x":r, "y":c, "player":self.player}
                self.client_thread.cmd_q.put(ClientCommand(ClientCommand.SEND, data))



    def on_render(self):
        print("rending...")
        self.render_gomoku_piece()
        self.render_last_position()
        self.render_game_info()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
            

    def grid_str_2_matrix(self, grid):
        return [list(map(int, grid[i:i+self.board_column])) for i in range(0, len(grid), self.board_column)]

    
    def gomoku_board_init(self):
        self._display_surf.fill(YELLOW)
        # Draw background rect for game area
        pygame.draw.rect(self._display_surf, BLACK,
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

        # Five dots
        points = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for point in points:
            pygame.draw.rect(self._display_surf,
                            BLACK,
                            (PADDING + point[0] * (MARGIN + WIDTH) - DOT // 2,
                            PADDING + point[1] * (MARGIN + WIDTH) - DOT // 2,
                            DOT,
                            DOT), 0)

    def render_game_info(self):
        color = BLACK if not self.last_player == 1 else WHITE
        center = (GAME_WIDTH // 2 - 60, BOARD + 60)
        radius = 12
        pygame.draw.circle(self._display_surf, color, center, radius, 0)

        info = "Your Turn"

        if self.winner > 0:
            color = WHITE if self.last_player == 1 else BLACK
            info = "You Win"
        elif self.winner == 0:
            info = "Draw"
            color = YELLOW
        info_font = pygame.font.SysFont('Helvetica', 24)
        text = info_font.render(info, True, BLACK)
        textRect = text.get_rect()
        textRect.centerx = self._display_surf.get_rect().centerx + 20
        textRect.centery = center[1]
        self._display_surf.blit(text, textRect)
        print("Finish render 3/3")

    def render_gomoku_piece(self):
        for r in range(self.board_row):
            for c in range(self.board_column):
                center = ((MARGIN + WIDTH) * r + MARGIN + PADDING,
                          (MARGIN + WIDTH) * c + MARGIN + PADDING)
                if self.grid[r][c] > 0:

                    color = BLACK if self.grid[r][c] == 2 else WHITE
                    pygame.draw.circle(self._display_surf, color,
                                       center,
                                       WIDTH // 2 - MARGIN, 0)
        print("Finish render 1/3")

    def render_last_position(self):
        if self.lastPosition[0] > 0 and self.lastPosition[1] > 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.lastPosition[0] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.lastPosition[1] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH),
                              (MARGIN + WIDTH)), 1)
        print("Finish render 2/3")

    def __call__(self):
        self.on_execute()

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]',
                                     description='Gomoku socket client @Ludisposed & @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python gomoku_game.py -i 'localhost' -p 9999 -e 2
'''
                                        )
    parser.add_argument('-i','--ip', type=str, default="localhost", help='server host')
    parser.add_argument('-p','--port', type=int, default=9999, help='server port')
    parser.add_argument('-e','--player', type=int, default=1, help='player')
    args = parser.parse_args()

    ip_pattern = "((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?<!\.)|\.)){4}"
    ip = re.match(ip_pattern, args.ip)
    valid_ip = (ip and ip.group(0) == args.ip)

    if not (args.ip == "localhost" or valid_ip):
        print("[-] IPV4 host is not valid")
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = parse_options()
    game = Gomoku(args.player, (args.ip, args.port))
    game()


for event in pygame.event.get():
    self.on_event(event)
x, y = self.random_position()
self.grid[x][y] = self.player
data = {"grid":self.grid, "x":x, "y":y, "player":self.player}
self.client_thread.cmd_q.put(ClientCommand(ClientCommand.SEND, data))