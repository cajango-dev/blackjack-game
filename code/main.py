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
        
class DEALER(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.card_pos_x = SCREEN_WIDTH/2 - 132
        self.card_pos_y = SCREEN_HEIGHT/2 + 37.5

        self.group = pg.sprite.Group()
        self.value_lst = list()
        self.dict = dict()
        self.total = 0
        self.over_17 = False

    def create_card(self, side, player_team):
        self.card_pos_x += 50
        return CARD(random.choice(card_list), (self.card_pos_x, self.card_pos_y), side, player_team)


class CARD(pg.sprite.Sprite):
    def __init__(self, rand_card, pos, side, player_team) -> None:
        super().__init__()
        self.rand_card = rand_card
        self.image = pg.image.load(rand_card).convert_alpha()
        self.surf = pg.Surface((50, 70))
        self.rect = self.surf.get_rect(center=pos)
        self.back = pg.image.load("graphics/card_extras/card_back.png").convert_alpha()
        self.upside = side

        for k, v in card_dict.items():
            for card in k:
                if self.rand_card == card:
                    if isinstance(v, int):
                        self.card_value = v
                    elif isinstance(v, list):
                        if player_team:
                            self.ace_value()
                            self.card_value = v[int(input("0 or 1: ")) % 2]
                        else:
                            self.card_value = v[0]

    def draw(self):
        if self.upside is True:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.back, self.rect)

    def ace_value(self):
        pass


