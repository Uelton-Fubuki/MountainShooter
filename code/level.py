#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAM_TIME, C_GREEN, C_CYAN, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL
from code.EntityMediator import EntityMediator
from code.enemy import Enemy
from code.entity import Entity
from code.entityFactory import EntityFactory
from code.player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []

        # Carrega o cenário e jogadores
        bg_entities = EntityFactory.get_entity(self.name + 'Bg')
        if bg_entities:
            self.entity_list.extend(bg_entities)

        player = EntityFactory.get_entity('Player1')
        if player:
            player.score = player_score[0]
            self.entity_list.append(player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            if player:
                player.score = player_score[1]
                self.entity_list.append(player)

        pygame.time.set_timer(EVENT_ENEMY, SPAM_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def run(self, player_score: list[int]):
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
                    if isinstance(ent, (Player, Enemy)):
                        shoot = ent.shoot()
                        if shoot is not None:
                            self.entity_list.append(shoot)
                    if ent.name == 'Player1':
                        self.level_text(14, f'Player1 - Health: {ent.health} | Score: {ent.score}', C_GREEN, (10, 25))
                    if ent.name == 'Player2':
                        self.level_text(14, f'Player2 - Health: {ent.health}| Score: {ent.score}', C_CYAN, (10, 45))
                else:
                    print("Atenção: Existe um elemento None na entity_list!")

            # 2. Captura de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    enemy = EntityFactory.get_entity(choice)
                    if enemy:
                        self.entity_list.append(enemy)

                # Contabilização do Timeout do nível
                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout <= 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score
                        pygame.time.set_timer(EVENT_TIMEOUT, 0)
                        pygame.time.set_timer(EVENT_ENEMY, 0)
                        return True

            # Checagem de Game Over (se os jogadores morreram)
            found_player = False
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    found_player = True

            if not found_player:
                pygame.time.set_timer(EVENT_TIMEOUT, 0)
                pygame.time.set_timer(EVENT_ENEMY, 0)
                return False

            # 3. Desenha os textos na tela
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'FPS: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'ENTIDADES: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(topleft=text_pos)
        self.window.blit(source=text_surf, dest=text_rect)