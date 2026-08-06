#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pygame

from code.Const import ENTITY_HEALTH


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        # Carregamento da imagem e posicionamento do rect
        self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0

        # Proteção com .get(): se o nome não estiver no dicionário (ex: tiros), usa 0 como padrão
        self.health = ENTITY_HEALTH.get(self.name, 0)

    @abstractmethod
    def move(self):
        pass

    def shoot(self):
        return None