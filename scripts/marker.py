import pygame
import subprocess

class Marker():
    def __init__(self, game) -> None:
        self.OFFSETS = [(0, 1), (1, 0), (1, 1), (1, -1)]
        self.game = game
        self.dimensions = self.game.board_dimensions
        self.marker_list = [[] for x in range(self.game.board_dimensions[0])]
        self.render_list = self.marker_list
        self.full_surf = pygame.Surface((self.dimensions[0]*self.game.tile_size, self.dimensions[1]*self.game.tile_size), pygame.SRCALPHA).convert_alpha()

    def update(self):
        self.full_surf.fill((0, 0, 0, 0))
        for outer in self.marker_list:
            for inner in outer:
                if inner:
                    self.full_surf.blit(self.game.assets[inner['colour'] + '_marker'], pygame.math.Vector2(inner['pos'][0], self.dimensions[1] - inner['pos'][1] - 1) * self.game.tile_size)


    def collumn_full(self, collumn):
        if len(self.marker_list[collumn]) == self.dimensions[1]:
            return True
        return False
    
    def stalemate(self):
        self.slots_filled = 0
        for outer in self.marker_list:
            self.slots_filled += len(outer)
        if self.slots_filled == self.dimensions[0] * self.dimensions[1]:
            return True
        return False
    
    def win(self, player_turn, win_condition=4):
        if player_turn == 'yellow':
            player_turn = 'red'
        else:
            player_turn = 'yellow'
        
        self.marker_line = []
        for column in self.marker_list:
            for marker in column:
                for offset in self.OFFSETS:
                    for x in range(win_condition):
                        try:
                            if marker['pos'][1] + offset[1] * x < 0:
                                break
                            self.marker_line.append(self.marker_list[marker['pos'][0] + offset[0] * x][marker['pos'][1] + offset[1] * x])
                        except IndexError:
                            break
                    if len(self.marker_line) == win_condition and all(x['colour'] == player_turn for x in self.marker_line):
                        return True
                    
                    self.marker_line = []
        #print(f'{self.marker_list}\n')
        return False

                        

class Yellow_Marker():
    marker_colour = 'yellow'

    def __init__(self, Marker, collumn, colour='yellow'):
        self.game = Marker.game
        self.Marker = Marker
        self.grid_pos = (collumn, len(self.Marker.marker_list[collumn]))
        self.Marker.marker_list[collumn].append({'colour': colour, 'pos': self.grid_pos})
        self.tile_size = self.game.tile_size
        self.pos = pygame.math.Vector2(self.grid_pos[0] * self.tile_size, 0)
        self.velocity = 0
        self.falling = True
        self.img = self.game.assets[colour + '_marker']

    def update(self):
        self.pos.y += self.velocity

        self.velocity = min(17, self.velocity + 0.5)

        if self.pos.y > (self.game.board_dimensions[1] - self.grid_pos[1] + self.game.marker_drop - 1) * self.game.tile_size:
            self.game.assets['plastic_sfx'].play()
            self.falling = False

class Red_Marker(Yellow_Marker):
  
    def __init__(self, Marker, collumn):
        super().__init__(Marker, collumn, 'red')
    
    marker_colour = 'red'