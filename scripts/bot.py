import random
import pygame

class Bot:
    def __init__(self, game):
        self.game = game
        if self.game.turn == 'yellow':
            self.turn = 'red'
        else:
            self.turn = 'yellow'
        self.drop_pos = None
        self.marker_line = []
        
        #starting offset will then be added with win condition to provide the rane for marker line
        self.OFFSETS = [(1, -1), (1, 0), (1, 1), (0, 1)]

    def drop(self):
        self.drop_pos = None
        self.marker_list = self.game.marker.marker_list
        
        #loop through markers and offsets
        for column in self.marker_list:
            for marker in column:
                for offset in self.OFFSETS:
                    Bot.make_marker_line(self, marker, offset)
                    
                    Bot.block(self)
                    if self.drop_pos:
                        break

                    Bot.attack(self)
                    if self.drop_pos:
                        break

            if self.drop_pos:
                break
        
        if not self.drop_pos:
            Bot.neutral(self)

        if not self.drop_pos:
            Bot.drop_rand(self)

        return self.drop_pos                                                                                                                               
    
    def drop_rand(self):
        self.drop_pos = random.randint(0, self.game.board_dimensions[0] - 1)
        while self.game.marker.collumn_full(self.drop_pos):
            self.drop_pos = random.randint(0, self.game.board_dimensions[0] - 1)

    def block(self):
        self.win_list = []

        for x in range(self.game.win_condition):
            for i in range(self.game.win_condition):
                self.win_list.append(self.marker_line[i+x])
            if sum(isinstance(n, dict) for n in self.win_list) == self.game.win_condition - 1:
                self.counter = 0
                for m in self.win_list:
                    if not m:
                        if self.counter == 0:
                            self.drop_pos = self.win_list[1]['pos'][1] - 1
                        else:
                            self.drop_pos = self.win_list[self.counter - 1]['pos'][1] + 1
                        print('yes')
                    self.counter += 1
                print(self.win_list)
            self.win_list = []

        for x in self.marker_list:
            self

    def attack(self):
        self.win_list = []

    def neutral(self):
        pass
 
    def make_marker_line(self, marker, offset):
        self.marker_line = []
        self.range_offset = self.game.win_condition - 1
        
        for x in range(self.game.win_condition * 2 - 1):
            x -= self.range_offset
            
            try:
                if marker['pos'][1] + offset[1] * x < 0 or marker['colour'] != self.turn:
                    self.marker_line.append([])
                else:
                    self.marker_line.append(self.marker_list[marker['pos'][0] + offset[0] * x][marker['pos'][1] + offset[1] * x])
            except IndexError:
                self.marker_line.append([])
    
    def dummy_yellow(self, pos):
        pass

    def dummy_red(self, pos):
        pass