import pygame
from scripts.entities import Basic_Surf
from math import floor, ceil


class Board_Tilemap:
    def __init__(self, game, tile_size=80, dimensions= (7, 6), marker_drop=1.5):
        self.game = game
        self.marker_drop = marker_drop
        self.tile_size = tile_size
        self.board_map = {}
        self.dimensions = dimensions
        self.full_surf = pygame.Surface((self.dimensions[0]*self.tile_size, self.dimensions[1]*self.tile_size + self.marker_drop*self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.board_surf =  pygame.Surface((self.dimensions[0]*self.tile_size, self.dimensions[1]*self.tile_size), pygame.SRCALPHA).convert_alpha()
        self.dummy_marker = self.game.assets[self.game.turn + '_marker']
        self.dummy_marker_col = 0
        self.dummy_marker_x = 0

        #Setting tilemap
        #First Row
        self.board_map['0;0'] = {'type': 'top_left', 'pos': (0, 0)}
        for inner in range(self.dimensions[0] - 2):
            self.board_map[str(inner + 1) + ';0'] = {'type': 'top', 'pos': (inner + 1, 0)}
        self.board_map[str(self.dimensions[0] - 1) + ';0'] = {'type': 'top_right', 'pos': (self.dimensions[0] - 1, 0)}

        #Middle 4 rows
        for outer in range(self.dimensions[1] - 2):
            self.board_map['0;' + str(outer + 1)] = {'type': 'left', 'pos': (0, outer + 1)}
            for inner in range(self.dimensions[0] - 2):
                self.board_map[str(inner + 1) + ';' + str(outer + 1)] = {'type': 'middle', 'pos': (inner + 1, outer + 1)}
            self.board_map[str(self.dimensions[0] - 1) + ';' + str(outer + 1)] = {'type': 'right', 'pos': (self.dimensions[0] - 1, outer + 1)}

        #Last Row
        self.board_map['0;' + str(self.dimensions[1] - 1)] = {'type': 'bottom_left', 'pos': (0, self.dimensions[1] - 1)}
        for inner in range(self.dimensions[0] - 2):
            self.board_map[str(inner + 1) + ';' + str(self.dimensions[1] - 1)] = {'type': 'bottom', 'pos': (inner + 1, self.dimensions[1] - 1)}
        self.board_map[str(self.dimensions[0] - 1) + ';' + str(self.dimensions[1] - 1)] = {'type': 'bottom_right', 'pos': (self.dimensions[0] - 1, self.dimensions[1] - 1)}

        for loc in self.board_map:
            tile = self.board_map[loc]
            tile['pos'] = pygame.math.Vector2(tile['pos'])
            self.board_surf.blit(pygame.transform.scale(self.game.assets['tiles'][tile['type']], (self.tile_size, self.tile_size)), tile['pos']*self.tile_size)
    def render(self, marker, player_marker=False):
        #clear screen
        self.full_surf.fill((0, 0, 0, 0))

        #rendering markers
        self.full_surf.blit(marker.full_surf, (0, self.marker_drop*self.tile_size))
        if player_marker:
            self.full_surf.blit(player_marker.img, player_marker.pos)

        #rendering board
        self.full_surf.blit(self.board_surf, (0, self.marker_drop*self.tile_size))
        if not self.game.wait:
            self.full_surf.blit(self.dummy_marker, (self.dummy_marker_x, 0))
        Basic_Surf(self.game, self.full_surf, 'game').render()

    def pre_drop(self, colour):
        self.m_pos = pygame.mouse.get_pos()[0]
        self.render_pos = Basic_Surf(self.game, self.full_surf, 'game').render_pos[0]
        self.dummy_marker = self.game.assets[colour + '_marker']
        
        #raw x
        self.dummy_marker_x = min(self.m_pos - self.render_pos, self.full_surf.get_width() - self.tile_size)
        print(self.m_pos - self.render_pos)
        self.dummy_marker_x = max(self.dummy_marker_x, 0)
        
        #grid x
        self.dummy_marker_col = floor(self.dummy_marker_x / self.tile_size)

        #clipped x
        self.dummy_marker_x = self.dummy_marker_col * self.tile_size