import sys
import pygame
from scripts.entities import Basic_Surf, Text
from scripts.utils import load_image, load_images, load_sound
from scripts.board import Board_Tilemap
from scripts.marker import Marker, Yellow_Marker, Red_Marker
from scripts.bot import Bot

win_screen_size = pygame.Vector2(1000, 800)*0.8
dis_screen_size = (1000, 800)
tile_size = 80
marker_drop = 1.5
board_dimensions = (7, 6)
win_name = 'Connect 4'
win_condition = 4

class Game:
    # init pygame and 'Game' variables
    def __init__(self, win_screen_size=(1000, 800), dis_screen_size=(1000, 800), win_name='Connect 4', tile_size=80, board_dimensions=(7, 6), marker_drop=1.5, win_condition=4):        
        pygame.init()
        
        self.win_screen_size = win_screen_size
        self.dis_screen_size = dis_screen_size
        self.tile_size = tile_size
        self.marker_drop = marker_drop
        self.board_dimensions = board_dimensions
        self.win_name = win_name
        self.win_condition = win_condition

        pygame.display.set_caption(win_name)
        #Window Screen
        self.screen = pygame.display.set_mode(win_screen_size)
        
        #Surface for game
        self.display = pygame.Surface(dis_screen_size)
        self.center = pygame.math.Vector2((dis_screen_size[0] / 2, dis_screen_size[1] / 2))

        self.clock = pygame.time.Clock()

        self.assets = {
            'background': load_image('background/background.png'),
            'yellow_marker': pygame.transform.scale(load_image('marker/yellow_marker.png', (0, 0, 0), True), (tile_size, tile_size)),
            'red_marker': pygame.transform.scale(load_image('marker/red_marker.png', (0, 0, 0), True), (tile_size, tile_size)),
            'table': load_image('background/table.svg', (0, 0, 0)),
            'red_cursor': load_image('cursor/red_cursor.png'),
            'yellow_cursor': load_image('cursor/yellow_cursor.png'),
            'tiles' : load_images('board'),
            'plastic_sfx': load_sound('plastic_sfx.wav', 0.3),
            'explosion': load_sound('explosion.mp3', 1),
            'stalemate': load_image('texts/stalemate.png', (0, 0, 0), True),
            'yellow_wins': load_image('texts/yellow_wins.png', (0, 0, 0), True),
            'red_wins': load_image('texts/red_wins.png', (0, 0, 0), True)
        }
        pygame.mixer.music.load('assets/audio/background_music.mp3')
        pygame.mixer.music.set_volume(0.8)

        #Smaller the #, the bigger the parallax
        self.parallax = {
            'background': 200,
            'table': 70,
            'game': 30
        }

        self.turn = 'yellow'
        self.wait = False
        self.mouse_down = False
        self.player = None
        self.switch = False
        
        #entities
        self.marker = Marker(self)
        self.board = Board_Tilemap(self, tile_size, board_dimensions, marker_drop)
        self.table = Basic_Surf(self, self.assets['table'], 'table', 1.1, (0, 420))
        self.background = Basic_Surf(self, self.assets['background'], 'background')
        self.bot = Bot(self)



    def run(self):
        #Hides mouse cursor
        pygame.mouse.set_visible(False)
        pygame.mixer.music.play(-1)

        while True:           
            
            #dummy marker and updating marker grid
            if not self.wait:
                if self.switch:
                    self.switch = False
                    if self.marker.win(self.turn, self.win_condition):
                        if self.turn == 'red':
                            Game.wins(self, 'yellow')
                        else:
                            Game.wins(self, 'red')
                    if self.marker.stalemate():
                        Game.stalemate(self)
                self.board.pre_drop(self.turn)
            
            #checking for user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP and self.mouse_down:
                    if not self.marker.collumn_full(self.board.dummy_marker_col) and self.player == None and not self.wait:
                        self.player = eval(self.turn.capitalize() + '_Marker')(self.marker, self.board.dummy_marker_col)
                        self.wait = True    
                        
                    self.mouse_down = False

            #updates and renders
            self.background.render()
            self.table.render()
            if self.player:
                self.player.update()
                if not self.player.falling:
                    self.wait = False
                    self.player = None
                    self.marker.update()
                    if self.turn == 'yellow':
                        self.turn = 'red'
                    else:
                        self.turn = 'yellow'
                    self.switch = True

            self.board.render(self.marker, self.player)

            #display surface to window screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            if pygame.mouse.get_focused():
                self.screen.blit(self.assets[self.turn + '_cursor'], pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(60)

    def stalemate(self, with_bot = False):
        pygame.mouse.set_visible(True)

        self.text = Text(self.dis_screen_size, self.assets['stalemate'], self.center, 2/3)

        pygame.mixer.music.fadeout(1000)
        self.assets['explosion'].play()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP and self.mouse_down:
                    if self.text.rect.collidepoint(pygame.mouse.get_pos()):
                        Game.restart(self, with_bot)

            self.board.pre_drop(self.turn)
            self.background.render()
            self.table.render()
            self.board.render(self.marker)
            
            #transparent rectangle          
            self.text.update(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    
    def wins(self, colour, with_bot = False):
        pygame.mouse.set_visible(True)

        self.text = Text(self.dis_screen_size, self.assets[colour + '_wins'], self.center, 2/3)

        pygame.mixer.music.fadeout(1000)
        self.assets['explosion'].play()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP and self.mouse_down:
                    if self.text.rect.collidepoint(pygame.mouse.get_pos()):
                        Game.restart(self, with_bot)
                

            self.board.pre_drop(self.turn)
            self.background.render()
            self.table.render()
            self.board.render(self.marker)
            
            #transparent rectangle          
            self.text.update(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
    
    def restart(self, with_bot=False):
        self.turn = 'yellow'
        self.wait = False
        self.mouse_down = False
        self.player = None
        self.switch = False
        
        #entities
        self.marker = Marker(self)
        self.board = Board_Tilemap(self, tile_size, board_dimensions, marker_drop)
        self.table = Basic_Surf(self, self.assets['table'], 'table', 1.1, (0, 420))
        self.background = Basic_Surf(self, self.assets['background'], 'background')
        if with_bot:
            Game.run_bot(self)
        else:
            Game.run(self)

    def run_bot(self):
        #Hides mouse cursor
        pygame.mouse.set_visible(False)
        pygame.mixer.music.play(-1)

        while True:           
            
            #dummy marker and updating marker grid
            if not self.wait:
                if self.switch:
                    self.switch = False
                    if self.marker.win(self.turn, self.win_condition):
                        if self.turn == 'red':
                            Game.wins(self, 'yellow', True)
                        else:
                            Game.wins(self, 'red', True)
                    if self.marker.stalemate():
                        Game.stalemate(self, True)
                self.board.pre_drop(self.turn)

            if self.turn == self.bot.turn and not self.wait:
                self.player = eval(self.bot.turn.capitalize() + '_Marker')(self.marker, self.bot.drop())
                self.wait = True
            
            #checking for user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP and self.mouse_down:
                    if not self.marker.collumn_full(self.board.dummy_marker_col) and self.player == None and not self.wait:
                        self.player = eval(self.turn.capitalize() + '_Marker')(self.marker, self.board.dummy_marker_col)
                        self.wait = True
                        
                    self.mouse_down = False

            #updates and renders
            self.background.render()
            self.table.render()
            if self.player:
                self.player.update()
                if not self.player.falling:
                    self.wait = False
                    self.player = None
                    self.marker.update()
                    if self.turn == 'yellow':
                        self.turn = 'red'
                    else:
                        self.turn = 'yellow'
                    self.switch = True

            self.board.render(self.marker, self.player)

            #display surface to window screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            if pygame.mouse.get_focused():
                self.screen.blit(self.assets[self.turn + '_cursor'], pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    Game(win_screen_size, dis_screen_size, win_name, tile_size, board_dimensions, marker_drop, win_condition).run()