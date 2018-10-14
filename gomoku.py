import pygame

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


class Gomoku(object):
    def __init__(self):
        self.grid = [[0 for x in range(15)] for y in range(15)]
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode(
            (GAME_WIDTH, GAME_HIGHT),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption('Gomoku')

        self.player = False
        self._running = True
        self._playing = False
        self._win = False
        self.lastPosition = [-1, -1]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            # does not update postion in python3.6, and I don't know why
            pos = pygame.mouse.get_pos()
            if self.mouse_in_botton(pos):
                if not self._playing:
                    self.start()
                    if self.player:
                        self.player = not self.player
                else:
                    self.surrender()
                    self.player = not self.player

            elif self._playing:
                r = (pos[0] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)
                c = (pos[1] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)

                if 0 <= r < 15 and 0 <= c < 15:
                    if self.grid[r][c] == 0:
                        self.lastPosition = [r, c]
                        self.grid[r][c] = 1 if self.player else 2
                        if self.player == 1:
                            pygame.mixer.Sound("Bb.wav").play()
                        else:
                            pygame.mixer.Sound("G.wav").play()

                        # check win
                        if self.check_win([r, c], self.player):
                            self._win = True
                            self._playing = False
                        else:
                            self.player = not self.player

    def on_render(self):
        self.render_gomoku_piece()
        self.render_last_position()
        self.render_game_info()
        self.render_button()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while self._running:
            self.gomoku_board_init()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        self.on_cleanup()

    def start(self):
        self._playing = True
        self.grid = [[0 for _ in range(15)] for _ in range(15)]
        self.lastPosition = [-1, -1]
        self._win = False

    def surrender(self):
        self._playing = False
        self._win = True

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

    def mouse_in_botton(self, pos):
        if GAME_WIDTH // 2 - 50 <= pos[0] <= GAME_WIDTH // 2 + 50 and GAME_HIGHT - 50 <= pos[1] <= GAME_HIGHT - 20:
            return True
        return False

    def render_button(self):
        color = GREEN if not self._playing else RED
        info = "Start" if not self._playing else "Surrender"

        pygame.draw.rect(self._display_surf, color,
                         (GAME_WIDTH // 2 - 50, GAME_HIGHT - 50, 100, 30))

        info_font = pygame.font.SysFont('Helvetica', 18)
        text = info_font.render(info, True, WHITE)
        textRect = text.get_rect()
        textRect.centerx = GAME_WIDTH // 2
        textRect.centery = GAME_HIGHT - 35
        self._display_surf.blit(text, textRect)

    def render_game_info(self):
        # current player color
        color = BLACK if not self.player else WHITE
        center = (GAME_WIDTH // 2 - 60, BOARD + 60)
        radius = 12
        pygame.draw.circle(self._display_surf, color, center, radius, 0)

        info = "You Win" if self._win else "Your Turn"
        info_font = pygame.font.SysFont('Helvetica', 24)
        text = info_font.render(info, True, BLACK)
        textRect = text.get_rect()
        textRect.centerx = self._display_surf.get_rect().centerx + 20
        textRect.centery = center[1]
        self._display_surf.blit(text, textRect)

    def render_gomoku_piece(self):
        for r in range(15):
            for c in range(15):
                center = ((MARGIN + WIDTH) * r + MARGIN + PADDING,
                          (MARGIN + WIDTH) * c + MARGIN + PADDING)
                if self.grid[r][c] > 0:

                    color = BLACK if self.grid[r][c] == 2 else WHITE
                    pygame.draw.circle(self._display_surf, color,
                                       center,
                                       WIDTH // 2 - MARGIN, 0)

    def render_last_position(self):
        if self.lastPosition[0] > 0 and self.lastPosition[1] > 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.lastPosition[0] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.lastPosition[1] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH),
                              (MARGIN + WIDTH)), 1)

    def check_win(self, position, player):
        target = 1 if player else 2
        if self.grid[position[0]][position[1]] != target:
            return False
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
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

    def __call__(self):
        self.on_execute()

if __name__ == "__main__":
    gomoku = Gomoku()
    gomoku()
