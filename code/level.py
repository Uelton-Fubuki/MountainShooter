#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.Const import COLOR_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAM_TIME
from code.EntityMediator import EntityMediator
from code.entity import Entity
from code.entityFactory import EntityFactory


class Level:
    def __init__(self, window, name, game_mode):
        self.timeout = 20000  # 20 segundos
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Carrega o cenário e jogadores
        bg_entities = EntityFactory.get_entity('Level1Bg')
        if bg_entities:
            self.entity_list.extend(bg_entities)

        player1 = EntityFactory.get_entity('Player1')
        if player1:
            self.entity_list.append(player1)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player2 = EntityFactory.get_entity('Player2')
            if player2:
                self.entity_list.append(player2)

        pygame.time.set_timer(EVENT_ENEMY, SPAM_TIME)

    def run(self):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            # 1. Desenha e move as entidades (com proteção contra None)
            for ent in self.entity_list:
                if ent is not None:
                    self.window.blit(source=ent.surf, dest=ent.rect)
                    ent.move()
                else:
                    print("Atenção: Existe um elemento None na entity_list!")

            # 2. Captura de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    # CORRIGIDO: 'choice' sem aspas para passar a variável
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    enemy = EntityFactory.get_entity(choice)
                    if enemy:
                        self.entity_list.append(enemy)

            # 3. Desenha os textos na tela
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', COLOR_WHITE, (10, 5))
            self.level_text(14, f'FPS: {clock.get_fps():.0f}', COLOR_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'ENTIDADES: {len(self.entity_list)}', COLOR_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)



    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(topleft=text_pos)
        self.window.blit(source=text_surf, dest=text_rect)