import pygame as pg
from pygame.locals import *
from pygame import mixer
from sys import exit
import random
from card_dict import card_dict

#setup
mixer.pre_init(44100, -16, 2, 2048)
pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
caption = pg.display.set_caption("blackjack")
frames = pg.time.Clock()
fps = 240
font = pg.font.SysFont("Verdana", 30)
small_font = pg.font.SysFont("Verdana", 15)

bg_music = mixer.music.load("music/Monkeys-Spinning-Monkeys.mp3")
mixer.music.play(-1)

#colors
black = (0, 0, 0)
white = (255, 255, 255)
player_deck_color = (40, 150, 60)
dealer_deck_color = (20, 90, 180)

cards = open('cards.txt')
card_list = list()
for line in cards:
    if line.startswith('graphics'):
        card_list.append(line.strip())