class MAIN():
    def __init__(self) -> None:
        self.start = START()

        self.player = PLAYER()
        self.dealer = DEALER()

        self.dealer.group.add(self.dealer.create_card(True, False))
        self.dealer.group.add(self.dealer.create_card(False, False))

        self.player.group.add(self.player.create_card(True, True))
        self.player.group.add(self.player.create_card(True, True))

        for card in self.dealer.group:
            self.dealer.value_lst.append(card.card_value)

        for card in self.player.group:
            self.player.value_lst.append(card.card_value)

        self.turn = ''
        self.turn_num = 0
        self.turn_done = True
        self.end_game = False

    def run(self):
        self.draw_elements()
        self.update_elements()

    def draw_elements(self):
        if self.turn == '':
            self.player.options(screen)

        self.decks(screen)
        for card in self.dealer.group:
            card.draw()

        for card in self.player.group:
            card.draw()

        self.draw_amounts(screen)
        self.turn_draw(screen)

        if self.turn == 'dealer':
            self.player.options(screen)

        if self.player.total < 12:
            self.card_recommend_text = small_font.render("number " + str(len(self.player.group) + 1) + " card recommended", True, white)
            screen.blit(self.card_recommend_text, (SCREEN_WIDTH/3, 600))

    def update_elements(self):
        self.dealer.total = sum(self.dealer.value_lst)
        self.player.total = sum(self.player.value_lst)
        self.num_checks()
        global mouse

        if self.turn_done is False and self.end_game is False:
            if self.turn == 'dealer':
                if self.player.passed:
                    self.upside()
                if self.dealer.total < 17 and len(self.dealer.group) < 4:
                    self.dealer.value_lst = []
                    self.dealer.group.add(self.dealer.create_card(True, False))
                    for card in self.dealer.group:
                        self.dealer.value_lst.append(card.card_value)
                if self.dealer.total > 16:
                    self.dealer.over_17 = True
                else:
                    self.dealer.over_17 = False
                if self.player.total < 12:
                    print("number " + str(len(self.player.group) + 1) + " card recommended")
                if len(self.dealer.group) == 4:
                    if self.dealer.total < 17:
                        self.dealer.over_17 = True

            elif self.turn == 'player':
                if self.player.passed is False:
                    if len(self.player.group) < 4 and self.player.total < 21:
                        if mouse[0] > 400:
                            self.player.group.add(
                                self.player.create_card(True, True))
                            self.player.value_lst = []
                            for card in self.player.group:
                                self.player.value_lst.append(card.card_value)
                        else:
                            self.player.passed = True

                if self.player.passed or len(self.player.group) == 4:
                    self.upside()
                    if self.dealer.total >= self.player.total:
                        if len(self.player.group) < 4 and self.player.total < 21:
                            if mouse[0] > 400:
                                self.player.group.add(self.player.create_card(True, True))
                                self.player.value_lst = []
                                for card in self.player.group:
                                    self.player.value_lst.append(card.card_value)

            if self.dealer.over_17 and self.player.total < self.dealer.total:
                if len(self.player.group) < 4 and self.player.total <= 21:
                    if mouse[0] < 400:
                        self.player.group.add(self.player.create_card(True, True))
                        self.player.value_lst = []
                        for card in self.player.group:
                            self.player.value_lst.append(card.card_value)

        self.turn_done = True

    def num_checks(self):
        if len(self.turn) > 1:
            if self.dealer.total >= 22:
                self.bust(screen, "DEALER")
            elif self.player.total >= 22:
                self.bust(screen, "PLAYER")
            elif self.dealer.total == 21 and self.player.total == 21:
                self.tie(screen)
            elif self.dealer.total == 21:
                self.wins(screen, "DEALER")
            elif self.player.total == 21:
                self.wins(screen, "PLAYER")
            elif self.dealer.over_17 and self.player.total > self.dealer.total:
                self.wins(screen, "PLAYER")
            elif self.dealer.over_17 and self.player.total == self.dealer.total:
                self.tie(screen)

    def upside(self):
        for card in self.dealer.group:
            card.upside = True

    def tie(self, surface):
        self.upside()
        self.tie_text = font.render("Tie", True, white)
        surface.blit(self.tie_text, (SCREEN_WIDTH/2.1, 100))
        self.end_game = True

    def bust(self, surface, busted):
        self.upside()
        self.busted_text = font.render(busted + " BUST", True, white)
        surface.blit(self.busted_text, (SCREEN_WIDTH/2.75, 50))
        self.end_game = True

    def wins(self, surface, winner):
        self.upside()
        self.won_text = font.render(winner + " WON", True, white)
        surface.blit(self.won_text, (SCREEN_WIDTH/2.75, 50))
        self.end_game = True

    def decks(self, surface):
        pg.draw.rect(surface, player_deck_color, (SCREEN_WIDTH /2 - 100, SCREEN_HEIGHT - 70, 200, 67.5), 4)
        pg.draw.rect(surface, dealer_deck_color, (SCREEN_WIDTH /2 - 100, SCREEN_HEIGHT/2, 200, 67.5), 4)

    def turn_draw(self, surface):
        if self.end_game == False:
            self.turn_display = font.render(self.turn, True, white)
            surface.blit(self.turn_display, (SCREEN_WIDTH/2.3, 0))

            self.turns_render = font.render(str(self.turn_num), True, white)
            if len(str(self.turn_num)) == 1:
                surface.blit(self.turns_render, (SCREEN_WIDTH - 20, 0))
            elif len(str(self.turn_num)) == 2:
                surface.blit(self.turns_render, (SCREEN_WIDTH - 40, 0))

    def draw_amounts(self, surface):
        if self.player.passed is False and self.end_game is False:
            if len(self.dealer.value_lst) == 2:
                self.dealer_amount = font.render(
                    str(self.dealer.value_lst[0]), True, white)
            elif len(self.dealer.value_lst) > 2:
                self.dealer_amount = font.render(
                    str(self.dealer.value_lst[0] + self.dealer.value_lst[2]), True, white)
        else:
            self.dealer_amount = font.render(str(self.dealer.total), True, white)

        if len(str(self.dealer.total)) == 2:
            surface.blit(self.dealer_amount, (SCREEN_WIDTH/2.1, 250))
        else:
            surface.blit(self.dealer_amount, (SCREEN_WIDTH/2.05, 250))

        self.player_amount = font.render(str(self.player.total), True, white)
        if len(str(self.player.total)) == 2:
            surface.blit(self.player_amount, (SCREEN_WIDTH/2.1, 550))
        else:
            surface.blit(self.player_amount, (SCREEN_WIDTH/2.05, 550))


def end_program():
    pg.quit()
    exit()

def is_even(num):
    if num % 2 == 0:
        main.turn = 'dealer'
    elif num == 0:
        main.turn = 'player'
    else:
        main.turn = 'player'

main = MAIN()

if __name__ == "__main__":
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end_program()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    end_program()

            if event.type == pg.MOUSEBUTTONDOWN:
                if main.turn_done and main.start.starting:
                    #time.sleep(.2)
                    if main.end_game is False:
                        main.turn_num += 1
                        main.turn_done = False
                        is_even(main.turn_num)
                elif main.start.starting is False:
                    #more accurate to buttons
                    if mouse[1] < 400:
                        main.start.starting = True
                    elif mouse[1] > 400:
                        end_program()

            if main.end_game is False:
                if main.turn == 'player':
                    pg.mouse.set_visible(False)
                elif main.turn == 'dealer':
                    pg.mouse.set_visible(True)
            else:
                pg.mouse.set_visible(True)

        screen.fill(black)
        mouse = pg.mouse.get_pos()

        if main.start.starting:
            main.run()
        elif main.start.exitting:
            end_program()
        elif main.start.starting is False:
            main.start.run(screen)

        frames.tick(fps)
        pg.display.update()