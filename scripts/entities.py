import pygame
from math import sin
from scripts.utils import parallax

class Basic_Surf:
    def __init__(self, game, img, img_name, scale_by=1, offset=0):
        self.img = pygame.transform.scale_by(img, scale_by)
        self.pos = pygame.math.Vector2(game.display.get_width()/2 - self.img.get_width()/2, game.display.get_height()/2 - self.img.get_height()/2) + pygame.math.Vector2(offset)
        self.game = game
        self.img_name = img_name
        self.render_pos = parallax(self.pos, self.game.center, self.game.parallax[self.img_name])

    def render(self):
        
        self.render_pos = parallax(self.pos, self.game.center, self.game.parallax[self.img_name])
        
        self.game.display.blit(self.img, self.render_pos)


class Text:
    def __init__(self, screen_size, img, centre, scale_to_screen=2/3) -> None:
        self.scale_to_screen = scale_to_screen


        #Creating transparent grey surface
        self.grey_rect = pygame.Surface((screen_size), pygame.SRCALPHA)
        pygame.draw.rect(self.grey_rect, (128, 128, 128), ((0, 0), screen_size))
        self.alpha_surface = pygame.Surface(self.grey_rect.get_size(), pygame.SRCALPHA)
        self.alpha_surface.fill((255, 255, 255, 225))
        self.grey_rect.blit(self.alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.original_img = img
        self.img =  pygame.transform.scale_by(img, Text.img_scale(self, self.scale_to_screen))
        self.pos = pygame.math.Vector2(centre) - (pygame.math.Vector2(self.img.get_size()) / 2)
        self.render_pos = self.pos
        self.render_image = self.img
        self.centre = centre
        self.rect = pygame.Rect(self.render_pos[0], self.render_pos[1], self.img.get_width(), self.img.get_height())
        self.counter = 0

    def update(self, surf):
        self.counter += 1
        
        self.size = self.render_image.get_width() / self.img.get_width()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.render_image = pygame.transform.scale_by(self.original_img, Text.img_scale(self, self.scale_to_screen)*(4 - self.size)/2)
        else:
            self.render_image = pygame.transform.scale_by(self.original_img, Text.img_scale(self, self.scale_to_screen)*(3 - self.size)/2)

        self.render_pos = pygame.math.Vector2(self.centre) - (pygame.math.Vector2(self.render_image.get_size()) / 2)
        self.render_pos.y = sin(self.counter/25)*self.img.get_height()/4 + self.render_pos.y
        
        self.rect = pygame.Rect(self.render_pos[0], self.render_pos[1], self.render_image.get_width(), self.render_image.get_height())

        surf.blit(self.grey_rect, (0, 0))
        surf.blit(self.render_image, self.render_pos)

    def img_scale(self, scale_to_screen):
        return (scale_to_screen * self.grey_rect.get_width()) / self.original_img.get_width()