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


class START():
    def __init__(self) -> None:
        self.start_button_surf = pg.Surface((200, 75))
        self.end_button_surf = pg.Surface((200, 75))
        self.start_button_surf.fill(('green')), self.end_button_surf.fill(('red'))
        self.start_button = self.start_button_surf.get_rect(center=(362.5, 300))
        self.end_button = self.end_button_surf.get_rect(center=(362.5, 500))
        self.start_text = font.render("start", True, black)
        self.end_text = font.render("exit", True, white)
        self.welcome_text = font.render("Welcome To Blackjack!", True, white)

        self.starting = False
        self.exitting = False

    def run(self, surface):
        surface.blit(self.start_button_surf, self.start_button)
        surface.blit(self.end_button_surf, self.end_button)
        surface.blit(self.start_text, (327.5, 288.5))
        surface.blit(self.end_text, (337.5, 488.5))
        surface.blit(self.welcome_text, (SCREEN_WIDTH/2 - 160, 50))


class PLAYER(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.card_pos_x = SCREEN_WIDTH/2 - 132
        self.card_pos_y = SCREEN_HEIGHT + - 32.5

        self.group = pg.sprite.Group()
        self.value_lst = list()
        self.total = 0

        self.hit_button_surf = pg.Surface((75, 50))
        self.pass_button_surf = pg.Surface((75, 50))
        self.hit_button_surf.fill(('green')), self.pass_button_surf.fill(('red'))
        self.hit = self.hit_button_surf.get_rect(center=(550, 650))
        self.passes = self.pass_button_surf.get_rect(center=(150, 650))

        self.hit_text = font.render("hit", True, black)
        self.pass_text = font.render("pass", True, white)

        self.passed = False

    def create_card(self, side, player_team):
        self.card_pos_x += 50
        return CARD(random.choice(card_list), (self.card_pos_x, self.card_pos_y), side, player_team)

    def options(self, surface):
        surface.blit(self.hit_button_surf, self.hit)
        surface.blit(self.pass_button_surf, self.passes)
        surface.blit(self.hit_text, (532.5, 632.5))
        surface.blit(self.pass_text, (115, 632.5))