import pygame
import os

BASE_IMG_PATH = 'assets/images/'
BASE_SOUND_PATH = 'assets/audio/'

def load_image(path, color_key=(0, 0, 0), alpha=False):
    if alpha:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    else:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey((color_key))
    return img

def load_images(path, color_key=(255, 255, 255)):
    images = {}
    for img_name in os.listdir(BASE_IMG_PATH + path):
        loc_name = img_name.split('.')[0]
        images[loc_name] = load_image(path + '/' + img_name, color_key, True)    
    return images

def load_sound(path, volume=0.5):
    sound = pygame.mixer.Sound(BASE_SOUND_PATH + path)
    sound.set_volume(volume)
    return sound
    
def parallax(pos, center, parallax):
    return pygame.math.Vector2(pos) + pygame.math.Vector2(pygame.mouse.get_pos() - center) / parallax